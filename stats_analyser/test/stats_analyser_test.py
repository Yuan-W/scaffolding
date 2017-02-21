import sys,os
import json
import unittest
from ..stats_analyser import stats_analyser

student_id = 3
exercise_id = 2
time_spend = 200
test_status = 'failed'

class StatsAnalyserTestCase(unittest.TestCase):

    def setUp(self):
        sys._called_from_test = True
        self.app = stats_analyser.app.test_client()

    def test_parameter_existence(self):
        response = self.app.get("/1/docs")
        self.assertEqual(response.status_code, 200)
        # assrt b'test_status must exists' in response.data


if __name__ == '__main__':
    unittest.main()