import json
import requests

class ExerciseDBHandler():
    def __init__(self, db_url):
      self.db_url = db_url
      self.table = 'exercise'

    def bulk_fetch(self, ids):
        ids = [str(e) for e in ids]
        data = {'keys':ids}

        response = requests.post('%s/%s/_all_docs?include_docs=true' % (self.db_url, self.table),
                                    data=json.dumps(data),
                                    headers={'Content-Type': 'application/json'
                                    })
        return response.json(), response.status_code

    def get_all(self):
        response = requests.get('%s/%s/_all_docs?include_docs=true' % (self.db_url, self.table),
                                    headers={'Content-Type': 'application/json'
                                    })
        if response.status_code != 200:
            return response.json(), response.status_code

        json_reply = response.json()['rows']
        json_reply = [e['doc'] for e in json_reply if not e['id'].startswith('_design')]
        return json_reply, response.status_code

    def get_exercise(self, doc_id):
        response = requests.get('%s/%s/%s' % (self.db_url, self.table, doc_id),
                                    headers={'Content-Type': 'application/json'
                                    })
        return response.json(), response.status_code

    def post_exercise(self, instructor_id, exercise_index, name, test_code, hints, description=None, template=None):
        data = {
                'name':name,
                'instructor_id': instructor_id,
                'exercise_index': exercise_index,
                'test_code': test_code,
                'hints': hints
                }
        if description is not None:
            data['description'] = description
        if template is not None:
            data['template'] = template
        response = requests.post('%s/%s/_design/hints/_update/default/%d_%d' % (self.db_url, self.table, instructor_id, exercise_index),
                                    data=json.dumps(data),
                                    headers={'Content-Type': 'application/json'
                                    })
        json_resp = response.json()
        json_resp['id'] = response.headers['X-Couch-Id']
        json_resp['rev'] = response.headers['X-Couch-Update-NewRev']

        return json_resp, response.status_code

    def init_db(self):
        response = requests.get('%s/%s' % (self.db_url, self.table))
        if response.status_code == 404:
            response = requests.put('%s/%s' % (self.db_url, self.table))
        design_id = '_design/hints'
        update_doc = {'name' : 'default',
                      'content':  '''function(doc, req) { 
                                        var fields = JSON.parse(req.body)
                                        if (!doc){
                                            if ('id' in req && req['id']){
                                                return [{'_id': req['id'], 
                                                         'name': fields['name'],
                                                         'test_code': fields['test_code'],
                                                         'instructor_id': fields['instructor_id'],
                                                         'exercise_index': fields['exercise_index'],
                                                         'hints': fields['hints']
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
                                    }'''}

        view_data = { "_id": design_id,
                      "language": "javascript",
                      "updates": 
                      {
                        update_doc['name']: update_doc['content']
                      }
                    }
        response = requests.post('%s/%s' % (self.db_url, self.table),
                                headers={'Content-Type': 'application/json'},
                                data = json.dumps(view_data)
                                )
        return response.json(), response.status_code

    def delete_doc(self, doc_id, doc_rev):
        requests.delete('%s/%s/%s?rev=%s' % (self.db_url, self.table, doc_id, doc_rev),
                                    headers={'Content-Type': 'application/json'
                                    })

    def cleardb(self):
        docs = requests.get('%s/%s/_all_docs' % (self.db_url, self.table), 
                                headers={'Content-Type': 'application/json'
                                })
        for d in docs.json()['rows']:
            self.delete_doc(d['id'], d['value']['rev'])

