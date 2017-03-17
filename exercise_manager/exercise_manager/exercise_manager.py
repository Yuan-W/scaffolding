import os
from flask import Flask, request, abort, make_response, jsonify
from config import Development, Production, Testing
from exercise_db_handler import ExerciseDBHandler

config = {
    "production": Production,
    "testing": Testing,
    "development": Development,
    "default": Development
}

app = Flask(__name__)

config_name = os.getenv('FLASK_CONFIGURATION', 'default')
app.config.from_object(config[config_name])
# app.config.from_pyfile('../config.cfg')

exercise_db_url = app.config['EXERCISE_DB_ADDRESS']
exercise_handler = ExerciseDBHandler(exercise_db_url)

# ExerciseManager
# Manage tests, retrieve tests for exercise, create tests for exercises, update tests for exercise
@app.route('/exercises', methods=['GET'])
def get_all_exercises():
    response = exercise_handler.get_all()
    if response[1] != 200:
        return response[0], response[1]

    exercises = response[0]
    json_response = []
    for exercise in exercises:
        ex_json = {'id':exercise['_id'],'name':exercise['name']}
        if 'description' in exercise:
            ex_json['description'] = exercise['description']
        if 'template' in exercise:
            ex_json['template'] = exercise['template']
        json_response.append(ex_json)

    return jsonify(json_response)

@app.route('/exercise/<doc_id>', methods=['GET'])
def get_exercise(doc_id):
    doc_id = doc_id
    response = exercise_handler.get_exercise(doc_id)
    if response[1] != 200:
        return response[0], response[1]
    exercise = response[0]

    json_response = {'id':exercise['_id'],
                     'rev':exercise['_rev'],
                     'instructor_id':exercise['instructor_id'],
                     'name':exercise['name'],
                     'test_code':exercise['test_code'],
                     'hints':exercise['hints']
                    }
    if 'description' in exercise:
        json_response['description'] = exercise['description']
    if 'template' in exercise:
        json_response['template'] = exercise['template']

    return jsonify(json_response)

@app.route('/exercise/<int:instructor_id>/<int:exercise_index>', methods=['POST'])
def post_exercise(instructor_id, exercise_index):
    request_data = request.json

    if 'name' not in request_data:
        abort(make_response(jsonify(message="name must exists"), 400))
    if 'test_code' not in request_data:
        abort(make_response(jsonify(message="test_code must exists"), 400))
    if 'hints' not in request_data:
        abort(make_response(jsonify(message="hints must exists"), 400))

    name = request_data['name']
    test_code = request_data['test_code']
    hints = request_data['hints']
    description = None
    template = None
    if 'description' in request_data:
        description = request_data['description']
    if 'template' in request_data:
        template = request_data['template']

    response = exercise_handler.post_exercise(instructor_id, exercise_index, name, test_code, hints, description, template)
    return jsonify(response[0]), response[1]

@app.route('/names', methods=['POST'])
def fetch_names():
    request_data = request.json
    if 'ids' not in request_data:
        abort(make_response(jsonify(message="ids must exists"), 400))
    if not isinstance(request_data['ids'], list):
        abort(make_response(jsonify(message="ids must be a list"), 400))
    response = exercise_handler.bulk_fetch(request_data['ids'])
    if response[1] != 200:
        return jsonify(response[0], response[1])
    names = response[0]['rows']
    names = [ {'id':e['doc']['_id'], 'name':e['doc']['name']} for e in names ]
    return jsonify(names)

########################
# Additional Commands
########################

@app.cli.command('initdb')
def init_db():
    response = exercise_handler.init_db()
    if response[1] == 201:
        print('Database exercise initialised')
    else:
        print(response)

@app.cli.command('cleardb')
def cleardb():
    exercise_handler.cleardb()
    print('Database exercise cleared')


if __name__ == '__main__':
    app.run(debug=True, port=5003)