import os
from json import dumps
from datetime import datetime
from flask import Flask, Response, request, render_template
import requests
from flaskext.mysql import MySQL
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
mysql = MySQL()
mysql.init_app(app)

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

def fetch_user_info(token):
    """for a given access_token returns student_id and instructor_id
    from oauth_access_tokens table in a database, unless token has expired"""
    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "SELECT `expires`, `instructor`, `id` FROM `oauth_access_tokens` INNER JOIN users on `oauth_access_tokens`.`user_id`=`users`.`username` WHERE `access_token`=%s"
    cursor.execute(sql, (token, )) #SQL query for the user_id and expiration time
    row = cursor.fetchone()
    cursor.close()
    connection.close()

    if row is None:
        return None

    expires, instructor, user_id = row

    if app.debug:        
        print(user_id, expires, instructor)

    if user_id and expires > datetime.now(): #if it was found check has it expired
        return user_id, int(instructor)
    return None

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

# @app.route('/docs', methods=['GET'])
# def forward_docs():
#     """route /docs response, looks for access_token in a header, queries
#     the db for it, and if finds an user_id, checks token expiration.
#     then finds instructor_id using user_id in db, forwards it
#     through a GET to serverA's /docs/instructor_id, accepts its reply
#     and serves it back as initial request's response"""
#     server_docs = app.config['ADDRESS_DOCS']
#     if 'access_token' not in request.headers:
#         return Response("No access_token in GET header\n", status='401')
#     access_token = request.headers['access_token'].encode('utf-8')
#     if app.debug:
#         print(access_token)
#     user_id = fetch_user_id(access_token) #query db
#     if not user_id:
#         return Response("Wrong or expired access_token in GET header\n", status='401')
#     instructor_id = fetch_instructor_id(user_id) #query db
#     if not instructor_id:
#         return Response("Inconsistent DB state, access_token doesn't provide a valid user\n", status='401')
#     req = get(server_docs + str(instructor_id)) #forward GET
#     if app.debug:
#         print(req.text)
#     resp = Response(req.text, status=req.status_code)
#     return resp #serve it back unchecked

# @app.route('/average/<exercise_id>', methods=['GET'])
# def forward_average(exercise_id):
#     """route /average response, looks for access_token in a header, queries
#     the db for it, and if finds an user_id, checks token expiration.
#     then finds instructor_id using user_id in db, forwards request
#     through a GET to server_average's /average/exercise_id, accepts its reply
#     and serves it back as initial request's response"""
#     server_average = app.config['ADDRESS_AVERAGE']
#     if 'access_token' not in request.headers:
#         return Response("No access_token in GET header\n", status='401')
#     access_token = request.headers['access_token'].encode('utf-8')
#     if app.debug:
#         print(access_token)
#     user_id = fetch_user_id(access_token) #query db
#     if not user_id:
#         return Response("Wrong or expired access_token in GET header\n", status='401')
#     req = get(server_average + exercise_id) #forward GET
#     if app.debug:
#         print(req.text)
#     if 'Content-Type' in req.headers and \
#       req.headers['Content-Type'] == 'application/json': #check reply
#         resp = Response(dumps(req.json()), mimetype='application/json')
#         # resp.set_data(req.json()) #fill a response
#         return resp #serve it back
#     else:
#         return Response("No JSON received in stats response\n", status='500')

# @app.route('/exercises/<id>/tests', methods=['GET', 'POST'])
# def forward_tests(id):
#     """route /exercises/<id>/tests response, looks for access_token in a header, and a json
#     POST query. queries the db for access_token, and if finds an user_id,
#     checks token expiration. then queries student_id/instructor_id,
#     and if found it then forwards the POST to server_test_management, accepts its reply
#     and serves it back as initial request's response"""
#     server_test_management = app.config['ADDRESS_EXERCISE_MANAGER']
#     if 'access_token' not in request.headers:
#         return Response("No access_token in " + request.method +\
#                         " header\n", status='401')
#     if request.method == 'POST':                        
#         if not 'Content-Type' in request.headers:
#             return Response("No Content-Type set in POST header\n", status='400')
#         if request.headers['Content-Type'] != 'application/json':
#             return Response("Content-Type in POST header should be application/json\n",\
#                             status='400')
#     access_token = request.headers['access_token'].encode('utf-8')
#     if app.debug:
#         print(access_token)
#     user_id = fetch_user_id(access_token) #query db
#     if not user_id:
#         return Response("Wrong or expired access_token in " + request.method +\
#                         " header\n", status='401')
#     if request.method == 'POST':
#         student_id, instructor_id = fetch_student_ids(user_id) #query db
#         if not student_id or not instructor_id:
#             return Response("Inconsistent DB state, access_token doesn't provide a valid user\n", status='401')
#         post_data = request.json
#         if id != str(post_data['exercise_id']):
#             return Response(str(post_data['exercise_id']) + " in POST data doesn't match " +\
#                             id + " in URL\n", status='400')
#         post_data['instructor'] = instructor_id
#         headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
#         req = post(server_test_management+id+'/tests', json=post_data, headers=headers) #forward POST
#     else: # it was a GET
#         headers = {'Accept': 'application/json'}
#         req = get(server_test_management+id+'/tests', headers=headers) #forward GET

#     if 'Content-Type' in req.headers and \
#       req.headers['Content-Type'] == 'application/json': #check reply
#         resp = Response(dumps(req.json()), mimetype='application/json')
#         # resp.set_data(req.json()) #fill a response
#         return resp #serve it back
#     else:
#         return Response("No JSON received in test response payload\n", status='500')


'''
Front-end endpints
TODO: get data from other services
'''

def new_student(s_id, name, exercise, time_spent):
    return {'id':s_id, 'name':name, 'exercise':exercise, 'time_spent':time_spent}
@app.route('/')
def show_entries():
    times = enumerate([100, 200, 300, 200, 100, 500])
    students = []
    students.append(new_student(1, 'Alice', [1,2,3,4], [300, 200, 500, 100]))
    students.append(new_student(2, 'Bob', [1,2], [500, 100]))

    exercise_ids = [e for s in students for e in s['exercise'] ]
    exercise_ids = set(exercise_ids)
    exercises = [{'id': e_id, 'name': 'exercise %d' % e_id} for e_id in exercise_ids]

    return render_template('index.html', students=students, exercises=exercises, times=times)

@app.route('/student')
def student():
    students_id = request.args.get('id')
    student = {'name': 'student %s' % students_id,
                'exercises': [{'name':'exercise 1', 'hints_number':5, 'time_spent':300},{'name':'exercise 2', 'hints_number':2, 'time_spent': 500}]}

    return render_template('student.html', student=student)

@app.route('/exercise')
def exercise():
    exercise_id = request.args.get('id')
    exercise = {'name': 'exercise %s' % exercise_id,
                'students': [{'name':'Alice', 'hints_number':5, 'time_spent':300},{'name':'Bob', 'hints_number':2, 'time_spent': 500}]}

    return render_template('exercise.html', exercise=exercise)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
