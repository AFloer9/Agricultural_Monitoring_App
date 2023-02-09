# main.py

from fastapi import Body, FastAPI  # import library/framework
from pydantic import BaseModel  # for Seed class template
from datetime import date  # for default date of seed collection
from random import randrange  # for random id num assignation (pre-database)
app = FastAPI()  # create instance of FastAPI named 'app'


class Seed(BaseModel):  # extends class Basemodel--allows auto-validation of user input adherence to format--'Pydantic model'
    seed_type: str
    location: str
    date: str = date.today()  # default = current date
    number_of_seeds: int = "1"  # default = 1 seed


# hardcoded for testing--normally this would come from database:
my_seeds = [{"seed_type": "daisy", "location": "backyard", "id": 1}, {
    "seed_type": "zinnia", "location": "field", "id": 2}]

# decorator    path operation/route("/")   http method(GET) to endpoint


@app.get("/")
def show_root():  # define function 'show_root"   ?async
    # displayed to user (gets converted to JSON) (key:value pair)
    return {"Hello": "world"}


@app.get("/login")  # get
def user_login():  # define function
    return {"data": "login"}  # displayed to user (gets converted to JSON)


@app.get("/seedvault")  # get entire seedvault (all listings)
def show_seedvault():  # define function
    return {"data": my_seeds}  # displayed to user (gets converted to JSON)


@app.get("/sensors")  # get
def show_sensors():  # define function
    return {"data": "sensors"}  # displayed to user (gets converted to JSON)


@app.post("/seedvault")  # post -- add new seed type
# define function  var = body   type = dict   'Body' imported from FastAPI library
# def create_new_seed(body: dict = Body(...)):
def create_new_seed(new_seed: Seed):
    # displayed to user (gets converted to JSON)
    # print(body)
    # print(new_seed)  # (printed in terminal)
    # print(new_seed.dict())
    # print(new_seed.seed_type)  # (printed in terminal)
    # print(new_seed.location)  # (printed in terminal)
    # print(new_seed.date)  # (printed in terminal)
    new_seed_dict = new_seed.dict()
    # assign ID num from random range (pre-database)--remove once connected to DB:
    new_seed_dict['id'] = randrange(0, 1000000)
    # add new seed type to dict array my_seeds:
    my_seeds.append(new_seed_dict)
    # return {"new_seed": f"title: {body['title']} content: {body['content']}"} #define seed type & collection location
    # define seed type & collection location
    # return {"new_seed": f"seed_type: {body['title']} location: {body['content']}"}
    # return {"new_seed": f"seed_type: {Seed['seed_type']} location: {Seed['location']}"}
    return {"data": new_seed_dict}  # prints seed data to user


# id is a "path parameter"--always returned as a string!
@app.get("/seedvault/{id}")  # get individual seed type
def get_seed(id: int):
    print(id)
    return {"data": f"Seed: {id}"}
