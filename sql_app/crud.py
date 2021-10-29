from sqlalchemy.orm import Session
from database import Base
from models import User, Dog
import schemas
import requests


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.User):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_users(db: Session, name: str):
    return db.query(User).filter(User.name == name,).delete()


def get_Dogs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Dog).offset(skip).limit(limit).all()


def get_dogs_by_name(db: Session, name: str):
    return db.query(Dog).filter(Dog.name == name).first()


def get_dogs_is_adopted(db: Session):
    return db.query(Dog).filter(Dog.is_adopted == True).all()


def create_user_Dogs(db: Session, dogs: schemas.Dogs_Base, id_user: int):
    db_item = Dog(**dogs.dict(), id_user=id_user)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
