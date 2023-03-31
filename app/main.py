# main.py

from fastapi import Body, FastAPI, Depends, HTTPException, status  # import library/framework
from pydantic import BaseModel  # classes inherit from base model
from datetime import date  # for default today's date insertion to date fields
import sqlite3  # SQLite library
from sqlalchemy.orm import Session
import pydanticmodels
import sqlalchmodels  
from dbsetup import engine, get_db

sqlalchmodels.Base.metadata.drop_all(bind=engine) #tclears DB
sqlalchmodels.Base.metadata.create_all(bind=engine) #creates all tables according to SQLAlchemy models

from db_filler import fill_db  #uncomment for populating DB for demo

#populate table if desired (comment out if not):
fill_db() 

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"]) #hash algorithm type--only needed for user passowrd implementation


app = FastAPI()  # create instance of FastAPI named 'app'

#path operations:
# API server drills down thru request functions until it finds an HTTP request match:

# @decorator(wrapper--extends behavior of following function (i.e. show_root))    
# path operation/route URL (i.e. "/")   http method(i.e. GET) to endpoint

@app.get("/")   
def show_root():  # define function   ?async
    # displayed to user (gets converted to JSON) (key:value pair)
    return {"Welcome to ": "the Agricultural Monitoring Project"}
    #shows on webpage at path address

@app.get("/login")
def user_login():
    return {"data": "login"} 


@app.get("/myclimate") #for external API calls
def show_climatedata():
    return

######################################################################
#methods formatted as below are for Python-language DB queries using SQLAlchemy library:

@app.get("/my_plants")  # get inventory of plants owned (all listings)
def show_my_plants(db: Session = Depends(get_db)): #opens DB session for queries
    plants = db.query(sqlalchmodels.Plant).all()  # using SQLAlchemy query
    return {"data": plants}


@app.get("/seedvault") 
def show_seeds(db: Session = Depends(get_db)):  # dependency
    seeds = db.query(sqlalchmodels.Seed).all() 
    #print(seeds)  # print to terminal
    #return {"data": seeds}
    return {"data": seeds}

@app.get("/wishlist") 
def show_wishlist(db: Session = Depends(get_db)):  
    plants = db.query(sqlalchmodels.Plant).all()  
    #print(seeds)  # print to terminal
    return {"data": plants}


@app.get("/users") 
def show_users(db: Session = Depends(get_db)): 
    users = db.query(sqlalchmodels.User).all() 
    return {"data": users}


@app.get("/my_supplies") 
def show_supplies(db: Session = Depends(get_db)):  
    supplies = db.query(sqlalchmodels.Supply).all() 
    #print(seeds)  # print to terminal
    return {"data": supplies}

@app.get("/my_sensors")
def show_sensors(db: Session = Depends(get_db)):
    sensors = db.query(sqlalchmodels.Sensor).all()
    return {"data": sensors}

@app.get("/my_data")
def show_sensor_data(db: Session = Depends(get_db)):
    sensor_data = db.query(sqlalchmodels.SensorData).all()
    return {"data": sensor_data}


# id is a "path parameter"--always returned as a string!
@app.get("/seedvault/{id}") 
def get_seed(id: int, db: Session = Depends(get_db)):  
    seed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.id == id).first()  # using SQLAlchemy query
    #return seed
    print(id)
    return {"data": f"Seed: {id}"}

@app.delete("/seedvault/{id}", ) 
def delete_seed(id: int, db: Session = Depends(get_db)):  
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
    if new_seed.seed_type == None:
        return {"Please provide a seed type"}
    else:    
        db.add(new_seed)
        db.commit()
        db.refresh(new_seed) #flush
        return new_seed

@app.put("/seedvault/{id}", response_model=pydanticmodels.EditSeed) 
def edit_seed(id: int, db: Session = Depends(get_db)): 
    edseed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.id == id) # using SQLAlchemy query
    seed = edseed.first() 
    if seed == None:
        print("no seed by that ID")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    edseed.update({'seed_type': 'snapdragon', 'coll_loc': 'field', 'num_coll': '34'})
    db.commit()
    return seed

