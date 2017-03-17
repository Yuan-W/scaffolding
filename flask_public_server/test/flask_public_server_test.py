import unittest
import requests
from json import dumps
from ..flask_public_server import flask_public_server

class PublicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = flask_public_server.app.test_client()

    def post_exercise(self, instructor_id, exercise_index):
        exercise_manager_url = '%s/exercise/%d/%d' % (flask_public_server.app.config['ADDRESS_EXERCISE_MANAGER'], \
                                                    instructor_id, exercise_index)
        exercise_name = 'reverse a list'
        test_code = 'def test_reverse_list():\n\tassert reverse_list([1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1]'
        hints = '>>> L = [0,1,2,3]\n>>> L[::-1]\n[3, 2, 1, 0]'
        content = {
                    'name': exercise_name,
                    'test_code': test_code,
                    'hints': hints
                }

        response = requests.post(exercise_manager_url, json=content,
                                    headers={'Content-Type': 'application/json'
                                    })
    
    def test_stats_using_token(self):
        headers = {'access_token': '7f05ad622a3d32a5a81aee5d73a5826adb8cbf64'}
        headers['Content-Type'] = 'application/json'
        self.post_exercise(1234, 16)

        data = {"exercise_id": "1234_16", "time_spent": 30, "code": "ABCz;)examplebla123", "hints_number": 1}
        rv = self.app.post('/hints', headers=headers, data=dumps(data))
        rv = self.app.get('/api/stats', headers=headers)
        assert u'time_spent' in rv.data
        assert u'student_id' in rv.data
        assert rv.status_code == 200

    def test_stats_using_bad_header(self):
        headers = {'Token': '6f05ad622a3d32a5a81aee5d73a5826adb8cbf64'}
        rv = self.app.get('/api/stats', headers=headers)
        assert u'No access_token in GET header' in rv.data
        assert rv.status_code == 401

    def test_stats_using_wrong_token(self):
        headers = {'access_token': '6f05ad622a3d32a5a81aee5d73a5826adb8cbf63'}
        rv = self.app.get('/api/stats', headers=headers)
        assert u'Wrong or expired access_token in GET header' in rv.data
        assert rv.status_code == 401

    def test_hints_using_token(self):
        self.post_exercise(1234, 16)
        headers = {'access_token': '7f05ad622a3d32a5a81aee5d73a5826adb8cbf64'}
        headers['Content-Type'] = 'application/json'
        data = {"exercise_id": "1234_16", "time_spent": 30, "code": "ABCz;)examplebla123", "hints_number": 1}
        rv = self.app.post('/api/hints', headers=headers, data=dumps(data))
        assert u'student_id' in rv.data
        assert u'exercise_id' in rv.data
        assert u'hints' in rv.data
        assert '"exercise_id": "1234_16"' in rv.data
        assert rv.status_code == 200

    def test_hints_using_bad_token_header(self):
        headers = {'token': '7f05ad622a3d32a5a81aee5d73a5826adb8cbf64'}
        headers['Content-Type'] = 'application/json'
        data = {"exercise_id": "1234_16", "time_spent": 30, "code": "ABCz;)examplebla123"}
        rv = self.app.post('/api/hints', headers=headers, data=dumps(data))
        assert u'No access_token in POST header' in rv.data
        assert rv.status_code == 401

    def test_hints_using_bad_json_header(self):
        headers = {'access_token': '7f05ad622a3d32a5a81aee5d73a5826adb8cbf64'}
        headers['Content'] = 'application/json'
        data = {"exercise_id": "1234_16", "time_spent": 30, "code": "ABCz;)examplebla123"}
        rv = self.app.post('/api/hints', headers=headers, data=dumps(data))
        assert u'Content-Type in POST header should be application/json' in rv.data
        assert rv.status_code == 400
                
    def test_hints_using_wrong_token(self):
        headers = {'access_token': '5f05ad622a3d32a5a81aee5d73a5826adb8cbf64'}
        headers['Content-Type'] = 'application/json'
        data = {"exercise_id": "1234_16", "time_spent": 30, "code": "ABCz;)examplebla123"}
        rv = self.app.post('/api/hints', headers=headers, data=dumps(data))
        assert u'Wrong or expired access_token in GET header' in rv.data
        assert rv.status_code == 401
        
if __name__ == '__main__':
    unittest.main()
