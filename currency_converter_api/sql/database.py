from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional
from functools import wraps

from currency_converter_api.settings import DATABASE_URL


Base = declarative_base()

database = None


def init_db() -> None:
    """
    Initiate database
    """
    global database
    if database is not None:
        return
    database = Database(database_url=DATABASE_URL)
    database.create_session()


def database_operation(func):
    """
    Opens and closes database connection fo each db operation
    """
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
        """
        Creates an engine, provides a factory for Session objects and creates
        tables that do not already exists
        """
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
        """
        Closes Session connection and disposes engine
        """
        self.session.close_all()
        self.engine.dispose()
        self.session = None

