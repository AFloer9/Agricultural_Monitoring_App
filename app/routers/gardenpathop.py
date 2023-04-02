# Author: Anna Hyer Spring 2023 Class: Intro to Programming

from fastapi import Body, FastAPI, Depends, HTTPException, status, APIRouter  # import library/framework
from pydantic import BaseModel  # classes inherit from base model
from datetime import date  # for default today's date insertion to date fields
from sqlalchemy.orm import Session
import pydanticmodels
import sqlalchmodels  
from dbsetup import get_db

router = APIRouter()

#garden info related routes

@router.get("/my_plants")  # get inventory of plants owned (all listings)
def show_my_plants(db: Session = Depends(get_db)): #opens DB session for queries
    plants = db.query(sqlalchmodels.Plant).all()  # using SQLAlchemy query
    return {"data": plants}


@router.get("/seedvault") 
def show_seeds(db: Session = Depends(get_db)):  # dependency
    seeds = db.query(sqlalchmodels.Seed).all() 
    #print(seeds)  # print to terminal
    #return {"data": seeds}
    return {"data": seeds}

@router.get("/wishlist") 
def show_wishlist(db: Session = Depends(get_db)):  
    plants = db.query(sqlalchmodels.Plant).all()  
    #print(seeds)  # print to terminal
    return {"data": plants}

@router.get("/my_supplies") 
def show_supplies(db: Session = Depends(get_db)):  
    supplies = db.query(sqlalchmodels.Supply).all() 
    #print(seeds)  # print to terminal
    return {"data": supplies}

@router.get("/my_sensors")
def show_sensors(db: Session = Depends(get_db)):
    sensors = db.query(sqlalchmodels.Sensor).all()
    return {"data": sensors}

@router.get("/my_data")
def show_sensor_data(db: Session = Depends(get_db)):
    sensor_data = db.query(sqlalchmodels.SensorData).all()
    return {"data": sensor_data}


# id is a "path parameter"--always returned as a string!
@router.get("/seedvault/{id}") 
def get_seed(id: int, db: Session = Depends(get_db)):  
    seed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.id == id).first()  # using SQLAlchemy query
    #return seed
    print(id)
    return {"data": f"Seed: {id}"}

@router.delete("/seedvault/{id}", ) 
def delete_seed(id: int, db: Session = Depends(get_db)):  
    delseed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.id == id)  # using SQLAlchemy query
    seed = delseed.first() 
    if seed == None:
        print("no seed by that ID")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(seed)
    db.commit()
    return {"seed deleted"}

@router.post("/seedvault", status_code=status.HTTP_201_CREATED, response_model=pydanticmodels.CreateSeed)
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

@router.put("/seedvault/{id}", response_model=pydanticmodels.EditSeed) 
def edit_seed(id: int, db: Session = Depends(get_db)): 
    edseed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.id == id) # using SQLAlchemy query
    seed = edseed.first() 
    if seed == None:
        print("no seed by that ID")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    edseed.update({'seed_type': 'snapdragon', 'coll_loc': 'field', 'num_coll': '34'})
    db.commit()
    return seed