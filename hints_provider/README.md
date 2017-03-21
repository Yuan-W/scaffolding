## Hints Provider

Return hints based on the input.

## Port

Port: 5001


## Installation

Modify `config.py` when needed.

`pip install -r requirements.txt`

## RESTful Endpoints

### Post students stats and get hints

| Title | Content |
--- | ---
URL | /hints
Method Allowed | POST
Headers Required | Content-Type=application/json
Data Params |{<br>student\_id : [integer],<br>instructor\_id : [integer],<br>exercise\_id : [string], <br>time\_spent : [int], <br>code : [string], <br>hints\_number : [int]<br>}
Successful Response | Code: HTTP 200 OK, <br>Content: {<br>student\_id : [integer], <br>exercise\_id : [string], <br>hints : [string] <br>}
Error Responses | HTTP 401 Unauthorized, <br> HTTP 404 Not Found