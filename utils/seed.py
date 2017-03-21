#!/usr/bin/env python

import sys
import requests
import random

ADDRESS_HINTS = 'http://localhost:5001'
ADDRESS_EXERCISE = 'http://localhost:5003'


TEST_CODE = 'def test_reverse_list():\n\tassert reverse_list([1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1]'
HINTS = '>>> L = [0,1,2,3]\n>>> L[::-1]\n[3, 2, 1, 0]'

CODE = "def reverse_list(l):\n\treturn l[::-1]"

def new_stats(student_id, instructor_id, exercise_id, code, time_spent, hints_number):
  url = '%s/hints' % ADDRESS_HINTS
  content = {'student_id':student_id, 'instructor_id':instructor_id, 
              'exercise_id':exercise_id, 'code':code,
              'time_spent':time_spent, 'hints_number':hints_number
              }
  response = requests.post(url, json=content, headers={'Content-Type': 'application/json'})
  return response

def new_student(s_id, name, pass_raw, instructor):
  sql = 'INSERT INTO users VALUES (%d, "%s", "%s", "%s");' % (s_id, name, pass_raw, instructor)
  return sql


def new_exercse(instructor_id, exercise_index, name, test_code, hints, description):
  url = '%s/exercise/%d/%d' % (ADDRESS_EXERCISE, instructor_id, exercise_index)
  content = {'name':name, 'test_code':test_code, 'hints':hints, 'description':description}
  response = requests.post(url, json=content, headers={'Content-Type': 'application/json'})

  return response

def create_exercises(instructor_id, total=4):
  ids = []
  for i in range(1, total+1):
    exercise_index = i
    name = 'Exercise %d' % i
    test_code = TEST_CODE
    hints = HINTS
    description = 'description for %s' % name
    response = new_exercse(instructor_id, exercise_index, name, test_code, hints, description)
    ids.append('%d_%d' % (instructor_id, exercise_index))
    # print response.json
  return ids

def create_students(instructor_id):
  pass_raw = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'
  instructor = 'tester'
  students = ['alice.test', 'bob.test', 'charlie.test']
  ids = []
  for i, student in enumerate(students):
    print new_student(i+111, student, pass_raw, instructor)
    ids.append(i+111)
  return ids

def main(instructor_id):
  exercise_ids = create_exercises(instructor_id)
  student_ids = create_students(instructor_id)
  for e_id in exercise_ids:
    for s_id in student_ids:
      time_spent = random.randint(300, 900)
      hints_number = random.randint(1, 10) 
      print new_stats(s_id, instructor_id, e_id, CODE, time_spent, hints_number)

if __name__ == '__main__':
  instructor_id = int(sys.argv[1])
  main(instructor_id)