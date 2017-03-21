import os
from json import dumps
from datetime import datetime
import requests
from flask import Flask, Response, request, render_template, abort, session, redirect, url_for
from flaskext.mysql import MySQL
from flask_cache import Cache
from config import Development, Production, Testing

config = {
    "production": Production,
    "testing": Testing,
    "development": Development,
    "default": Development
}

app = Flask(__name__)
config_name = os.getenv('FLASK_CONFIGURATION', 'default')
app.config.from_object(config[config_name])
app.config.from_pyfile('../config.cfg')
app.secret_key = 'xnKt\x0cw\xa1\xc4t\xb9\x9a\xa6\x87Q\x1d\xec\x97\x84\x9avx\xf3"\x1e'

cache = Cache(app,config={'CACHE_TYPE': 'simple'})

mysql = MySQL()
mysql.init_app(app)

login_address = app.config['ADDRESS_LOGIN']
server_exercise = app.config['ADDRESS_EXERCISE_MANAGER']

########################################
# FLASK CLI Command
########################################

def init_db():
    connection = mysql.connect()
    cursor = connection.cursor()
    with app.open_resource('../schema.sql', mode='r') as f:
        cursor.execute(f.read())
    cursor.close()
    connection.close()

def seed_db():
    connection = mysql.connect()
    cursor = connection.cursor()
    with app.open_resource('../seed.sql', mode='rb') as f:
        cursor.execute(f.read())
    cursor.close()
    connection.commit()
    connection.close()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.cli.command('seeddb')
def seeddb_command():
    """Seed the database."""
    seed_db()
    print('Seed the database.')

########################################
# MySQL Query
########################################

def fetch_user_info(token):
    """for a given access_token returns student_id and instructor_id
    from oauth_access_tokens table in a database, unless token has expired"""
    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "SELECT `expires`, `instructor`, `id` FROM `oauth_access_tokens` INNER JOIN users on `oauth_access_tokens`.`user_id`=`users`.`username` WHERE `access_token`=%s"
    cursor.execute(sql, (token, )) #SQL query for the user_id and expiration time
    row = cursor.fetchone()
    

    if row is None:
        return None

    expires, instructor, user_id = row

    if app.debug:        
        print(user_id, expires, instructor)

    try:
        int(instructor)
    except ValueError:
        sql = "SELECT `instructors`.`id` FROM `oauth_access_tokens` INNER JOIN users on `oauth_access_tokens`.`user_id`=`users`.`username` INNER JOIN instructors on `users`.`instructor`=`instructors`.`username` WHERE `access_token`=%s"
        cursor.execute(sql, (token, ))
        instructor = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    if user_id and expires > datetime.now(): #if it was found check has it expired
        return user_id, int(instructor)
    return None

def fetch_instructor_info(authorization_code):
    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "SELECT `expires`, `username`, `id` FROM `oauth_authorization_codes` INNER JOIN instructors on `oauth_authorization_codes`.`user_id`=`instructors`.`username` WHERE `authorization_code`=%s"
    cursor.execute(sql, (authorization_code, ))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    expires, name, instructor_id = row
    if row is None:
        return None, 'User not found'
    if expires < datetime.now(): #if it was found check has it expired
        return None, 'Code expired'
    return int(instructor_id), name

def fetch_students(instructor_id):
    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "SELECT `users`.`id`, `users`.`username` FROM `users` INNER JOIN instructors on `users`.`instructor`=`instructors`.`username` WHERE `instructors`.`id`=%s"
    cursor.execute(sql, (instructor_id, ))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    students = []
    for row in rows:
        name = row[1].split('.')
        first_name = name[0].title()
        last_name = name[1].title()
        name = '%s %s' % (first_name, last_name)
        student = {'id':row[0], 'first_name':first_name, 'last_name':last_name, 'name':name}
        students.append(student)
    return students
    
########################################
# APIs for VSCode
########################################

@app.route('/api/stats', methods=['GET'])
def forward_stats():
    """route /stats response, looks for access_token in a header, queries
    the db for it, and if finds an user_id, checks token expiration.
    then finds instructor_id using user_id in db, forwards it
    through a GET to server_stats's /stats/instructor_id, accepts its reply
    and serves it back as initial request's response"""

    if 'access_token' not in request.headers:
        return Response("No access_token in GET header\n", status='401')
    access_token = request.headers['access_token'].encode('utf-8')

    if app.debug:
        print(access_token)

    row = fetch_user_info(access_token) #query db

    if not row:
        return Response("Wrong or expired access_token in GET header\n", status='401')

    student_id, instructor_id = row
    
    # # instructor_id = fetch_instructor_id(user_id) #query db
    # if not instructor_id:
    #     return Response("Inconsistent DB state, access_token doesn't provide a valid user\n", status='401')

    server_stats = app.config['ADDRESS_STATS']
    req = requests.get('%s/docs/%d' % (server_stats, instructor_id))#forward GET
    if app.debug:
        print(req.text)
    if 'Content-Type' in req.headers:
        resp = Response(dumps(req.json()), mimetype='application/json')
        #resp.set_data(req.json()) #fill a response
        return resp #serve it back
    else:
        return Response("No JSON received in stats response\n", status='500')

@app.route('/api/exercises', methods=['GET'])
def forward_exercises():
    if 'access_token' not in request.headers:
        return Response("No access_token in GET header\n", status='401')
    access_token = request.headers['access_token'].encode('utf-8')

    if app.debug:
        print(access_token)

    row = fetch_user_info(access_token) #query db

    if not row:
        return Response("Wrong or expired access_token in GET header\n", status='401')

    student_id, instructor_id = row
    
    if not instructor_id or not student_id:
        return Response("Inconsistent DB state, access_token doesn't provide a valid user\n", status='401')

    req = requests.get('%s/exercises' % server_exercise)

    if app.debug:
        print(req.text)
    if 'Content-Type' in req.headers:
        resp = Response(dumps(req.json()), mimetype='application/json')
        #resp.set_data(req.json()) #fill a response
        return resp #serve it back
    else:
        return Response("No JSON received in stats response\n", status='500')

@app.route('/api/hints', methods=['POST'])
def forward_hints():
    """route /hints response, looks for access_token in a header, and a json
    POST query. queries the db for access_token, and if finds an user_id,
    checks token expiration. then queries student_id/instructor_id,
    and if found it then forwards the POST to server_hints's /hints, accepts its reply
    and serves it back as initial request's response"""

    if 'access_token' not in request.headers:
        return Response("No access_token in POST header\n", status='401')
    if not 'Content-Type' in request.headers:
        return Response("No Content-Type set in POST header\n", status='400')
    if request.headers['Content-Type'] != 'application/json':
        return Response("Content-Type in POST header should be application/json\n",\
                        status='400')

    access_token = request.headers['access_token'].encode('utf-8')

    if app.debug:
        print(access_token)
     
    row = fetch_user_info(access_token) #query db
    if not row:
        return Response("Wrong or expired access_token in GET header\n", status='401')

    student_id, instructor_id = row

    server_hints = app.config['ADDRESS_HINTS']

    post_data = request.json
    post_data['student_id'] = student_id
    post_data['instructor_id'] = instructor_id
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    print(dumps(post_data))

    response = requests.post(server_hints, json=post_data, headers=headers) #forward POST

    if app.debug:
        print(response.content)

    if 'Content-Type' in response.headers and \
        response.headers['Content-Type'] == 'application/json': #check reply
        return Response(dumps(response.json()), mimetype='application/json') #serve it back
    else:
        return Response("No JSON received in hints response payload\n", status='500')

########################################
# Dashboard Backend
########################################

@cache.memoize(timeout=50)
def fetch_students_and_exercises(instructor_id):
    students = fetch_students(instructor_id)
    docs = requests.get('%s/docs/%d' % (app.config['ADDRESS_STATS'], instructor_id))
    exercise_stats = docs.json()['exercise_stats']
    student_stats = docs.json()['student_stats']
    exercise_names = requests.get('%s/exercises/%d' % (app.config['ADDRESS_EXERCISE_MANAGER'], instructor_id), headers={'Content-Type': 'application/json'})
    exercises = exercise_names.json()
    for exercise in exercises:
        stat = [s for s in exercise_stats if s['exercise_id'] == exercise['id']]
        if stat:
            exercise.update(stat[0])
        else:
            exercise['average_hints'] = 0
            exercise['average_time_spent'] = 0
            exercise['student_count'] = 0
    exercises = sorted(exercises, key=lambda k: k['name'])

    for student in students:
        stat = [s for s in student_stats if s['student_id'] == student['id']][0]
        student.update(stat)
    students = sorted(students, key=lambda k: k['name']) 

    return students, exercises

def valid_session_and_fetch_data():
    if 'instructor_id' not in session:
        return None, None
    return fetch_students_and_exercises(session['instructor_id'])

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard_controller():
    if request.method == 'POST':
        if 'authorization_code' not in request.form or 'authorized' not in request.form:
            abort(400)
        authorization_code = request.form['authorization_code']
        authorized = request.form['authorized']
        if authorized != 'Yes':
            abort(401)
        response = fetch_instructor_info(authorization_code)
        if(response[0] is None):
            abort(401, response[1])
        instructor_id, instructor_name = response
        session['instructor_id'] = instructor_id
        
        students, exercises = fetch_students_and_exercises(instructor_id)

        exercise_names = [str(e['name']) for e in exercises]

        return render_template('index.html', students=students, exercises=exercises, exercise_names=exercise_names)

    else:
        cache.delete_memoized(fetch_students_and_exercises)
        students, exercises = valid_session_and_fetch_data()
        if students is None or exercises is None:
            return redirect(login_address)

        exercise_names = [str(e['name']) for e in exercises]

        return render_template('index.html', students=students, exercises=exercises, exercise_names=exercise_names)

@app.route('/dashboard/student', methods=['GET'])
def student_controller():
    students, exercises = valid_session_and_fetch_data()
    if students is None or exercises is None:
        return redirect(login_address)

    student_id = request.args.get('id')
    response = requests.get('%s/docs/student/%s/%s' % (app.config['ADDRESS_STATS'], session['instructor_id'] , student_id))
    docs = response.json()['docs']
    for doc in docs:
        exercise_name = [s for s in exercises if s['id'] == doc['exercise_id']][0]
        doc['name'] = exercise_name['name']

    this_student = [ s for s in students if s['id'] == int(student_id) ][0]
    student = {'name': this_student['name'],
                'exercises': docs}

    return render_template('student.html', student=student, students=students, exercises=exercises)

@app.route('/dashboard/exercise', methods=['GET'])
def exercise_controller():
    students, exercises = valid_session_and_fetch_data()
    if students is None or exercises is None:
        return redirect(login_address)

    exercise_id = request.args.get('id')
    response = requests.get('%s/docs/exercise/%s/%s' % (app.config['ADDRESS_STATS'], session['instructor_id'] , exercise_id))
    docs = response.json()['docs']
    this_exercise = [ e for e in exercises if e['id'] == exercise_id ][0]
    for doc in docs:
        student_name = [s for s in students if s['id'] == doc['student_id']][0]
        doc['name'] = student_name['name']

    exercise = {'name': this_exercise['name'],
                'students': docs}

    return render_template('exercise.html', exercise=exercise, students=students, exercises=exercises)

@app.route('/dashboard/exercise/new', methods=['GET','POST'])
def new_exercise():
    students, exercises = valid_session_and_fetch_data()
    if students is None or exercises is None:
        return redirect(login_address)
    if request.method == 'POST':
        form_data = request.form
        json_data = {'name': form_data['name'], 'description': form_data['description'], 
            'test_code': form_data['test_code'], 'hints': 'hints'}
        if form_data['template'] != '':
            json_data['template'] = form_data['template']

        exercise_index = len(exercises) + 1
        response = requests.post('%s/exercise/%s/%s' % (server_exercise, session['instructor_id'], exercise_index), 
                        json=json_data, headers={'Content-Type': 'application/json'
                        })
        return redirect(url_for('dashboard_controller'))
    else:
        return render_template('new_exercise.html', students=students, exercises=exercises)

@app.route('/dashboard/logout')
def logout():
    session.pop('instructor_id', None)
    return redirect(login_address)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
