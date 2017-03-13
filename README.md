# Scaffolding

[![Build Status](https://travis-ci.com/Yuan-W/scaffolding.svg?token=wCDdC3iNXfe4K35sqGoj&branch=master)](https://travis-ci.com/Yuan-W/scaffolding)

# Services and Ports
| Service | Port | Url
--- | --- | ---
PublicServer | 5000 | 51.140.39.195
HintsProvider | 5001 | N/A
StatsAnalyser | 5005 | N/A
StatsUpdater | 5002 | N/A
TestManagement | 5003 | 10.0.1.7
TestRunner | 5004 | 10.0.1.7




# RESTful APIs
##PublicServer

###Get all stats belongs to an instructor

| Title | Content |
--- | ---
URL | /stats
Method Allowed | GET
Headers Required | access_token=\<token>,<br> Content-Type=application/json
Successful Response | Code: HTTP 200 OK, <br>Content: {<br>time\_spent : [integer], <br>student\_id : [integer], <br>average\_time\_spent : [integer] <br>}
Error Responses | HTTP 401 Unauthorized, <br> HTTP 404 Not Found

##HintsProvider

##StatsAnalyser
| Title | Content |
--- |---
URL | /docs/\<instructor_id\>
Method Allowed | GET
Successful Response| Code : HTTP 200 OK,<br> Content:\{all the docs related to the instructor and the exercise_id\}
Error Response| 

##StatsUpdater

| Title | Content |
--- | ---
URL | /stats/\<int:student_id\>/\<int:exercise_id\>
Method Allowed | POST
Headers Required | Content-Type=application/json
Data Params |{<br>instructor\_id : [int], <br>time\_spent : [int], <br>code : [string], <br>test\_status : [string], <br>hints\_number : [int]<br>}
Successful Response | Code: HTTP 201 Created, <br>Content: {<br>id : [string], <br>rev : [string]<br>}
Error Responses | HTTP 400 Bad Request

##TestManagement

##TestRunner

