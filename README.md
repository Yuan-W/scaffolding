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

##StatsUpdater

##TestManagement

##TestRunner

