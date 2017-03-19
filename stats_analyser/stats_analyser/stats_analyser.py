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

#create the view for average time according to the exercise_id
time_by_exercise = flaskext.couchdb.ViewDefinition('docs','exercise_id','''\
    function(doc){
        emit(doc.exercise_id,doc.time_spent);
    }
  ''')

docs_by_instructor_student = flaskext.couchdb.ViewDefinition('docs','instructor_student_id','''\
    function(doc){
        emit([doc.instructor_id, doc.student_id],doc);
    }
  ''')

#create the view for the specific instructor and specific exercise
docs_by_instructor_exercise = flaskext.couchdb.ViewDefinition('docs','instructor_exercise_id','''\
    function(doc){
        emit([doc.instructor_id,doc.exercise_id],doc);
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
manager.add_viewdef(docs_by_instructor_exercise)
manager.add_viewdef(docs_by_instructor_student)
manager.sync(app)


def get_stats(key, docs):
  stats = []

  exercise_time_dict = dict()
  hints_number_dict = dict()
  if key == 'exercise_id':
    student_count_dict = dict()
  if key == 'student_id':
    exercise_count_dict = dict()

  for doc in docs:
    if doc[key] not in exercise_time_dict:
      exercise_time_dict[doc[key]] = []
    exercise_time_dict[doc[key]].append(doc['time_spent'])

    if doc[key] not in hints_number_dict:
      hints_number_dict[doc[key]] = []
    hints_number_dict[doc[key]].append(doc['hints_number'])

    if key == 'exercise_id':
      if doc[key] not in student_count_dict:
        student_count_dict[doc[key]] = []
      student_count_dict[doc[key]].append(doc['student_id'])

    if key == 'student_id':
      if doc[key] not in exercise_count_dict:
        exercise_count_dict[doc[key]] = []
      exercise_count_dict[doc[key]].append(doc['exercise_id'])

  average_time = { key:sum(exercise_time_dict[key])/len(exercise_time_dict[key]) for key in exercise_time_dict } 
  
  average_hints = { key:sum(hints_number_dict[key])/len(hints_number_dict[key]) for key in hints_number_dict }
  if key == 'exercise_id':
    student_count = { key:len(set(student_count_dict[key])) for key in student_count_dict } 
  if key == 'student_id':
    exercise_count = { key:len(set(exercise_count_dict[key])) for key in exercise_count_dict } 

  for e_id in average_time:
    stat = { key: e_id, 'average_time_spent': average_time[e_id], 'average_hints':average_hints[e_id] }
    if key == 'exercise_id':
      stat['student_count'] = student_count[e_id]
    if key == 'student_id':
      stat['exercise_count'] = exercise_count[e_id]
    stats.append(stat)
  return stats

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
@app.route("/docs/<int:instructor_id>", methods=['GET'])
def docs(instructor_id):
  response = dict()

  rows = docs_by_instructor(g.couch)[int(instructor_id)]

  response['docs'] = [row.value for row in rows]

  response['exercise_stats'] = get_stats('exercise_id', response['docs'])
  response['student_stats'] = get_stats('student_id', response['docs'])
  response['exercise'] = [ stat['exercise_id'] for stat in response['exercise_stats'] ]
  
  return jsonify(response)

#return all the docs according to the exercise_id and instructor_id
@app.route("/docs/exercise/<int:instructor_id>/<exercise_id>", methods=['GET'])
def docs_exercise(instructor_id,exercise_id):
  mResponse = dict()
  mResponse['docs'] = []
  for row in docs_by_instructor_exercise(g.couch)[instructor_id,exercise_id]:
    mResponse['docs'].append(row.value)
  # mResponse['student_stats'] = get_stats('student_id', mResponse['docs'])
  # mResponse['exercise_stats'] = get_stats('exercise_id', mResponse['docs'])
  return jsonify(mResponse)

@app.route("/docs/student/<int:instructor_id>/<int:student_id>", methods=['GET'])
def docs_student(instructor_id,student_id):
  mResponse = dict()
  mResponse['docs'] = []
  for row in docs_by_instructor_student(g.couch)[instructor_id,student_id]:
    mResponse['docs'].append(row.value)
  # mResponse['student_stats'] = get_stats('student_id', mResponse['docs'])
  # mResponse['exercise_stats'] = get_stats('exercise_id', mResponse['docs'])
  return jsonify(mResponse)

if __name__ == '__main__':
  app.run(debug=True, port=5005)