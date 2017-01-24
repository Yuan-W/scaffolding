from flask import Flask
from flask_restful import reqparse, Api, Resource, marshal_with, fields

app = Flask(__name__)
api = Api(app)

resource_fields = {
    'student_id':   fields.Integer,
    'exercise_id':  fields.Integer,
    'hints':   fields.Raw
}


parser = reqparse.RequestParser()
parser.add_argument('student_id', type=int, location='json', required=True, help='student_id must exists and be a integer')
parser.add_argument('exercise_id', type=int, location='json', required=True, help='exercise_id must exists and be a integer')
parser.add_argument('time_spent', type=int, location='json', required=True, help='time_spent must exists and be a integer')
parser.add_argument('code', location='json', required=True, help='code must exists')

# Create a test instance on test server, and return test result
def get_test_result(code):
    return 'Failed'

def get_hint(exercise_id, time_spent, test_result):
    return 'Dummy Hints'

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
        test_result = get_test_result(code)
        student_id = args['student_id']
        exercise_id = args['exercise_id']
        time_spent = args['time_spent']
        hint = get_hint(exercise_id, time_spent, test_result)
        return Hint(student_id=student_id, exercise_id=exercise_id, hints=hint)

##
## routing
##
api.add_resource(HintsProvider, '/hints')


if __name__ == '__main__':
    app.run(debug=True, port=5001)