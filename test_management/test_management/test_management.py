from flask import Flask, request
from flask_restful import reqparse, Api, Resource, marshal_with, fields

app = Flask(__name__)
api = Api(app)

resource_fields = {
    'exercise_id': fields.Integer,
    'test_code': fields.String
}


parser = reqparse.RequestParser()
parser.add_argument('test_code', location='json', required=True, help='test_code must exist')

def get_test_code(exercise_id):
    # DB logic should go here
    test = "def test_reverse_list():\n\tassert reverse_list([1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1]"
    return test

def update_or_create_test(exercise_id, test_code):
    # DB logic should go here
    return Test(exercise_id=exercise_id, test_code=test_code)

def update_test(exercise_id, test_code):
    return update_or_create_test(exercise_id, test_code)

def create_test(exercise_id, test_code):
    return update_or_create_test(exercise_id, test_code)

class Test(object):
    def __init__(self, exercise_id, test_code):
        self.exercise_id = exercise_id
        self.test_code = test_code



# TestManagement
# Manage tests, retrieve tests for exercise, create tests for exercises, update tests for exercise
class TestManagement(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        exercise_id = kwargs['exercise_id']
        test_code = get_test_code(exercise_id)
        return Test(exercise_id=exercise_id, test_code=test_code)
    @marshal_with(resource_fields)
    def post(self, **kwargs):
        exercise_id = kwargs['exercise_id']
        args = parser.parse_args()
        test_code = args['test_code']
        new_test = create_test(exercise_id, test_code)
        return new_test
    @marshal_with(resource_fields)
    def put(self, **kwargs):
        exercise_id = kwargs['exercise_id']
        args = parser.parse_args()
        test_code = args['test_code']
        new_test = update_test(exercise_id, test_code)
        return new_test

##
## routing
##
api.add_resource(TestManagement, '/exercises/<int:exercise_id>/tests')


if __name__ == '__main__':
    app.run(debug=True, port=5003)