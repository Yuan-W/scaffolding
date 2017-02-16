import sys,os
import json
import unittest
from ..stats_analysis.py import StatsAnalyser

student_id = 3
exercise_id = 2
time_spend = 200
test_status = 'failed'

def post(app, test_status, time_spent, exercise_id, student_id):
    request_data = dict()
    if test_status != None:
        request_data['test_status'] = test_status
    if time_spent != None:
        request_data['time_spent'] = time_spent
    if exercise_id != None:
        request_data['exercise_id'] = exercise_id
    if student_id != None:
    	request_data['student_id'] = student_id
    return app.post('/%d' % exercise_id, data=json.dumps(request_data), content_type='application/json')


class StatsAnalyserTestCase(unittest.TestCase):

    def setUp(self):
        sys._called_from_test = True
        self.app = stats_analysis.app.test_client()

    def test_parameter_existence(self):
        response = post(self.app, None, time_spent, exercise_id, student_id)
        self.assertEqual(response.status_code, 400)
        assert b'test_status must exists' in response.data

        response = post(self.app, test_status, None, exercise_id, student_id)
        self.assertEqual(response.status_code, 400)
        assert b'time_spent must exists and be a integer' in response.data

        response = post(self.app, test_status, time_spent, None, student_id)
        self.assertEqual(response.status_code, 400)
        assert b'exercise_id must exists and be a integer' in response.data

    def test_complete_post(self):
        response = post(self.app, test_status, time_spent, exercise_id, student_id)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()