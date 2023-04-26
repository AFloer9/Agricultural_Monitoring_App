# Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

from fastapi import Body, FastAPI, Depends, HTTPException, status, APIRouter, Request  # import library/framework
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel  # classes inherit from base model
from datetime import date  # for default today's date insertion to date fields
from sqlalchemy.orm import Session
import sqlalchmodels  
import pydanticmodels
from dbsetup import get_db
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, Template

router = APIRouter()

templates = Jinja2Templates(directory="./templates/") #create template object for HTML

#user-related routes
@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=pydanticmodels.CreateUser)
#@router.post("/users", status_code=status.HTTP_201_CREATED) #create new user
def create_new_user(user: pydanticmodels.CreateUser, db: Session = Depends(get_db)):

    #hashed_pw = pwd_context.hash(user.pw)
    #user.pw = hashed_pw
    new_user = sqlalchmodels.User(name=user.name, user_name=user.user_name, join_date=user.join_date, 
    pw=user.pw, email=user.email, zipcode=user.zipcode) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user) #flush
    return JSONResponse(new_user)

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
   return templates.TemplateResponse("login.html", {"request": request})

@router.get("/users/{email}") #returns user searched for by email (unique)
def show_user(email: str, db: Session = Depends(get_db)): 
    user = db.query(sqlalchmodels.User).filter(sqlalchmodels.User.email == email).first()
    return user

@router.get("/login")
def user_login():
    return {"data": "login"} 


