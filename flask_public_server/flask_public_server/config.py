class Development(object):
  DEBUG = True
  MYSQL_DATABASE_USER = 'root'
  MYSQL_DATABASE_PASSWORD = 'password'
  MYSQL_DATABASE_DB = 'oauth'
  MYSQL_DATABASE_HOST = 'localhost'
  ADDRESS_STATS = 'http://localhost:5005/docs/'
  ADDRESS_HINTS= 'http://localhost:5001/hints'
  ADDRESS_TEST_MANAGEMENT= 'http://localhost:5003/testmanagement/'

class Testing(Development):
  TESTING = True
  MYSQL_DATABASE_USER = 'root'
  MYSQL_DATABASE_PASSWORD = ''
  MYSQL_DATABASE_DB = 'oauth'
  MYSQL_DATABASE_HOST = 'localhost'

class Production(object):
  DEBUG = False

