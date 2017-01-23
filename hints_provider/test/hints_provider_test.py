import os,sys
sys.path.append(os.path.abspath("../src"))
import json
import hints_provider
import unittest

student_id = 1
exercise_id = 2
time_spent = 3
code = 'test code'


def post(app, code, student_id, exercise_id, time_spent):
    request_data = dict()
    if code != None:
        request_data['code'] = code
    if student_id != None:
        request_data['student_id'] = student_id
    if exercise_id != None:
        request_data['exercise_id'] = exercise_id
    if time_spent != None:
        request_data['time_spent'] = time_spent
    return app.post('/hints', data=json.dumps(request_data), content_type='application/json')


class HintsProviderTestCase(unittest.TestCase):

    def setUp(self):
        self.app = hints_provider.app.test_client()

    def test_parameter_existence(self):
        response = post(self.app, None, student_id, exercise_id, time_spent)
        self.assertEqual(response.status_code, 400)
        assert b'code must exists' in response.data

        response = post(self.app, code, None, exercise_id, time_spent)
        self.assertEqual(response.status_code, 400)
        assert b'student_id must exists and be a integer' in response.data

        response = post(self.app, code, student_id, None, time_spent)
        self.assertEqual(response.status_code, 400)
        assert b'exercise_id must exists and be a integer' in response.data

        response = post(self.app, code, student_id, exercise_id, None)
        self.assertEqual(response.status_code, 400)
        assert b'time_spent must exists and be a integer' in response.data

    def test_complete_post(self):
        response = post(self.app, code, student_id, exercise_id, time_spent)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['student_id'], student_id)
        self.assertEqual(json_data['exercise_id'], exercise_id)
        self.assertEqual(json_data['hints'], 'Dummy Hints')

if __name__ == '__main__':
    unittest.main()