# main.py

from fastapi import Body, FastAPI, Depends  # import library/framework
from pydantic import BaseModel  # classes inherit from base model
from datetime import date  # for default today's date insertion to date fields
# for random id num assignation (pre-database) #DEBUG
from random import randrange
import sqlite3  # SQLite library
from sqlalchemy.orm import Session
import sqlalchmodels
#from .dbsetup import engine, SessionLocal
from dbsetup import engine, SessionLocal

sqlalchmodels.Base.metadata.create_all(bind=engine)

app = FastAPI()  # create instance of FastAPI named 'app'

# Dependency--don't start session unless connected


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(BaseModel):  # extends class Base--allows auto-validation of user input adherence to format--Seed inherits from Pydantic model
    id: int  # unique ID number for database
    name: str
    user_name: str
    join_date: str = date.today()  # default = current date
    pw: str
    email: str
    zipcode: int


class Seed(BaseModel):  # extends class Basemodel--allows auto-validation of user input adherence to format--Seed inherits from Pydantic model
    id: int
    seed_type: str
    coll_loc: str
    coll_date: str = date.today()  # default = current date
    num_seeds: int = "1"  # default = 1 seed


class Plant(BaseModel):  # extends class Basemodel--allows auto-validation of user input adherence to format--Seed inherits from Pydantic model
    id: int
    plant_type: str
    sci_name: str
    date_acq: str = date.today()  # default = current date
    num_plants: int = "1"  # default = 1 plant
    watering_week: int
    sunlight_hrs_day: int


class Supply(BaseModel):  # extends class Basemodel--allows auto-validation of user input adherence to format--Seed inherits from Pydantic model
    id: int
    supply_type: str
    brand_name: str
    purch_acq: str = date.today()  # default = current date
    num_supply: int = "1"  # default = 1 item/container
    amt: int = "1"  # default = 1 unit
    unit: str = "lbs."  # default = pounds; could be ounces, etc.


while True:  # until connected to DB   #
    # connect to local database:
    try:
        db = sqlite3.connect(database='database.db', check_same_thread=False)
        cursor = db.cursor()  # cursor to execute SQL queries
        print("connection successful")
        break
    except Exception as error:
        print("Error: ", error)


# hardcoded for http post requests/database "seeding"  [list{dict}] for testing--normally this would come from database:  #DEBUG
user = [{"uid": 1, "name": "Jon Snow", "pw": "winteriscoming",
         "email": "jonsnow@gmail.com", "zipcode": 51031}]

my_seeds = [{"id": 10, "seed_type": "daisy", "coll_loc": "backyard"}, {
    "id": 2, "seed_type": "zinnia", "coll_loc": "field"}]

my_plants = [{"id": 20, "plant_type": "maple", "sci_name": "Acer"}]

my_supplies = [
    {"id": 30, "supply_type": "fertilizer", "brand_name": "MiracleGro"}]

wishlist = [{"id": 40, "plant_type": "", "sci_name": "Acer"}]

# print class which object belongs to (for testing type/curiosity):    #DEBUG
# print(type(my_seeds))


# API drills down thru request functions until it finds a request match:

# decorator(wrapper--extends behavior of following function (i.e. show_root))    path operation/route URL (i.e. "/")   http method(i.e. GET) to endpoint

@app.get("/")
def show_root():  # define function   ?async
    # displayed to user (gets converted to JSON) (key:value pair)
    return {"Welcome to ": "the Agricultural Monitoring Project"}


@app.get("/sqlalchemy")  # *******this one works!*****
def test_seeds(db: Session = Depends(get_db)):  # dependency
    seeds = db.query(sqlalchmodels.Seed).all()  # using SQLAlchemy query
    print(seeds)  # print to terminal
    return {"data": seeds}


@app.get("/login")
def user_login():
    return {"data": "login"}


@app.get("/seedvault")  # get inventory of seeds collected (all listings)
def show_seedvault():
    seeds = cursor.execute("""SELECT * FROM seedvault""")  # using SQL query
    # cursor.execute("""SELECT * FROM seedvault""")  # using SQL query
    # print(seeds)
    return {"data": seeds}


@app.get("/my_plants")  # get inventory of plants owned (all listings)
def show_my_plants(db: Session = Depends(get_db)):
    plants = db.query(sqlalchmodels.Plant).all()  # using SQLAlchemy query
    return {"data": plants}


@app.get("/wishlist")  # get entire plant wishlist (all listings)
def show_wishlist():
    return {"data": wishlist}


@app.get("/my_supplies")  # get supply inventory (all listings)
def show_supplies():
    return {"data": my_supplies}

# revive later for sensor DB (stub):
# @app.get("/sensors")  #get list of all sensors
# def show_sensors():
#    return {"data": "sensors"}


@app.post("/seedvault")  # post -- add new seed type
# define function  var = body   type = dict   'Body' imported from FastAPI library
# def create_new_seed(body: dict = Body(...)):  >> new_seed inherits from Seed
def create_new_seed(new_seed: Seed):
    # displayed to user (gets converted to JSON)
    # print(body)
    # print(new_seed)  # (printed in terminal)
    # print(new_seed.dict())
    # print(new_seed.seed_type)  # (printed in terminal)
    # print(new_seed.location)  # (printed in terminal)
    # print(new_seed.date)  # (printed in terminal)
    # put in Python dictionary format:
    new_seed_dict = new_seed.dict()
    # assign ID num from random range (pre-database)--remove once connected to DB:                  #DEBUG
    new_seed_dict['id'] = randrange(0, 1000000)
    # add new seed type to dict array my_seeds:
    my_seeds.append(new_seed_dict)
    # return {"new_seed": f"title: {body['title']} content: {body['content']}"} #define seed type & collection location
    # define seed type & collection location
    # return {"new_seed": f"seed_type: {body['title']} location: {body['content']}"}
    # return {"new_seed": f"seed_type: {Seed['seed_type']} location: {Seed['location']}"}
    return {"data": new_seed_dict}  # prints seed data to user


# id is a "path parameter"--always returned as a string!
@app.get("/seedvault/{id}")  # get individual seed type by ID
def get_seed(id: int):
    print(id)
    return {"data": f"Seed: {id}"}
