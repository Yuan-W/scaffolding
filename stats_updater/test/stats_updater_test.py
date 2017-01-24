import os,sys
from ..stats_updater import stats_updater
import json
import unittest

student_id = 1
exercise_id = 2
time_spent = 300
test_status = 'failed'


def post(app, test_status, time_spent, exercise_id):
    request_data = dict()
    if test_status != None:
        request_data['test_status'] = test_status
    if time_spent != None:
        request_data['time_spent'] = time_spent
    if exercise_id != None:
        request_data['exercise_id'] = exercise_id
    return app.post('/%d' % student_id, data=json.dumps(request_data), content_type='application/json')


class StatsUpdaterTestCase(unittest.TestCase):

    def setUp(self):
        self.app = stats_updater.app.test_client()

    def test_parameter_existence(self):
        response = post(self.app, None, time_spent, exercise_id)
        self.assertEqual(response.status_code, 400)
        assert b'test_status must exists' in response.data

        response = post(self.app, test_status, None, exercise_id)
        self.assertEqual(response.status_code, 400)
        assert b'time_spent must exists and be a integer' in response.data

        response = post(self.app, test_status, time_spent, None)
        self.assertEqual(response.status_code, 400)
        assert b'exercise_id must exists and be a integer' in response.data

    def test_complete_post(self):
        response = post(self.app, test_status, time_spent, exercise_id)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['student_id'], student_id)
        self.assertEqual(json_data['exercise_id'], exercise_id)
        self.assertEqual(json_data['time_spent'], time_spent)
        self.assertEqual(json_data['test_status'], test_status)

if __name__ == '__main__':
    unittest.main()