class Development(object):
  DEBUG = True
  COUCHDB_SERVER = 'http://localhost:5984/'
  COUCHDB_DATABASE = 'progress'
  

class Testing(Development):
  TESTING = True

class Production(object):
  STATS_DB_ADDRESS= 'http://admin:ANfCd8PDW8QhNAWd@10.0.1.6:5894/'
  DEBUG = False
  COUCHDB_SERVER = 'http://admin:ANfCd8PDW8QhNAWd@10.0.1.6:5894/'
  COUCHDB_DATABASE = 'progress'