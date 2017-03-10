import json
import requests

class HintsDBHandler():
    def __init__(self, db_url, table):
      self.db_url = db_url
      self.table = table

    def getHints(self, exercise_id):
        response = requests.get('%s/%s/%d' % (self.db_url, self.table, exercise_id),
                                    headers={'Content-Type': 'application/json'
                                    })
        return response.json(), response.status_code

    def postHints(self, instructor_id, exercise_id, hints):
        data = {'instructor_id': instructor_id,
                'hints': hints}
        response = requests.post('%s/%s/_design/hints/_update/default/%d' % (self.db_url, self.table, exercise_id),
                                    data=json.dumps(data),
                                    headers={'Content-Type': 'application/json'
                                    })
        json_resp = response.json()
        json_resp['id'] = response.headers['X-Couch-Id']
        json_resp['rev'] = response.headers['X-Couch-Update-NewRev']

        return json_resp, response.status_code

    def init_db(self):
        design_id = '_design/hints'
        update_doc = {'name' : 'default',
                      'content':  '''function(doc, req) { 
                                        var fields = JSON.parse(req.body)
                                        if (!doc){
                                            if ('id' in req && req['id']){
                                                return [{'_id': req['id'], 
                                                         'exercise_id': fields['exercise_id'],
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
        response = requests.get('%s/%s/_design/hints' % (self.db_url, self.table),
                                headers={'Content-Type': 'application/json'},
                                )
        if response.status_code == 404:
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

