import sys
import os
import json
from flask import Flask, g,jsonify,request
import flaskext.couchdb
from easydict import EasyDict as edict
from config import Development, Production, Testing

config = {
    "production": Production,
    "testing": Testing,
    "development": Development,
    "default": Development
}

app = Flask(__name__)
config_name = os.getenv('FLASK_CONFIGURATION', 'default')
app.config.from_object(config[config_name])

#create the view for the specific instructor and specific exercise
docs_by_exercise = flaskext.couchdb.ViewDefinition('docs','instructor_exercise_id','''\
    function(doc){
        emit([doc.instructor_id,doc.exercise_id],doc);
    }
  ''')

#create the view for average time according to the exercise_id
time_by_exercise = flaskext.couchdb.ViewDefinition('docs','exercise_id','''\
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

manager = flaskext.couchdb.CouchDBManager()
manager.setup(app)
manager.add_viewdef(time_by_exercise)
manager.add_viewdef(docs_by_instructor)
manager.add_viewdef(docs_by_exercise)
manager.sync(app)

#return the docs
@app.route("/average/<exercise_id>")
def average(exercise_id):
  ave = 0;
  num = 0;
  for row in time_by_exercise(g.couch)[int(exercise_id)]:
    ave += row.value
    num += 1
  if num != 0:
    ave_response = dict()
    ave_response['average_time_spent'] = ave /(num * 1.0)
    return jsonify(ave_response)
  else:
    return null

#return all the docs related to the instructor
@app.route("/docs/<int:instructor_id>")
def docs(instructor_id):
  response = dict()
  response['docs'] = []
  response['exercise'] = []
  for row in docs_by_instructor(g.couch)[int(instructor_id)]:
    response['docs'].append(row.value)
    if row.value['exercise_id'] not in response['exercise']:
      response['exercise'].append(row.value['exercise_id'])
    response['exercise'].sort()
  return jsonify(response)

#return all the docs according to the exercise_id and instructor_id
@app.route("/newdocs/<int:instructor_id>/<int:exercise_id>")
def newdocs(instructor_id,exercise_id):
  mResponse = dict()
  mResponse['docs'] = []
  for row in docs_by_exercise(g.couch)[int(instructor_id),int(exercise_id)]:
    mResponse['docs'].append(row.value)
  return jsonify(mResponse)

if __name__ == '__main__':
  app.run(debug=True, port=5005)