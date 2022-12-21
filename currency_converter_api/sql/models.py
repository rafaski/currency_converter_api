from sqlalchemy import Boolean, Column, Integer, String

from currency_converter_api.sql.database import Base


class User(Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, primary_key=True)
    api_key = Column(String, unique=True)
    concurrency = Column(Boolean, default=False)
    credits = Column(Integer)
    subscription = Column(String)
    expiration = Column(String)
