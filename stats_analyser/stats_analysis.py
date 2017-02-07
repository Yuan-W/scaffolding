from flask import Flask, request, session, g, redirect, url_for, abort, flash
from flask_restful import reqparse, Api, Resource, marshal_with, fields
from couchdb.design import ViewDefinition
from couchdb import Server
import flaskext.couchdb
import json

app = Flask(__name__)
app.config.from_object(__name__)

#create the view for CouchDB
docs_by_exercise = ViewDefinition('docs','by_exercise')

#return the docs
@app.route("/<exercise_id>/docs")
def docs(exercise_id):
  docs = []
  num = 0
  for row in docs_by_exercise(g.couch)[exercise_id]:
    docs.append(row.value)
  return json.dumps(docs)

'''
#init the database 
def connect_db():
  server = couchdb.Server(app.config['url'])
  return server.get_or_create_db(app.config['DATABASE'])

def init_db():
  """Create the views"""
  db = connect_db('stats')
  loader = couchdbkit.loader.FileSystemDocsLoader

@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = connect_db()
    Entry.set_db(g.db)
'''
resource_fields = {
    'exercise_id':  fields.Integer,
    'time_spent':   fields.Integer,
    'test_status':  fields.Raw
}

parser = reqparse.RequestParser()
parser.add_argument('exercise_id', type=int, location='json', required=True, help='exercise_id must exists and be a integer')
parser.add_argument('time_spent', type=int, location='json', required=True, help='time_spent must exists and be a integer')
parser.add_argument('test_status', location='json', required=True, help='test_status must exists')

class Stats(object):
  def __init__(self, student_id, exercise_id, time_spent, test_status):
    self.student_id = student_id
    self.exercise_id = exercise_id
    self.time_spent = time_spent
    self.test_status = test_status

class StatsAnalyser(Resource):
  @marshal_with(resource_fields)
  def post(self, exercise_id):
    args = parser.parse_args()
    return Stats(student_id, args['exercise_id'], args['time_spent'], args['test_status'])


api.add_resource(StatsAnalyser, '/<int:exercise_id>')

# @app.route('/get/<int:exercise_id>', methods=['GET'])
# def get_stats():

'''
Another method for getting the docs
server = Server('http://admin:couchdbpass@51.140.37.67:5984')
db = server['progress']
doc = db[args['exercise_id']]
---
view = ViewDefinition('tests', 'all', function(doc) {
  emit(doc._id, null);
})
view.get_doc(db)
# The view is not yet stored in the database, in fact, design doc doesn't
# even exist yet. That can be fixed using the `sync` method:
view.sync(db)
---
view = db.view('theview')
options = {
    'key': 'exercise_id',
    'include_docs': True
}
for row in view.iter(params=options):
    # emits only rows with the key 'exercise_id'
    # with each row's emitting document
'''
#configuration
if __name__ == '__main__':
    app.config.update(
      DEBUG = True,
      COUCHDB_SERVER = 'http://admin:couchdbpass@51.140.37.67:5984',
      COUCHDB_DATABASE = 'progress'
    )
    manager = flaskext.couchdb.CouchDBManager()
    manager.setup(app)
    manager.add_viewdef(docs_by_exercise)
    manager.sync(app)
    app.run(debug=True, port=5002)

