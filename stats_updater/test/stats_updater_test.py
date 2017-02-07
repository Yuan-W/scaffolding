import os,sys
from ..stats_updater import stats_updater
import json
import unittest

student_id = 1
exercise_id = 2
time_spent = 300
code = 'code'
test_status = 'failed'


def post(app, test_status, time_spent, exercise_id, student_id, code):
    request_data = dict()
    if test_status != None:
        request_data['test_status'] = test_status
    if time_spent != None:
        request_data['time_spent'] = time_spent
    if student_id != None:
        request_data['student_id'] = student_id
    if exercise_id != None:
        request_data['exercise_id'] = exercise_id
    if code != None:
        request_data['code'] = code
    return app.post('/%d' % student_id, data=json.dumps(request_data), content_type='application/json')


class StatsUpdaterTestCase(unittest.TestCase):

    def setUp(self):
        sys._called_from_test = True
        self.app = stats_updater.app.test_client()

    def test_parameter_existence(self):
        response = post(self.app, None, time_spent, exercise_id, student_id, code)
        self.assertEqual(response.status_code, 400)
        assert b'test_status must exists' in response.data

        response = post(self.app, test_status, None, exercise_id, student_id, code)
        self.assertEqual(response.status_code, 400)
        assert b'time_spent must exists and be a integer' in response.data

        response = post(self.app, test_status, time_spent, None, student_id, code)
        self.assertEqual(response.status_code, 400)
        assert b'exercise_id must exists and be a integer' in response.data

        response = post(self.app, test_status, time_spent, exercise_id, student_id, None)
        self.assertEqual(response.status_code, 400)
        assert b'code must exists' in response.data

    def test_complete_post(self):
        response = post(self.app, test_status, time_spent, exercise_id, student_id, code)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()