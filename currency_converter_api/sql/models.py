import sqlalchemy

from .database import metadata

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("api_key", sqlalchemy.String),
    sqlalchemy.Column("concurrency", sqlalchemy.Boolean),
    sqlalchemy.Column("credits", sqlalchemy.Integer),
    sqlalchemy.Column("subscription", sqlalchemy.String),
    sqlalchemy.Column("expiration", sqlalchemy.String)
)