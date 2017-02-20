## Test Management

Manage tests for exercises.

## Port

Port: 5003

### RESTful Endpoints

#### READ

`/exercises/:exercise_id/tests/` #GET

**Parameters**:

Key | Type
---- | ------
exercise_id | int

#### CREATE

`/exercises/:exercise_id/tests/` #POST

**Parameters**:

Key | Type
---- | ------
exercise_id | int
test_code | string

#### UPDATE

`exercises/:exercise_id/tests/` #PUT

**Parameters**:

Key | Type
---- | ------
exercise_id | int
test_code | string