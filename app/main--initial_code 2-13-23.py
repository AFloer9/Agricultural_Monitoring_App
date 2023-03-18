# main.py

from fastapi import Body, FastAPI  # import library/framework
from pydantic import BaseModel  # for Seed class template
from datetime import date  # for default date of seed collection
from random import randrange  # for random id num assignation (pre-database)
import sqlite3

app = FastAPI()  # create instance of FastAPI named 'app'


class User(BaseModel):  # extends class Basemodel--allows auto-validation of user input adherence to format--Seed inherits from Pydantic model
    id: int
    name: str
    user_name: str
    join_date: str = date.today()  # default = current date
    pw: str


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


class Supply(BaseModel):  # extends class Basemodel--allows auto-validation of user input adherence to format--Seed inherits from Pydantic model
    id: int
    supply_type: str
    brand_name: str
    purch_acq: str = date.today()  # default = current date
    num_supply: int = "1"  # default = 1 item/container
    amt: int


try:
    db = sqlite3.connect(database='database.db')
    cursor = db.cursor()
    print("connection successful")
except Exception as error:
    print("Error: ", error)


# hardcoded for post request [list{dict}] for testing--normally this would come from database:  #DEBUG
my_seeds = [{"seed_type": "daisy", "location": "backyard", "id": 1}, {
    "seed_type": "zinnia", "location": "field", "id": 2}]

# print class which object belongs to (for testing type) #DEBUG
print(type(my_seeds))

# decorator(wrapper--extends behavior of following function (show_root))    path operation/route("/")   http method(GET) to endpoint


@app.get("/")
def show_root():  # define function   ?async
    # displayed to user (gets converted to JSON) (key:value pair)
    return {"Hello": "world"}


@app.get("/login")
def user_login():  # define function
    return {"data": "login"}  # displayed to user (gets converted to JSON)


@app.get("/seedvault")  # get entire seedvault (all listings)
def show_seedvault():  # define function
    return {"data": my_seeds}  # displayed to user (gets converted to JSON)

# revive later for sensor DB (stub):
# @app.get("/sensors")  # get
# def show_sensors():  # define function
#    return {"data": "sensors"}  # displayed to user (gets converted to JSON)


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
    new_seed_dict = new_seed.dict()
    # assign ID num from random range (pre-database)--remove once connected to DB: #DEBUG
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
