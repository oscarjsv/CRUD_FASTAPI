from typing import List

from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from auth import AuthHandler
from schemas import AuthDetails
from celery_worker import create_order

import crud
import models
import schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

auth_handler = AuthHandler()
app = FastAPI()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


users = []


@app.post('/register', status_code=201)
def register(auth_details: AuthDetails):
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'password': hashed_password
    })
    return


@app.post('/login')
def login(auth_details: AuthDetails):
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break

    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(
            status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return {'token': token}


@app.post("/api/users", response_model=schemas.User_Base)
def create_user(user: schemas.User_Base, db: Session = Depends(get_db),
                username=Depends(auth_handler.auth_wrapper)):
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="already registered")
    return crud.create_user(db=db, user=user)


@app.put('/api/dogs/{name}', response_model=schemas.User_Base)
def update_user(name: str, db: Session = Depends(get_db)):
    pass


@app.get("/api/users", response_model=List[schemas.User_Base])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/api/users/{user_id}", response_model=schemas.User_Base)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


"""@app.delete('/api/users/{name}', response_model=schemas.User_Base)
def delete_users(name: str, db: Session = Depends(get_db)):
    return crud.delete_users(db=db, name=name)
"""


@app.post("/api/dogs/{user_id}", response_model=schemas.Dogs_Base)
def create_item_for_Dogs(
        id_user: int, dogs: schemas.Dogs_Base,
        db: Session = Depends(get_db)):
    dogs_id = crud.create_user_Dogs(db=db, dogs=dogs, id_user=id_user)
    task = create_order.delay(id_user)
    print(task)

    return dogs_id


@app.get("/api/dogs/", response_model=List[schemas.Dogs_Base])
def read_Dogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dogs = crud.get_Dogs(db, skip=skip, limit=limit)
    return dogs


@app.get('/api/dogs/{name}', response_model=List[schemas.Dogs_Base])
def get_dogs_names(name: str, db: Session = Depends(get_db)):
    db_dogs = crud.get_dogs_by_name(db, name=name)
    if db_dogs is None:
        raise HTTPException(status_code=404, detail="Dogs not found")
    return db_dogs


@app.get('/api/dogs/is_adopted', response_model=List[schemas.Dogs_Base])
def dogs_is_adopted(db: Session = Depends(get_db), ):
    return crud.get_dogs_is_adopted(db)


@app.delete('/api/dogs/{name}', response_model=schemas.Dogs_Base)
def delete_users_dogs(name: str, db: Session = Depends(get_db)):
    return crud.delete_Dog(db, name=name)


@app.put("/api/dogs/{name}", response_model=schemas.Dogs_Base)
def update_dog(name: str, dogs: schemas.Dogs_Base, db: Session = Depends(get_db)):
    """update and return TODO for given id"""
    dogs = crud.update_Dogs(db, name)
    updated_dogss = crud.update_Dogs(db, name=name,  dogs=dogs)
    return updated_dogss
