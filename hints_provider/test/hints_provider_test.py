import os,sys
import json
from ..hints_provider import hints_provider
import unittest

student_id = 1
exercise_id = 2
instructor_id = 3
time_spent = 300
code = 'test code'
code = "def reverse_list(l):\n\treturn l[::-1]"
hints_number = 1
hints = {'test1':'hint1', 'test2':'hint2'}

def post(app, code, student_id, exercise_id, instructor_id, time_spent, hints_number):
    request_data = dict()
    if code != None:
        request_data['code'] = code
    if student_id != None:
        request_data['student_id'] = student_id
    if exercise_id != None:
        request_data['exercise_id'] = exercise_id
    if instructor_id != None:
        request_data['instructor_id'] = instructor_id
    if time_spent != None:
        request_data['time_spent'] = time_spent
    if hints_number != None:
        request_data['hints_number'] = hints_number
    return app.post('/hints', data=json.dumps(request_data), content_type='application/json')

def postHint(app, instructor_id, exercise_id, hints):
    request_data = dict()
    if exercise_id != None:
        request_data['exercise_id'] = exercise_id
    if instructor_id != None:
        request_data['instructor_id'] = instructor_id
    if hints != None:
        request_data['hints'] = hints
    return app.post('/hint', data=json.dumps(request_data), content_type='application/json')

class HintsProviderTestCase(unittest.TestCase):

    def setUp(self):
        self.app = hints_provider.app.test_client()

    def test_hint_parameter(self):
        response = postHint(self.app, None, exercise_id, hints)
        self.assertEqual(response.status_code, 400)
        assert b'instructor_id must exists' in response.data

        response = postHint(self.app, instructor_id, None, hints)
        self.assertEqual(response.status_code, 400)
        assert b'exercise_id must exists' in response.data

        response = postHint(self.app, instructor_id, exercise_id, None)
        self.assertEqual(response.status_code, 400)
        assert b'hints must exists' in response.data

    def test_complete_post_hint(self):
        response = postHint(self.app, instructor_id, exercise_id, hints)
        self.assertEqual(response.status_code, 200)

    def test_parameter_existence(self):
        response = post(self.app, None, student_id, exercise_id, instructor_id, time_spent, hints_number)
        self.assertEqual(response.status_code, 400)
        assert b'code must exists' in response.data

        response = post(self.app, code, None, exercise_id, instructor_id, time_spent, hints_number)
        self.assertEqual(400, response.status_code)
        assert b'student_id must exists and be an integer' in response.data

        response = post(self.app, code, student_id, None, instructor_id, time_spent, hints_number)
        self.assertEqual(400, response.status_code)
        assert b'exercise_id must exists and be an integer' in response.data

        response = post(self.app, code, student_id, exercise_id, None, time_spent, hints_number)
        self.assertEqual(400, response.status_code)
        assert b'instructor_id must exists and be an integer' in response.data

        response = post(self.app, code, student_id, exercise_id, instructor_id, None, hints_number)
        self.assertEqual(400, response.status_code)
        assert b'time_spent must exists and be an integer' in response.data

        response = post(self.app, code, student_id, exercise_id, instructor_id, time_spent, None)
        self.assertEqual(400, response.status_code)
        assert b'hints_number must exists and be an integer' in response.data

    def test_complete_post(self):
        response = postHint(self.app, instructor_id, exercise_id, hints)
        
        response = post(self.app, code, student_id, exercise_id, instructor_id, time_spent, hints_number)
        json_data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(student_id, json_data['student_id'])
        self.assertEqual(exercise_id, json_data['exercise_id'])
        self.assertEqual(json.dumps(hints), json.dumps(json_data['hints']))

if __name__ == '__main__':
    unittest.main()