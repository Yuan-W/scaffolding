import os,sys
import json
from ..flask_public_server import flask_public_server
import unittest

name = 'jen krinke'
username = 'jenkins'
test = 'how to program in java?'
testID = '15'

def post(app, name, username, test, testID):
    request_data = dict()
    if name != None:
        request_data['name'] = name
    if username != None:
        request_data['username'] = username
    if test != None:
        request_data['test'] = test
    if testID != None:
        request_data['testID'] = testID
    return app.post('/api/hints', data=json.dumps(request_data), content_type='application/json')


class PublicServerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = hints_provider.app.test_client()

    def test_parameter_existence(self):
        response = post(self.app, name, None, test, testID)
        self.assertEqual(response.status_code, 400)
        assert b'code must exists' in response.data

    def test_complete_post(self):
        response = post(self.app, name, username, test, testID)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['name'], name)
        self.assertEqual(json_data['test'], test)
        self.assertEqual(json_data['testID'], testID)
        self.assertEqual(json_data['username'], username)

if __name__ == '__main__':
    unittest.main()