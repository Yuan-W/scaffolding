import json
from ..exercise_manager import exercise_manager
import unittest

exercise_index = 1
exercise_index_2 = 2
instructor_id = 1
exercise_name = 'reverse a list'
exercise_name_2 = 'name 2'
test_code = 'def test_reverse_list():\n\tassert reverse_list([1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1]'
hints = '>>> L = [0,1,2,3]\n>>> L[::-1]\n[3, 2, 1, 0]'
description = 'reverse list without using the builtin reverse()'
template = 'list = [1 ,2, 3, 4]'

def get(app, instructor_id, exercise_index):
    return app.get('/exercise/%d_%d' % (instructor_id, exercise_index), content_type='application/json')

def post(app, exercise_index, instructor_id, name, test_code, hints, description=None, template=None):
    request_data = dict()
    if name != None:
        request_data['name'] = name
    if instructor_id != None:
        request_data['instructor_id'] = instructor_id
    if test_code != None:
        request_data['test_code'] = test_code
    if hints != None:
        request_data['hints'] = hints
    if description != None:
        request_data['description'] = description
    if template != None:
        request_data['template'] = template
    return app.post('/exercise/%d/%d' % (instructor_id, exercise_index), data=json.dumps(request_data), content_type='application/json')

class TestManagementTestCase(unittest.TestCase):

    def setUp(self):
        self.app = exercise_manager.app.test_client()

    def test_parameter_existence(self):
        response = post(self.app, exercise_index, instructor_id, None, test_code, hints)
        self.assertEqual(response.status_code, 400)
        assert b'name must exist' in response.data

        response = post(self.app, exercise_index, instructor_id, exercise_name, None, hints)
        self.assertEqual(response.status_code, 400)
        assert b'test_code must exist' in response.data

        response = post(self.app, exercise_index, instructor_id, exercise_name, test_code, None)
        self.assertEqual(response.status_code, 400)
        assert b'hints must exist' in response.data

    def test_complete_post(self):
        response = post(self.app, exercise_index, instructor_id, exercise_name, test_code, hints)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        assert b'rev' in json_data
        assert b'id' in json_data

    def test_complete_get(self):
        response = post(self.app, exercise_index, instructor_id, exercise_name, test_code, hints, description, template)
        response = get(self.app, instructor_id, exercise_index)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['name'], exercise_name)
        self.assertEqual(json_data['instructor_id'], instructor_id)
        self.assertEqual(json_data['test_code'], test_code)
        self.assertEqual(json_data['hints'], hints)
        self.assertEqual(json_data['description'], description)
        self.assertEqual(json_data['template'], template)

    def test_fetch_names(self):
        response = post(self.app, exercise_index, instructor_id, exercise_name, test_code, hints)
        response = post(self.app, exercise_index_2, instructor_id, exercise_name_2, test_code, hints)

        request_data = dict()
        response = self.app.post('/names' , data=json.dumps(request_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        assert b'ids must exist' in response.data

        request_data['ids'] = '1_1'
        response = self.app.post('/names' , data=json.dumps(request_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        assert b'ids must be a list' in response.data

        request_data['ids'] = ['1_1', '1_2']
        response = self.app.post('/names' , data=json.dumps(request_data), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.data)
        self.assertEqual(len(json_data), 2)
        self.assertEqual(json_data[0]['id'], request_data['ids'][0])
        self.assertEqual(json_data[0]['name'], exercise_name)
        self.assertEqual(json_data[1]['id'], request_data['ids'][1])
        self.assertEqual(json_data[1]['name'], exercise_name_2)

    def test_get_all(self):
        response = post(self.app, exercise_index, instructor_id, exercise_name, test_code, hints)
        response = post(self.app, exercise_index_2, instructor_id, exercise_name_2, test_code, hints)

        response = self.app.get('/exercises' ,content_type='application/json')
        ids = ['1_1', '1_2']
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.data)
        self.assertEqual(len(json_data) >= 2, True)
        # self.assertEqual(json_data[0]['id'], ids[0])
        # self.assertEqual(json_data[0]['name'], exercise_name)
        # self.assertEqual(json_data[1]['id'], ids[1])
        # self.assertEqual(json_data[1]['name'], exercise_name_2)

if __name__ == '__main__':
    unittest.main()