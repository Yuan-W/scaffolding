import sys
import json
from flask import Flask, g
import flaskext.couchdb

app = Flask(__name__)
app.config.from_object(__name__)

#create the view for CouchDB
docs_by_exercise = flaskext.couchdb.ViewDefinition('docs','exercise_id','''\
    function(doc){
        emit(doc.exercise_id,doc)
    }
  ''')

test_url = 'http://localhost:5984'
db_url = 'http://admin:ANfCd8PDW8QhNAWd@10.0.0.6:5984'

app.config.update(
  DEBUG = True,
  COUCHDB_SERVER = test_url,
  COUCHDB_DATABASE = 'progress'
)
manager = flaskext.couchdb.CouchDBManager()
manager.setup(app)
manager.add_viewdef(docs_by_exercise)
manager.sync(app)

#return the docs
@app.route("/<exercise_id>/docs")
def docs(exercise_id):
  response = dict()
  response['docs'] = []
  for row in docs_by_exercise(g.couch)[int(exercise_id)]:
    response['docs'].append(row.value)
  return json.dumps(response)

#configuration
if __name__ == '__main__':
  app.run(debug=True, port=5005)