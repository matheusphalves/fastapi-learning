from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

username = 'postgres'
password = 'root'
host = 'localhost'
port = 5432
DB_NAME = 'financial_db'

DATABASE_URL = f"postgresql://{username}:{password}@{host}/{DB_NAME}"
Base = declarative_base()
class DatabaseConector:
    engine = None

    def create_engine(self, connect_args={}):
        try:
            self.engine = create_engine(DATABASE_URL, connect_args=connect_args)
            if not database_exists(self.engine.url):
                create_database(self.engine.url)
            Base.metadata.create_all(bind=self.engine)
        except Exception as e:
            print("Failed on create_engine: " + str(e))

    def get_database_session(self, autoflush=False):

        SessionLocal = sessionmaker(autoflush=autoflush, bind=self.engine)

        database = SessionLocal()
        try:
            yield database
        finally:
            database.close()


database = DatabaseConector()

engine = database.create_engine()
