class Development(object):
  DEBUG = True
  ADDRESS_STATS_UPDATER = 'http://localhost:5002'

class Testing(Development):
  TESTING = True

class Production(object):
  DEBUG = False
  ADDRESS_STATS_UPDATER = 'http://10.0.1.5:5002'
