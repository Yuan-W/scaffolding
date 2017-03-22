# Scaffolding

[![Build Status](https://travis-ci.com/Yuan-W/scaffolding.svg?token=wCDdC3iNXfe4K35sqGoj&branch=master)](https://travis-ci.com/Yuan-W/scaffolding)

# Installation
**Prerequisites**

`Python 2.7, PHP 7, Composer, Node.js, couchDB, docker, MySQL`

Follow the installation instruction in each app.


# Services and Ports

Service | Port
--- | --- 
PublicServer | 5000
HintsProvider | 5001
StatsAnalyser | 5005
StatsUpdater | 5002
ExerciseManager | 5003
TestRunner | 5004


# RESTful APIs
## PublicServer

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

## HintsProvider

### Post students stats and get hints

| Title | Content |
--- | ---
URL | /hints
Method Allowed | POST
Headers Required | Content-Type=application/json
Data Params |{<br>student\_id : [integer],<br>instructor\_id : [integer],<br>exercise\_id : [string], <br>time\_spent : [int], <br>code : [string], <br>hints\_number : [int]<br>}
Successful Response | Code: HTTP 200 OK, <br>Content: {<br>student\_id : [integer], <br>exercise\_id : [string], <br>hints : [string] <br>}
Error Responses | HTTP 401 Unauthorized, <br> HTTP 404 Not Found

## StatsAnalyser

### Get all stats for an instructor

| Title | Content |
--- |---
URL | /docs/\<instructor_id\>
Method Allowed | GET
Successful Response | Code : HTTP 200 OK,<br> Content: \{docs: [list], exercise: [list], exercise_stats:[list], student_stats: [list] \}
Error Response | None

### Get all stats for an exercise belongs to an instructor

| Title | Content |
--- |---
URL | /docs/\<instructor_id\>/\<exercise\_id\>
Method Allowed | GET
Successful Response | Code : HTTP 200 OK,<br> Content: \{docs: [list]\}
Error Response | None

### Get all stats for a student belongs to an instructor

| Title | Content |
--- |---
URL | /docs/\<instructor_id\>/\<student\_id\>
Method Allowed | GET
Successful Response | Code : HTTP 200 OK,<br> Content: \{docs: [list]\}
Error Response | None


### Get average time spent for an exercise

| Title | Content |
--- |---
URL | /average/\<exercise\_id\>
Method Allowed | GET
Successful Response | Code : HTTP 200 OK,<br> Content: \{average_time\_spent: [integer]\}
Error Response | None

## StatsUpdater

| Title | Content |
--- | ---
URL | /stats/\<int:student\_id\>/\<exercise\_id\>
Method Allowed | POST
Headers Required | Content-Type=application/json
Data Params |{<br>instructor\_id : [integer], <br>time\_spent : [integer], <br>code : [string], <br>test\_status : [string], <br>hints\_number : [integer]<br>}
Successful Response | Code: HTTP 201 Created, <br>Content: {<br>id : [string], <br>rev : [string]<br>}
Error Responses | HTTP 400 Bad Request

## ExerciseManager

### Get all exercises

| Title | Content |
--- | ---
URL | /exercises
Method Allowed | GET
Headers Required | Content-Type=application/json
Successful Response | Code: HTTP 200 OK, <br>Content: {<br>id : [string], <br>name : [string], <br>description: [string], <br>template: [string] <br>}
Error Responses |HTTP 400 400 Bad Request

### Get all exercises for an instructor

| Title | Content |
--- | ---
URL | /exercises/\<instructor\_id\>
Method Allowed | GET
Headers Required | Content-Type=application/json
Successful Response | Code: HTTP 200 OK, <br>Content: {<br>id : [string], <br>name : [string], <br>description: [string], <br>template: [string] <br>}
Error Responses |HTTP 400 400 Bad Request

### Get one exercise info

| Title | Content |
--- | ---
URL | /exercise/\<exercise\_id\>
Method Allowed | GET
Headers Required | Content-Type=application/json
Successful Response | Code: HTTP 200 OK, <br>Content: {<br>id : [string], <br>rev : [string], <br>instructor\_id : [integer], <br>name : [string], <br>test\_code : [string], <br>hints : [string], <br>description: [string], <br>template: [string] <br>}
Error Responses |HTTP 400 400 Bad Request

### Post new exercise

| Title | Content |
--- | ---
URL | /exercise/\<instructor\_id\>/\<exercise\_index\>
Method Allowed | POST
Headers Required | Content-Type=application/json
Data Params |{<br>name : [string], <br>test\_code : [string], <br>hints : [string], <br>description : [string], <br>template : [string]<br>}
Successful Response | Code: HTTP 201 Created, <br>Content: {<br>id : [string], <br>rev : [string]<br>}
Error Responses |HTTP 400 400 Bad Request

### Fetch exercise names

| Title | Content |
--- | ---
URL | /names
Method Allowed | POST
Headers Required | Content-Type=application/json
Data Params |{<br>ids : [list]<br>}
Successful Response | Code: HTTP 200 OK, <br>Content: {<br>id : [string], <br>name : [string]<br>}
Error Responses |HTTP 400 400 Bad Request


## TestRunner

| Title | Content |
--- | ---
URL | /test
Method Allowed | POST
Headers Required | Content-Type=application/json
Data Params |{<br>code : [string], <br>testCode : [string]<br>}
Successful Response | Code: HTTP 200 OK, <br>Content:<br>{ <br> &nbsp;&nbsp;&nbsp;&nbsp;results:{<br> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; failed:{<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;number:[integer],<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;tests:[list]<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;},<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;passed: { <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;number: [integer] <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}<br>&nbsp;&nbsp;&nbsp;&nbsp;},<br>&nbsp;&nbsp;&nbsp;&nbsp;errors:[string],<br>&nbsp;&nbsp;&nbsp;&nbsp;time: [string]<br>}
Error Responses |HTTP 400 400 Bad Request

