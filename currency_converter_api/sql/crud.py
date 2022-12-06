from sqlalchemy.orm import Session

from . import models
from currency_converter_api.schemas import CreateUser, ReadUser


def get_user(db: Session, email: int):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: CreateUser):
    db_user = models.User(
        email=user.email,
        api_key=user.api_key,
        concurrency=user.concurrency,
        credits=user.credits,
        subscription=user.subscription,
        expiration=user.expiration
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user