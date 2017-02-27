class Development(object):
  DEBUG = True
  STATS_DB_ADDRESS = 'http://localhost:5984/'
  EXERCISE_DB_ADDRESS = 'http://localhost:5984/'
  

class Testing(Development):
  TESTING = True

class Production(object):
  STATS_DB_ADDRESS= 'http://admin:ANfCd8PDW8QhNAWd@10.0.1.6:5894/'
  EXERCISE_DB_ADDRESS= 'http://admin:ANfCd8PDW8QhNAWd@10.0.1.6:5894/'
  DEBUG = False
