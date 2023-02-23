import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

# TODO change to get this values from env
username = 'postgres'
password = 'root'
host = 'localhost'
port = 5432
DB_NAME = 'financial_db'

# username = os.environ["ALFRED_FINANCE_USER_NAME"]
# password = os.environ["ALFRED_FINANCE_PASSWORD"]
# host = os.environ["ALFRED_FINANCE_HOST"]
# port = os.environ["ALFRED_FINANCE_PORT"]
# DB_NAME = os.environ["ALFRED_FINANCE_DB_NAME"]

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


database_conector = DatabaseConector()
