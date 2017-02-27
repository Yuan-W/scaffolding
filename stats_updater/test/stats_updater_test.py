import os,sys
from ..stats_updater import stats_updater
import json
import unittest

student_id = 1
exercise_id = 2
instructor_id = 3
time_spent = 300
code = 'code'
test_status = 'failed'

def post(app, student_id, exercise_id, test_status, time_spent, instructor_id, code):
    request_data = dict()
    if test_status != None:
        request_data['test_status'] = test_status
    if time_spent != None:
        request_data['time_spent'] = time_spent
    if instructor_id != None:
        request_data['instructor_id'] = instructor_id
    if code != None:
        request_data['code'] = code
    return app.post('/stats/%d/%d' % (student_id, exercise_id), data=json.dumps(request_data), content_type='application/json')


class StatsTestCase(unittest.TestCase):

    def setUp(self):
        sys._called_from_test = True
        self.app = stats_updater.app.test_client()
        self.doc_ids = []

    def tearDown(self):
        for d in self.doc_ids:
            stats_updater.delete_doc(d[0], d[1])
        return

    def test_parameter_existence(self):
        response = post(self.app, student_id, exercise_id, None, time_spent, instructor_id, code)
        self.assertEqual(400, response.status_code)
        assert b'test_status must exists' in response.data

        response = post(self.app, student_id, exercise_id, test_status, None, instructor_id, code)
        self.assertEqual(400, response.status_code)
        assert b'time_spent must exists and be a integer' in response.data

        response = post(self.app, student_id, exercise_id, test_status, time_spent, None, code)
        self.assertEqual(400, response.status_code)
        assert b'instructor_id must exists' in response.data

        response = post(self.app, student_id, exercise_id, test_status, time_spent, instructor_id, None)
        self.assertEqual(400, response.status_code)
        assert b'code must exists' in response.data

    def test_complete_post(self):
        response = post(self.app, student_id, exercise_id, test_status, time_spent, instructor_id, code)
        json_data = json.loads(response.data)
        self.doc_ids.append((json_data['id'], json_data['rev']))
        self.assertEqual(201, response.status_code)

    def test_get(self):
        response = post(self.app, student_id, exercise_id, test_status, time_spent, instructor_id, code)
        print response
        json_data = json.loads(response.data)
        doc_id = json_data['id']
        doc_rev = json_data['rev']
        self.doc_ids.append((doc_id, doc_rev))


        response = self.app.get('/stats/%d/%d' % (student_id, exercise_id), content_type='application/json')
        json_data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        # print json_data
        doc = json_data['rows'][0]
        self.assertEqual(doc_id, doc['id'])
        self.assertEqual(student_id, doc['value']['student_id'])
        self.assertEqual(exercise_id, doc['value']['exercise_id'])
        self.assertEqual(time_spent, doc['value']['time_spent'])
        self.assertEqual(instructor_id, doc['value']['instructor_id'])
        self.assertEqual(code, doc['value']['code'])
        self.assertEqual(test_status, doc['value']['test_status'])

    def test_update(self):
        response = post(self.app, student_id, exercise_id, test_status, time_spent, instructor_id, code)
        json_data = json.loads(response.data)
        doc_id = json_data['id']
        doc_rev = json_data['rev']
        self.doc_ids.append((doc_id, doc_rev))

        new_time_sepnt = time_spent + 100
        new_code = code*3
        new_test_status = 'passed'

        response = post(self.app, student_id, exercise_id, new_test_status, new_time_sepnt, instructor_id, new_code)
        json_data = json.loads(response.data)
        
        self.assertEqual(201, response.status_code)

        response = self.app.get('/stats/%d/%d' % (student_id, exercise_id), content_type='application/json')
        json_data = json.loads(response.data)
        self.assertEqual(200, response.status_code)

        doc = json_data['rows'][0]
        self.assertEqual(doc_id, doc['id'])
        self.assertEqual(student_id, doc['value']['student_id'])
        self.assertEqual(exercise_id, doc['value']['exercise_id'])
        self.assertEqual(new_time_sepnt, doc['value']['time_spent'])
        self.assertEqual(instructor_id, doc['value']['instructor_id'])
        self.assertEqual(new_code, doc['value']['code'])
        self.assertEqual(new_test_status, doc['value']['test_status'])

if __name__ == '__main__':
    unittest.main()