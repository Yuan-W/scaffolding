class Development(object):
  DEBUG = True
  MYSQL_DATABASE_USER = 'root'
  MYSQL_DATABASE_PASSWORD = 'password'
  MYSQL_DATABASE_DB = 'oauth'
  MYSQL_DATABASE_HOST = 'localhost'
  ADDRESS_STATS = 'http://localhost:5005/stats/'
  ADDRESS_DOCS = 'http://localhost:5005/docs/'
  ADDRESS_HINTS = 'http://localhost:5001/hints'
  ADDRESS_TEST_MANAGEMENT = 'http://localhost:5003/testmanagement/'
  ADDRESS_AVERAGE = 'http://localhost:5005/average/'

class Testing(Development):
  TESTING = True
  MYSQL_DATABASE_USER = 'root'
  MYSQL_DATABASE_PASSWORD = ''
  MYSQL_DATABASE_DB = 'oauth'
  MYSQL_DATABASE_HOST = 'localhost'

class Production(object):
  DEBUG = False
  MYSQL_DATABASE_USER = 'b30fe6096c92ec'
  MYSQL_DATABASE_PASSWORD = '910a7d79'
  MYSQL_DATABASE_DB = 'oauthdb'
  MYSQL_DATABASE_HOST = 'eu-cdbr-azure-west-d.cloudapp.net'
  ADDRESS_STATS = 'http://10.0.1.5:5005/docs/'
  ADDRESS_HINTS= 'http://10.0.1.5:5001/hints'
  ADDRESS_TEST_MANAGEMENT= 'http://10.0.1.5:5003/'

