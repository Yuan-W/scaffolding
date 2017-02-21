import sys
from flask import Flask, jsonify
from flask_restful import reqparse, Api, Resource, marshal_with, fields
import json
import requests

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('exercise_id', type=int, location='json', required=True, help='exercise_id must exists and be a integer')
parser.add_argument('student_id', type=int, location='json', required=True, help='student_id must exists and be a integer')
parser.add_argument('time_spent', type=int, location='json', required=True, help='time_spent must exists and be a integer')
parser.add_argument('code', location='json', required=True, help='code must exists')
parser.add_argument('test_status', location='json', required=True, help='test_status must exists')

class Stats(object):
  def __init__(self, student_id, exercise_id, time_spent, test_status):
    self.student_id = student_id
    self.exercise_id = exercise_id
    self.time_spent = time_spent
    self.test_status = test_status

class StatsUpdater(Resource):
  def post(self, student_id):
    args = parser.parse_args()
    data = dict()
    data['exercise_id'] = args['exercise_id']
    data['student_id'] = args['student_id']
    data['time_spent'] = args['time_spent']
    data['code'] = args['code']
    if sys._called_from_test:
        db_url = 'http://localhost:5984'
    else:
        db_url = 'http://10.0.1.6:5984'
    response = requests.post('%s/progress/' % db_url,
                                data=json.dumps(data),
                                headers={
                                    'Content-Type': 'application/json'
                                })

    return response.json(), response.status_code


api.add_resource(StatsUpdater, '/<int:student_id>')

# @app.route('/get/<int:user_id>', methods=['GET'])
# def get_stats():

if __name__ == '__main__':
    app.run(debug=True, port=5002)