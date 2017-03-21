# Stats Analyser

## Installation

Modify `config.py`.

`pip install -r requirements.txt`

## RESTful Endpoints

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