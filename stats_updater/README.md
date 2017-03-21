# Stats Updater

## Installation

Modify `config.py`.

`pip install -r requirements.txt`

`FLASK_APP=stats_updater/stats_updater/stats_updater.py flask initdb`

## RESTful Endpoints

### Post new stat

| Title | Content |
--- | ---
URL | /stats/\<int:student\_id\>/\<exercise\_id\>
Method Allowed | POST
Headers Required | Content-Type=application/json
Data Params |{<br>instructor\_id : [integer], <br>time\_spent : [integer], <br>code : [string], <br>test\_status : [string], <br>hints\_number : [integer]<br>}
Successful Response | Code: HTTP 201 Created, <br>Content: {<br>id : [string], <br>rev : [string]<br>}
Error Responses | HTTP 400 Bad Request