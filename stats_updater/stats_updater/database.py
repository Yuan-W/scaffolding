from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

engine = create_engine('mssql+pyodbc://scaffolding:gs02Scaff@scaffolding-sql.database.windows.net:1433/VSTS_SQL_1?driver=ODBC+Driver+13+for+SQL+Server')

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import yourapplication.models
    Base.metadata.create_all(bind=engine)