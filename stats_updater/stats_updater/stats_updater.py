import os
import sys
import json
import requests
from flask import Flask, jsonify, request
from flask_restful import reqparse, Api, Resource, marshal_with, fields
from config import Development, Production, Testing

config = {
    "production": Production,
    "testing": Testing,
    "development": Development,
    "default": Development
}

app = Flask(__name__)
api = Api(app)

config_name = os.getenv('FLASK_CONFIGURATION', 'default')
app.config.from_object(config[config_name])
# app.config.from_pyfile('../config.cfg')

stats_db_url = app.config['STATS_DB_ADDRESS']

stats_parser = reqparse.RequestParser()
stats_parser.add_argument('instructor_id', type=int, location='json', required=True, help='instructor_id must exists and be a integer')
stats_parser.add_argument('time_spent', type=int, location='json', required=True, help='time_spent must exists and be a integer')
stats_parser.add_argument('code', location='json', required=True, help='code must exists')
stats_parser.add_argument('test_status', location='json', required=True, help='test_status must exists')
stats_parser.add_argument('hints_number', type=int, location='json', required=True, help='hints_number must exists')

class StatsUpdater(Resource):
    def get(self, student_id, exercise_id):
        response = requests.get('%s/progress/_design/stats/_view/default?key=[%d,%d]' % (stats_db_url, student_id, exercise_id),
                                    headers={'Content-Type': 'application/json'
                                    })
        return response.json(), response.status_code

    def post(self, student_id, exercise_id):
        args = stats_parser.parse_args()
        data = dict()
        # data['id'] = '%d_%d' % (student_id, exercise_id)
        data['student_id'] = student_id
        data['exercise_id'] = exercise_id
        data['instructor_id'] = args['instructor_id']
        data['time_spent'] = args['time_spent']
        data['test_status'] = args['test_status']
        data['code'] = args['code']
        data['hints_number'] = args['hints_number']
        response = requests.post('%s/progress/_design/stats/_update/default/%d_%d' % (stats_db_url, student_id, exercise_id),
                                    data=json.dumps(data),
                                    headers={'Content-Type': 'application/json'
                                    })
        json_resp = response.json()
        json_resp['id'] = response.headers['X-Couch-Id']
        json_resp['rev'] = response.headers['X-Couch-Update-NewRev']

        return json_resp, response.status_code

@app.cli.command('initdb')
def init_db():
    view_data = { "_id": "_design/stats",
                  "language": "javascript",
                  "views": 
                  {
                    "default": 
                    {
                      "map": "function(doc) { emit([doc.student_id, doc.exercise_id], doc) }"
                    }
                  },
                  "updates": 
                  {
                    "default": '''function(doc, req) { 
                                    var fields = JSON.parse(req.body)
                                    if (!doc){
                                        if ('id' in req && req['id']){
                                            return [{'_id': req['id'], 
                                                     'student_id': fields['student_id'],
                                                     'exercise_id': fields['exercise_id'],
                                                     'instructor_id': fields['instructor_id'],
                                                     'time_spent': fields['time_spent'],
                                                     'test_status': fields['test_status'],
                                                     'hints_number': fields['hints_number'],
                                                     'code': fields['code']
                                                     }, 
                                                     toJSON({'message': 'doc created'})
                                                    ]
                                        }
                                        return [null, toJSON({'message':'reuqest does not contain id'})]
                                    }
                                    for(var key in fields)
                                    {
                                        doc[key] = fields[key]
                                    }

                                    return [doc, toJSON({'message':'doc updated'})]
                                }'''
                  }
                }
    view = requests.post('%s/progress' % stats_db_url,
                            headers={'Content-Type': 'application/json'},
                            data = json.dumps(view_data)
                            )
    # print view.content
    print('Database initialised.')

def seed():
    return

def delete_doc(doc_id, doc_rev):
    requests.delete('%s/progress/%s?rev=%s' % (stats_db_url, doc_id, doc_rev),
                                headers={'Content-Type': 'application/json'
                                })

@app.cli.command('cleardb')
def cleardb():
    """Initializes the database."""
    docs = requests.get('%s/progress/_all_docs' % stats_db_url, 
                            headers={'Content-Type': 'application/json'
                            })
    for d in docs.json()['rows']:
        # if not (u'_design') in d['id']:
            delete_doc(d['id'], d['value']['rev'])
    print('Database cleared.')


api.add_resource(StatsUpdater, '/stats/<int:student_id>/<int:exercise_id>')

# @app.route('/get/<int:user_id>', methods=['GET'])
# def get_stats():

if __name__ == '__main__':
    app.run(debug=True, port=5002)