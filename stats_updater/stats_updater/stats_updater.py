from flask import Flask
from flask_restful import reqparse, Api, Resource, marshal_with, fields

app = Flask(__name__)
api = Api(app)

resource_fields = {
    'student_id':   fields.Integer,
    'exercise_id':  fields.Integer,
    'time_spent':   fields.Integer,
    'test_status':  fields.Raw
}

parser = reqparse.RequestParser()
parser.add_argument('exercise_id', type=int, location='json', required=True, help='exercise_id must exists and be a integer')
parser.add_argument('time_spent', type=int, location='json', required=True, help='time_spent must exists and be a integer')
parser.add_argument('test_status', location='json', required=True, help='test_status must exists')

class Stats(object):
  def __init__(self, student_id, exercise_id, time_spent, test_status):
    self.student_id = student_id
    self.exercise_id = exercise_id
    self.time_spent = time_spent
    self.test_status = test_status

class StatsUpdater(Resource):
  @marshal_with(resource_fields)
  def post(self, student_id):
    args = parser.parse_args()
    return Stats(student_id, args['exercise_id'], args['time_spent'], args['test_status'])


api.add_resource(StatsUpdater, '/<int:student_id>')

# @app.route('/get/<int:user_id>', methods=['GET'])
# def get_stats():

if __name__ == '__main__':
    app.run(debug=True, port=5002)