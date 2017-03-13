class Development(object):
  DEBUG = True
  ADDRESS_STATS_UPDATER = 'http://localhost:5002'
  ADDRESS_TEST_RUNNER = 'http://localhost:5004'
  ADDRESS_TEST_MANAGEMENT = 'http://localhost:5003'
  ADDRESS_HINTS_DB = 'http://localhost:5984'

class Testing(Development):
  TESTING = True

class Production(object):
  DEBUG = False
  ADDRESS_STATS_UPDATER = 'http://localhost:5002'
  ADDRESS_TEST_RUNNER = 'http://localhost:5004'
  ADDRESS_TEST_MANAGEMENT = 'http://localhost:5003'
  ADDRESS_HINTS_DB = 'http://admin:ANfCd8PDW8QhNAWd@10.0.1.6:5984/'
