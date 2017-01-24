# -*- vsts scaffolding

from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "scaffolding_db"
mongo = PyMongo(app, config_prefix='MONGO')
APP_URL = "http://127.0.0.1:5000"


class Student(Resource):
    def get(self, username=None, studentID=None):
        data = []

        if username:
            studnet_info = mongo.db.student.find_one({"username": username}, {"_id": 0})
            if studnet_info:
                return jsonify({"status": "ok", "data": studnet_info})
            else:
                return {"response": "no student found for {}".format(username)}

        elif studentID:
            cursor = mongo.db.student.find({"studentID": studentID}, {"_id": 0}).limit(10)
            for student in cursor:
                student['url'] = APP_URL + url_for('students') + "/" + student.get('username')
                data.append(student)

            return jsonify({"studentID": studentID, "response": data})

        else:
            cursor = mongo.db.student.find({}, {"_id": 0, "update_time": 0}).limit(10)

            for student in cursor:
                print student
                student['url'] = APP_URL + url_for('students') + "/" + student.get('username')
                data.append(student)

            return jsonify({"response": data})

    def post(self):
        data = request.get_json()
        if not data:
            data = {"response": "ERROR"}
            return jsonify(data)
        else:
            username = data.get('username')
            #find username for student and if found then append
            if username:
                if mongo.db.student.find_one({"username": username}):
                    mongo.db.student.insert(data)
                else:
                    return {"response": "no student found for {}".format(username)}
            else:
                return {"response": "username number missing"}

        #this will be changed to get from the hints_provider
        return redirect(url_for("students"))

    def put(self, username):
        data = request.get_json()
        mongo.db.student.update({'username': username}, {'$set': data})
        return redirect(url_for("students"))

    def delete(self, username):
        mongo.db.student.remove({'username': username})
        return redirect(url_for("students"))


class Teacher(Resource):
    def get(self, username=None, teacherID=None):
        data = []

        if username:
            studnet_info = mongo.db.teacher.find_one({"username": username}, {"_id": 0})
            if studnet_info:
                return jsonify({"status": "ok", "data": studnet_info})
            else:
                return {"response": "no teacher found for {}".format(username)}

        elif teacherID:
            cursor = mongo.db.teacher.find({"teacherID": teacherID}, {"_id": 0}).limit(10)
            for teacher in cursor:
                teacher['url'] = APP_URL + url_for('teachers') + "/" + teacher.get('username')
                data.append(teacher)

            return jsonify({"teacherID": teacherID, "response": data})

        else:
            cursor = mongo.db.teacher.find({}, {"_id": 0, "update_time": 0}).limit(10)

            for teacher in cursor:
                print teacher
                teacher['url'] = APP_URL + url_for('teachers') + "/" + teacher.get('username')
                data.append(teacher)

            return jsonify({"response": data})

    def post(self):
        data = request.get_json()
        if not data:
            data = {"response": "ERROR"}
            return jsonify(data)
        else:
            username = data.get('username')
            #find username for teacher and if found then append
            if username:
                if mongo.db.teacher.find_one({"username": username}):
                    mongo.db.teacher.insert(data)
                else:
                    return {"response": "no teacher found for {}".format(username)}
            else:
                return {"response": "username number missing"}

        #this will be changed to get from the test_runner
        return redirect(url_for("teachers"))

    def put(self, username):
        data = request.get_json()
        mongo.db.teacher.update({'username': username}, {'$set': data})
        return redirect(url_for("teachers"))

    # to delete TA? TODO:: do we delete questions?
    def delete(self, username):
        mongo.db.teacher.remove({'username': username})
        return redirect(url_for("teachers"))


class Index(Resource):
    def get(self):
        return redirect(url_for("students"))

api = Api(app)
api.add_resource(Index, "/", endpoint="index")
api.add_resource(Student, "/api/hints", endpoint="students")
api.add_resource(Student, "/api/hints/<string:username>")
api.add_resource(Student, "/api/hints/studentID/<string:studentID>", endpoint="studentID")

api.add_resource(Teacher, "/api/tests", endpoint="teachers")
api.add_resource(Teacher, "/api/tests/<string:username>")
api.add_resource(Teacher, "/api/tests/teacherID/<string:teacherID>", endpoint="teacherID")

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0',port=5000) #run app on port 5000 in debug mode