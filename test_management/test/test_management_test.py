import json
from ..test_management import test_management
import unittest

exercise_id = 1
test_code = 'def test_reverse_list():\n\tassert reverse_list([1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1]'

def get(app, exercise_id):
    return app.get('/exercises/' + str(exercise_id) + '/tests', content_type='application/json')

def post(app, exercise_id, test_code):
    request_data = dict()
    if test_code != None:
        request_data['test_code'] = test_code
    return app.post('/exercises/' + str(exercise_id) + '/tests', data=json.dumps(request_data), content_type='application/json')


class TestManagementTestCase(unittest.TestCase):

    def setUp(self):
        self.app = test_management.app.test_client()

    def test_parameter_existence(self):
        response = post(self.app, exercise_id, None)
        self.assertEqual(response.status_code, 400)
        assert b'test_code must exist' in response.data

    def test_complete_post(self):
        response = post(self.app,  exercise_id, test_code)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['exercise_id'], exercise_id)
        self.assertEqual(json_data['test_code'], test_code)

    def test_complete_get(self):
        response = get(self.app, exercise_id)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()