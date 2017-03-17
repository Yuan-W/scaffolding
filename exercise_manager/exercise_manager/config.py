class Development(object):
  DEBUG = True
  EXERCISE_DB_ADDRESS = 'http://localhost:5984/'
  

class Testing(Development):
  TESTING = True

class Production(object):
  EXERCISE_DB_ADDRESS= 'http://admin:ANfCd8PDW8QhNAWd@10.0.1.6:5984/'
  DEBUG = False
