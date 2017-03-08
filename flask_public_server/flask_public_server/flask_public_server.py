import os
from json import dumps
from datetime import datetime
from flask import Flask, Response, request
from requests import post, get
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

def fetch_user_id(token):
    """for a given access_token returns a string user_id
    from oauth_access_tokens table in a database, unless token has expired"""
    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "SELECT `user_id`, `expires` FROM `oauth_access_tokens` WHERE `access_token`=%s"
    cursor.execute(sql, (token, )) #SQL query for the user_id and expiration time
    try:
        user_id, expires = cursor.fetchone()
    except TypeError:
        user_id, expires = None, None
    cursor.close()
    connection.close()
    if app.debug:        
        print(user_id, expires)
    if user_id and expires > datetime.now(): #if it was found check has it expired
        return user_id
    return None

def fetch_instructor_id(username):
    """for a given username returns an integer id from users table in a database"""
    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "SELECT `instructor` FROM `users` WHERE `username`=%s"
    cursor.execute(sql, (username, )) #SQL query for the instructor_id
    instructor_id = int(cursor.fetchone()[0])
    cursor.close()
    connection.close()
    if app.debug:        
        print(instructor_id)
    return instructor_id

def fetch_student_ids(username):
    """for a given username returns a tuple with integers student_id,
    instructor_id from users table in a database"""
    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "SELECT `id`, `instructor` FROM `users` WHERE `username`=%s"
    cursor.execute(sql, (username, )) #SQL query for the student_id
    try:
        student_id, instructor_id = cursor.fetchone()
    except TypeError:
        student_id, instructor_id = None, None
    cursor.close()
    connection.close()
    if app.debug:        
        print(student_id, instructor_id)
    return student_id, instructor_id

@app.route('/stats', methods=['GET'])
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
    user_id = fetch_user_id(access_token) #query db
    if not user_id:
        return Response("Wrong or expired access_token in GET header\n", status='401')
    instructor_id = fetch_instructor_id(user_id) #query db
    if not instructor_id:
        return Response("Inconsistent DB state, access_token doesn't provide a valid user\n", status='401')

    server_stats = app.config['ADDRESS_STATS']
    req = get(server_stats + str(instructor_id)) #forward GET
    if app.debug:
        print(req.text)
    if 'Content-Type' in req.headers:
        resp = Response(dumps(req.json()), mimetype='application/json')
        #resp.set_data(req.json()) #fill a response
        return resp #serve it back
    else:
        return Response("No JSON received in stats response\n", status='500')

@app.route('/hints', methods=['POST'])
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
    user_id = fetch_user_id(access_token) #query db
    if not user_id:
        return Response("Wrong or expired access_token in GET header\n", status='401')
    student_id, instructor_id = fetch_student_ids(user_id) #query db
    if not student_id or not instructor_id:
        return Response("Inconsistent DB state, access_token doesn't provide a valid user\n", status='401')
    
    server_hints = app.config['ADDRESS_HINTS']

    post_data = request.json
    post_data['student_id'] = student_id
    post_data['instructor_id'] = instructor_id
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    req = post(server_hints, json=post_data, headers=headers) #forward POST
    if 'Content-Type' in req.headers and \
        req.headers['Content-Type'] == 'application/json': #check reply
        resp = Response(dumps(req.json()), mimetype='application/json')
        #resp.set_data(req.json()) #fill a response
        return resp #serve it back
    else:
        return Response("No JSON received in hints response payload\n", status='500')


@app.route('/testmanagement', methods=['POST'])
def forward_test_management():
    """route /testmanagement response, looks for access_token in a header, and a json
    POST query. queries the db for access_token, and if finds an user_id,
    checks token expiration.
    and if found it then forwards the POST to server_test_management, accepts its reply
    and serves it back as initial request's response"""

    if 'access_token' not in request.headers:
        return Response("No access_token in POST header\n", status='401')
    access_token = request.headers['access_token'].encode('utf-8')
    if app.debug:
        print(access_token)
    user_id = fetch_user_id(access_token) #query db
    if not user_id:
        return Response("Wrong or expired access_token in POST header\n", status='401')
    instructor_id = fetch_instructor_id(user_id) #query db
    if not instructor_id:
        return Response("Inconsistent DB state, access_token doesn't provide a valid user\n", status='401')
    
    server_test_management = app.config['ADDRESS_TEST_MANAGEMENT']

    post_data = request.json
    post_data['instructor_id'] = instructor_id
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    req = post(server_test_management + str(instructor_id), json=post_data, headers=headers) #forward POST
    if 'Content-Type' in req.headers and \
        req.headers['Content-Type'] == 'application/json': #check reply
        resp = Response(dumps(req.json()), mimetype='application/json')
        #resp.set_data(req.json()) #fill a response
        return resp #serve it back
    else:
        return Response("No JSON received in test management response payload\n", status='500')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
