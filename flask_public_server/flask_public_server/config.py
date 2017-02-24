class Development(object):
  DEBUG = True
  MYSQL_DATABASE_USER = 'root'
  MYSQL_DATABASE_PASSWORD = 'password'
  MYSQL_DATABASE_DB = 'oauth'
  MYSQL_DATABASE_HOST = 'localhost'
  ADDRESS_STATS = 'http://localhost:5005/stats/'
  ADDRESS_HINTS= 'http://localhost:5001/hints'

class Testing(Development):
  TESTING = True
  MYSQL_DATABASE_USER = 'travis'
  MYSQL_DATABASE_PASSWORD = ''
  MYSQL_DATABASE_DB = 'oauth'
  MYSQL_DATABASE_HOST = 'localhost'

class Production(object):
  DEBUG = False
