RESTful APIs

# Public Server

Manage tests for exercises.

## Port

Port: 5000

## Installation

Modify `config.py` when needed.

Create `config.cfg`, it won't get committed to git, used to overwrite `config.py`.

`pip install -r requirements.txt`

`FLASK_APP=flask_public_server/flask_public_server/flask_public_server.py flask initdb`

`FLASK_APP=flask_public_server/flask_public_server/flask_public_server.py flask seeddb`

## RESTful Endpoints

### Get all exercises

| Title | Content |
--- | ---
URL | /api/exercises
Method Allowed | GET
Headers Required | access_token=\<token>,<br> Content-Type=application/json
Successful Response | Code: HTTP 200 OK, <br>Content: {<br>id : [string], <br>name : [string], <br>description: [string], <br>template: [string] <br>}
Error Responses | HTTP 401 Unauthorized, <br> HTTP 400 400 Bad Request

### Get stats for all exercises and students belong to an instructor

| Title | Content |
--- | ---
URL | /api/stats
Method Allowed | GET
Headers Required | access_token=\<token>,<br> Content-Type=application/json
Successful Response | Code: HTTP 200 OK, <br>Content: {<br>time\_spent : [integer], <br>student\_id : [integer], <br>average\_time\_spent : [integer] <br>}
Error Responses | HTTP 401 Unauthorized, <br> HTTP 400 400 Bad Request

### Post students stats and get hints

| Title | Content |
--- | ---
URL | /api/hints
Method Allowed | POST
Headers Required | access_token=\<token>,<br> Content-Type=application/json
Data Params |{<br>exercise\_id : [string], <br>time\_spent : [int], <br>code : [string], <br>hints\_number : [int]<br>}
Successful Response | Code: HTTP 200 OK, <br>Content: {<br>student\_id : [integer], <br>exercise\_id : [string], <br>hints : [string] <br>}
Error Responses | HTTP 401 Unauthorized, <br> HTTP 404 Not Found
