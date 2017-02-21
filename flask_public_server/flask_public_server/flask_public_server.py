from flask import Flask, Response, request
from requests import post, get
from json import dumps
from flaskext.mysql import MySQL
from datetime import datetime

app = Flask(__name__)
app.debug = True
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'oauth'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

portA = 5000 #remote stats / hints server port
portB = 5001 #remote stats / hints server port
serverA = 'http://10.1.1.6:{:d}/stats/'.format(portA)
serverB = 'http://10.1.1.6:{:d}/hints'.format(portB)

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
    sql = "SELECT `id` FROM `users` WHERE `username`=%s"
    cursor.execute(sql, (username, )) #SQL query for the instructor_id
    instructor_id = cursor.fetchone()
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
    sql = "SELECT `id`, `instructor_id` FROM `users` WHERE `username`=%s"
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
    through a GET to serverA's /stats/instructor_id, accepts its reply
    and serves it back as initial request's response"""
    global serverA
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
    req = get(serverA + str(instructor_id)) #forward GET
    if app.debug:
        print(req.text)
    if 'Content-Type' in req.headers and \
      req.headers['Content-Type'] == 'application/json': #check reply
        resp = Response(dumps(req.json()), mimetype='application/json')
        resp.set_data(req.json()) #fill a response
        return resp #serve it back
    else:
        return Response("No JSON received in stats response\n", status='404')

@app.route('/hints', methods=['POST'])
def forward_hints():
    """route /hints response, looks for access_token in a header, and a json
    POST query. queries the db for access_token, and if finds an user_id,
    checks token expiration. then queries student_id/instructor_id,
    and if found it then forwards the POST to serverB's /hints, accepts its reply
    and serves it back as initial request's response"""
    global serverB
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
    post_data = request.json
    post_data['student_id'] = student_id
    post_data['instructor_id'] = instructor_id
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    req = post(serverB, json=post_data, headers=headers) #forward POST
    if 'Content-Type' in req.headers and \
        req.headers['Content-Type'] == 'application/json': #check reply
        resp = Response(dumps(req.json()), mimetype='application/json')
        #resp.set_data(req.json()) #fill a response
        return resp #serve it back
    else:
        return Response("No JSON received in hints response payload\n", status='404')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
