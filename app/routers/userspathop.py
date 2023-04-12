# Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

from fastapi import Body, FastAPI, Depends, HTTPException, status, APIRouter  # import library/framework
from pydantic import BaseModel  # classes inherit from base model
from datetime import date  # for default today's date insertion to date fields
from sqlalchemy.orm import Session
import pydanticmodels
import sqlalchmodels  
from dbsetup import get_db

router = APIRouter()

#user-related routes

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=pydanticmodels.CreateUser) #create new user
def create_new_user(user: pydanticmodels.CreateUser, db: Session = Depends(get_db)):
    #hashed_pw = pwd_context.hash(user.pw)
    #user.pw = hashed_pw
    new_user = sqlalchmodels.User(name=user.name, user_name=user.user_name, join_date=user.join_date, 
    pw=user.pw, email=user.email, zipcode=user.zipcode) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user) #flush
    return new_user

#@router.get("/users/{id}") 
@router.get("/users/{email}") #returns user searched for by email (unique)
def show_user(email: str, db: Session = Depends(get_db)): 
    user = db.query(sqlalchmodels.User).filter(sqlalchmodels.User.email == email).first()
    return user