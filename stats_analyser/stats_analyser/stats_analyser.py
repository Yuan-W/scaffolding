import sys
import json
from flask import Flask, g
import flaskext.couchdb
from easydict import EasyDict as edict

app = Flask(__name__)
app.config.from_object(__name__)

#create the view for average time according to the exercise_id
docs_by_exercise = flaskext.couchdb.ViewDefinition('docs','exercise_id','''\
    function(doc){
        emit(doc.exercise_id,doc.time_spent);
    }
  ''')

#create the view for docs related to the instructor 
docs_by_instructor = flaskext.couchdb.ViewDefinition('docs','instructor_id','''\
    function(doc){
        emit(doc.instructor_id,doc);
    }
  ''')

test_url = 'http://localhost:5984'
db_url = 'http://admin:ANfCd8PDW8QhNAWd@10.0.0.6:5984'

#configuration
app.config.update(
  DEBUG = True,
  COUCHDB_SERVER = test_url,
  COUCHDB_DATABASE = 'progress'
)
manager = flaskext.couchdb.CouchDBManager()
manager.setup(app)
manager.add_viewdef(docs_by_exercise)
manager.add_viewdef(docs_by_instructor)
manager.sync(app)

#return the docs
@app.route("/<exercise_id>/average")
def average(exercise_id):
  ave = 0;
  num = 0;
  for row in docs_by_exercise(g.couch)[int(exercise_id)]:
    row = edict(row.value)
    ave += row.time_spent
    num += 1
  if num != 0:
    return json.dumps(ave /(num * 1.0))
  else:
    return null

#return all the docs related to the instructor
@app.route("/<instructor_id>/docs")
def docs(instructor_id):
  response = dict()
  response['docs'] = []
  for row in docs_by_instructor(g.couch)[int(instructor_id)]:
    response['docs'].append(row.value)
  return json.dumps(response)

if __name__ == '__main__':
  app.run(debug=True, port=5005)