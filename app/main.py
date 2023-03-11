# main.py

from fastapi import Body, FastAPI, Depends, HTTPException, status  # import library/framework
from pydantic import BaseModel  # classes inherit from base model
from datetime import date  # for default today's date insertion to date fields
import sqlite3  # SQLite library
from sqlalchemy.orm import Session
import pydanticmodels
import sqlalchmodels #for use with SQLAlchemy
#from sqlalchmodels import Seed
#from . import sqlalchmodels
#   from sqlalchmodels import User, Seed, Plant, Supply, Base
#from .dbsetup import engine, SessionLocal
from dbsetup import engine, get_db #for use with SQLAlchemy
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"]) #hash algorithm type
sqlalchmodels.Base.metadata.create_all(bind=engine) #creates all tables according to SQLAlchemy models

app = FastAPI()  # create instance of FastAPI named 'app'

#while True:  # until connected to DB   #for raw SQL
   
    #try:
        #db = sqlite3.connect(database='database.db', check_same_thread=False)  # connect to local database
        #cursor = db.cursor()  # cursor to execute SQL queries
        #print("connection to DB successful")
        #break
    #except Exception as error:
        #print("Error: ", error)


#path operations:
# API server drills down thru request functions until it finds an HTTP request match:

# @decorator(wrapper--extends behavior of following function (i.e. show_root))    
# path operation/route URL (i.e. "/")   http method(i.e. GET) to endpoint

#methods formatted as below are for testing HTTP queries BEFORE DB is contructed--change format, or delete once DB is in use
@app.get("/")   
def show_root():  # define function   ?async
    # displayed to user (gets converted to JSON) (key:value pair)
    return {"Welcome to ": "the Agricultural Monitoring Project"}
    #shows on webpage at path address

@app.get("/login")
def user_login():
    return {"data": "login"} 

# id is a "path parameter"--always returned as a string!
#@app.get("/seedvault/{id}")  # get individual seed type by ID
#def get_seed(id: int):
    #print(id)
    #return {"data": f"Seed: {id}"}

# revive later for sensor DB (stub):
# @app.get("/sensors")  #get list of all sensors
# def show_sensors():
#    return {"data": "sensors"}


######################################################################
#methods formatted as below are for Python-language DB queries using SQLAlchemy library:

@app.get("/my_plants")  # get inventory of plants owned (all listings)
def show_my_plants(db: Session = Depends(get_db)): #opens DB session for queries
    plants = db.query(sqlalchmodels.Plant).all()  # using SQLAlchemy query
    return {"data": plants}


@app.get("/seedvault")  #USE WITH SQLAlchemy
def show_seeds(db: Session = Depends(get_db)):  # dependency
    seeds = db.query(sqlalchmodels.Seed).all()  # using SQLAlchemy query
    #print(seeds)  # print to terminal
    return {"data": seeds}

@app.get("/wishlist")  #USE WITH SQLAlchemy
def show_wishlist(db: Session = Depends(get_db)):  # dependency
    plants = db.query(sqlalchmodels.Plant).all()  # using SQLAlchemy query
    #print(seeds)  # print to terminal
    return {"data": plants}


@app.get("/users")  #USE WITH SQLAlchemy
def show_users(db: Session = Depends(get_db)):  # dependency
    users = db.query(sqlalchmodels.User).all()  # using SQLAlchemy query
    return {"data": users}


@app.get("/my_supplies")  #USE WITH SQLAlchemy
def show_users(db: Session = Depends(get_db)):  # dependency
    supplies = db.query(sqlalchmodels.Supply).all()  # using SQLAlchemy query
    #print(seeds)  # print to terminal
    return {"data": supplies}

@app.get("/seedvault/{id}")  #USE WITH SQLAlchemy
def get_seed(id: int, db: Session = Depends(get_db)):  # dependency
    seed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.id == id).first()  # using SQLAlchemy query
    return seed

@app.delete("/seedvault/{id}", )  #USE WITH SQLAlchemy
def delete_seed(id: int, db: Session = Depends(get_db)):  # dependency
    delseed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.id == id)  # using SQLAlchemy query
    seed = delseed.first() 
    if seed == None:
        print("no seed by that ID")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(seed)
    db.commit()
    return {"seed deleted"}

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=pydanticmodels.CreateUser)
def create_new_user(user: pydanticmodels.CreateUser, db: Session = Depends(get_db)):
    hashed_pw = pwd_context.hash(user.pw)
    user.pw = hashed_pw
    new_user = sqlalchmodels.User(uid=user.uid, name=user.name, user_name=user.user_name, join_date=user.join_date, 
    pw=user.pw, email=user.email, zipcode=user.zipcode) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user) #flush
    return new_user
    
@app.post("/seedvault", status_code=status.HTTP_201_CREATED, response_model=pydanticmodels.CreateSeed)
def create_new_seed(seed: pydanticmodels.CreateSeed, db: Session = Depends(get_db)):
    new_seed = sqlalchmodels.Seed(id=seed.id, seed_type=seed.seed_type, coll_loc = seed.coll_loc, 
    coll_date = seed.coll_date, num_coll = seed.num_coll)
    db.add(new_seed)
    db.commit()
    db.refresh(new_seed) #flush
    return new_seed

@app.put("/seedvault/{id}", response_model=pydanticmodels.EditSeed)  #USE WITH SQLAlchemy
def edit_seed(id: int, db: Session = Depends(get_db)):  # dependency
    edseed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.id == id) # using SQLAlchemy query
    seed = edseed.first() 
    if seed == None:
        print("no seed by that ID")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    edseed.update({'seed_type': 'snapdragon', 'coll_loc': 'field', 'num_coll': '34'})
    db.commit()
    return seed




