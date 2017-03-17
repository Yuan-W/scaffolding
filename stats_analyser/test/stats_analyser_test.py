import sys,os
import json
import unittest
import requests
from ..stats_analyser import stats_analyser

student_id = 3
exercise_id = "2"
instructor_id = 9
code = "def reverse_list(l):\n\treturn l[::-1]"
hints_number = 1
# test_status = "{'failed': {'tests': [], 'number': 0}, 'passed': {'number': 1}}"
test_status = 'failed'
time_spent = 300

class StatsAnalyserTestCase(unittest.TestCase):

    def setUp(self):
        sys._called_from_test = True
        self.app = stats_analyser.app.test_client()

    def test_connect(self):
        response = self.app.get("/docs/1")
        self.assertEqual(response.status_code, 200)

    def test_get_by_instructor_id(self):
        content = { "code": code,
                    "hints_number": hints_number,
                    "instructor_id": instructor_id,
                    "test_status": test_status,
                    "time_spent": time_spent
                  }
        response = requests.post('http://localhost:5002/stats/%d/%s' % (student_id, exercise_id), json=content)
        response = self.app.get("/docs/%d" % instructor_id)
        self.assertEqual(response.status_code, 200)
        print json.loads(response.data)
        json_response = json.loads(response.data)['docs'][0]
        self.assertEqual(json_response['student_id'], student_id)
        self.assertEqual(json_response['exercise_id'], exercise_id)
        self.assertEqual(json_response['instructor_id'], instructor_id)
        self.assertEqual(json_response['code'], code)
        self.assertEqual(json_response['hints_number'], hints_number)
        self.assertEqual(json_response['test_status'], test_status)
        self.assertEqual(json_response['time_spent'], time_spent)

if __name__ == '__main__':
    unittest.main()