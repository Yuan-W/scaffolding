class Development(object):
  DEBUG = True
  ADDRESS_STATS_UPDATER = 'http://localhost:5002'
  ADDRESS_TEST_RUNNER = 'http://localhost:5004'
  ADDRESS_TEST_MANAGEMENT = 'http://localhost:5003'

class Testing(Development):
  TESTING = True

class Production(object):
  DEBUG = False
  ADDRESS_STATS_UPDATER = 'http://localhost:5002'
  ADDRESS_TEST_RUNNER = 'http://localhost:5004'
  ADDRESS_TEST_MANAGEMENT = 'http://localhost:5003'
