# Exercise Manager

Manage tests for exercises.

## Port

Port: 5003

## Installation

Modify `config.py`.

`pip install -r requirements.txt`

`FLASK_APP=exercise_manager/exercise_manager/exercise_manager.py flask initdb`

## RESTful Endpoints

#### Get all exercises

| Title | Content |
--- | ---
URL | /exercises
Method Allowed | GET
Headers Required | Content-Type=application/json
Successful Response | Code: HTTP 200 OK, <br>Content: {<br>id : [string], <br>name : [string], <br>description: [string], <br>template: [string] <br>}
Error Responses |HTTP 400 400 Bad Request

#### Get all exercises for an instructor

| Title | Content |
--- | ---
URL | /exercises/\<instructor\_id\>
Method Allowed | GET
Headers Required | Content-Type=application/json
Successful Response | Code: HTTP 200 OK, <br>Content: {<br>id : [string], <br>name : [string], <br>description: [string], <br>template: [string] <br>}
Error Responses |HTTP 400 400 Bad Request

#### Get one exercise info

| Title | Content |
--- | ---
URL | /exercise/\<exercise\_id\>
Method Allowed | GET
Headers Required | Content-Type=application/json
Successful Response | Code: HTTP 200 OK, <br>Content: {<br>id : [string], <br>rev : [string], <br>instructor\_id : [integer], <br>name : [string], <br>test\_code : [string], <br>hints : [string], <br>description: [string], <br>template: [string] <br>}
Error Responses |HTTP 400 400 Bad Request

#### Post new exercise

| Title | Content |
--- | ---
URL | /exercise/\<instructor\_id\>/\<exercise\_index\>
Method Allowed | POST
Headers Required | Content-Type=application/json
Data Params |{<br>name : [string], <br>test\_code : [string], <br>hints : [string], <br>description : [string], <br>template : [string]<br>}
Successful Response | Code: HTTP 201 Created, <br>Content: {<br>id : [string], <br>rev : [string]<br>}
Error Responses |HTTP 400 400 Bad Request

#### Fetch exercise names

| Title | Content |
--- | ---
URL | /names
Method Allowed | POST
Headers Required | Content-Type=application/json
Data Params |{<br>ids : [list]<br>}
Successful Response | Code: HTTP 200 OK, <br>Content: {<br>id : [string], <br>name : [string]<br>}
Error Responses |HTTP 400 400 Bad Request