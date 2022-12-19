from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional
from functools import wraps

DATABASE_URL = "sqlite:///./sql_app.db"

Base = declarative_base()

database = None


def init_db() -> None:
    global database
    if database is not None:
        return
    database = Database(database_url=DATABASE_URL)
    database.create_session()


def database_operation(func):
    @wraps(func)
    def _database_operation(*args, **kwargs):
        if database is None:
            init_db()
        open_connection = database.session()
        try:
            return func(open_connection, *args, **kwargs)
        except Exception as e:
            print(e)
            open_connection.rollback()
            raise
        finally:
            open_connection.close()
    return _database_operation


class Database:
    session: Optional[sessionmaker] = None
    engine = None

    def __init__(self, database_url: str):
        self.database_url = database_url

    def create_session(self):
        self.engine = create_engine(
            DATABASE_URL, connect_args={"check_same_thread": False}
        )
        self.session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        # Create all tables that do not already exist
        Base.metadata.create_all(self.engine)

    def dispose_session(self):
        self.session.close_all()
        self.engine.dispose()
        self.session = None

