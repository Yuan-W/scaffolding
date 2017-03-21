import os
import requests
from flask import Flask, request, jsonify, abort
from flask_restful import reqparse, Api, Resource, marshal_with, fields
from config import Development, Production, Testing

app = Flask(__name__)
api = Api(app)

config = {
    "production": Production,
    "testing": Testing,
    "development": Development,
    "default": Development
}

config_name = os.getenv('FLASK_CONFIGURATION', 'default')
app.config.from_object(config[config_name])
# app.config.from_pyfile('../config.cfg')

stats_updater_url = app.config['ADDRESS_STATS_UPDATER']
test_runner_url = app.config['ADDRESS_TEST_RUNNER']
exericise_manager_url = app.config['ADDRESS_EXERCISE_MANAGER']

resource_fields = {
    'student_id':   fields.Integer,
    'exercise_id':  fields.Raw,
    'hints':   fields.Raw
}

parser = reqparse.RequestParser()
parser.add_argument('student_id', type=int, location='json', required=True, help='student_id must exists and be an integer')
parser.add_argument('exercise_id', location='json', required=True, help='exercise_id must exists')
parser.add_argument('instructor_id', type=int, location='json', required=True, help='instructor_id must exists and be an integer')
parser.add_argument('time_spent', type=int, location='json', required=True, help='time_spent must exists and be an integer')
parser.add_argument('hints_number', type=int, location='json', required=True, help='hints_number must exists and be an integer')
parser.add_argument('code', location='json', required=True, help='code must exists')

# Create a test instance on test server, and return test result
def get_test_result(code, script):
    url = '%s/test/' % (test_runner_url)
    data = {"code":code, "testCode":script}
    response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
    return response.json(),  response.status_code

def store_stats(student_id, exercise_id, stat):
    url = '%s/stats/%d/%s' % (stats_updater_url, student_id, exercise_id)
    response = requests.post(url, headers={'Content-Type': 'application/json'}, json=stat)
    return response.json(), response.status_code

def get_exercise(exercise_id):
    url = '%s/exercise/%s' % (exericise_manager_url, exercise_id)
    response = requests.get(url, headers={'Content-Type': 'application/json'})
    if app.debug:
        print(url)
        print(response.json())
    return response.json(), response.status_code

class Hint(object):
    def __init__(self, student_id, exercise_id, hints):
        self.student_id = student_id
        self.exercise_id = exercise_id
        self.hints = hints

# Hints
# Return hints based on correctness and time_spent
class HintsProvider(Resource):
    # @marshal_with(resource_fields)
    @marshal_with(resource_fields)
    def post(self, **kwargs):
        args = parser.parse_args()
        code = args['code']
        student_id = args['student_id']
        exercise_id = args['exercise_id']

        response = get_exercise(exercise_id)
        if response[1] != 200:
            return response
        script = response[0]['test_code']
        hint = response[0]['hints']

        response = get_test_result(code, script)
        if response[1] != 200:
            return response[0]['errors'], response[1]
        test_result = response[0]['results']
        
        stat = {
                'instructor_id': args['instructor_id'],
                'hints_number': args['hints_number'],
                'time_spent': args['time_spent'],
                'code': code,
                'test_status': test_result
                }
        response = store_stats(student_id, exercise_id, stat)
        if response[1] == 201:
            return Hint(student_id=student_id, exercise_id=exercise_id, hints=hint)
        return response

api.add_resource(HintsProvider, '/hints')


if __name__ == '__main__':
    app.run(debug=True, port=5001)