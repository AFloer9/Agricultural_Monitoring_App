# Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

from fastapi import Body, FastAPI, Depends, HTTPException, status, Request, APIRouter  # import library/framework
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # classes inherit from base model
from datetime import date  # for default today's date insertion to date fields
from sqlalchemy.orm import Session
import sqlalchmodels
import templates
from dbsetup import engine
from routers import sensorpathop, userspathop, gardenpathop, sensorpathop2
from jinja2 import Environment, FileSystemLoader
import uvicorn


#sqlalchmodels.Base.metadata.drop_all(bind=engine) #tclears DB upon restarting main--COMMENT OUT FOR PERSISTENT DB
sqlalchmodels.Base.metadata.create_all(bind=engine) #creates all tables according to SQLAlchemy models--

#from db_filler import fill_db  #uncomment for populating DB for demo

#populate table if desired (comment out if not):
#fill_db() 

#from passlib.context import CryptContext  #stub for user password implementation
#pwd_context = CryptContext(schemes=["bcrypt"]) #hash algorithm type--only needed for user passowrd implementation


app = FastAPI()  # create instance of FastAPI named 'app'


#allowed domains:
origins = [
    "http://localhost",
    "http://localhost:5500",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#app.mount('/', StaticFiles(directory="./templates"), name="templates")

templates = Jinja2Templates(directory="./templates") #create template object for HTML


app.include_router(gardenpathop.router) #router object--directs API to routes in other .py files
app.include_router(userspathop.router)
app.include_router(sensorpathop.router)
app.include_router(sensorpathop2.router)
  
if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)