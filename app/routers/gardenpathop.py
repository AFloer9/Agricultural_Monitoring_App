# Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

from fastapi import Body, FastAPI, Depends, HTTPException, status, APIRouter, Response  # import library/framework
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel  # classes inherit from base model
from datetime import date  # for default today's date insertion to date fields
from sqlalchemy.orm import Session
from sqlalchemy import update
import pydanticmodels
import sqlalchmodels  
from dbsetup import get_db
from typing import Dict, Optional, List
import requests

router = APIRouter()

#garden info related routes (non-user-related)

@router.get("/my_plants")  # get inventory of plants owned (all listings)
def show_my_plants(db: Session = Depends(get_db)): #opens DB session for queries
    plants = db.query(sqlalchmodels.Plant).all()  # using SQLAlchemy query
    return plants


@router.get("/seedvault")  #get inventory of all seeds collected
#@router.get("/seedvault", response_model=List[pydanticmodels.Seed]) 
def show_seeds(db: Session = Depends(get_db)):  # dependency
    seeds = db.query(sqlalchmodels.Seed).all() 
    return seeds
    #return Body('index.html')

@router.get("/wishlist") #get list of all plants/seeds on wishlist
def show_wishlist(db: Session = Depends(get_db)):  
    plants = db.query(sqlalchmodels.Plant).all()  
    #print(seeds)  # print to terminal
    return plants

@router.get("/my_supplies") #get gadening supply inventory
def show_supplies(db: Session = Depends(get_db)):  
    supplies = db.query(sqlalchmodels.Supply).all() 
    #print(seeds)  # print to terminal
    return supplies

@router.get("/my_sensors") #**Arduino sensors* list
def show_sensors(db: Session = Depends(get_db)):
    sensors = db.query(sqlalchmodels.Sensor).all()
    return sensors

@router.get("/my_data")  #**Arduino data* list
def show_sensor_data(db: Session = Depends(get_db)):
    sensor_data = db.query(sqlalchmodels.SensorData).all()
    return sensor_data


# id is a "path parameter"--always returned as a string!



@router.get("/seedvault/{seed_type}")  #get all seeds of a certain type
def get_seed_by_type(seed_type: str, db: Session = Depends(get_db)): 
#if id can be successfully converted to int, go to get_seed_by_id()...   int(id)
    seed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.seed_type == seed_type).all() # using SQLAlchemy query
    return seed

@router.get("/seedvault/{id}")  #get a single seed by id    #FIX--read as a string by API, need to distinguish from above method
#if id can be successfully converted to int, continue...   int(id)
def get_seed_by_id(id: int, db: Session = Depends(get_db)):  #auto-converts id to int
    seed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.id == id).first()  # using SQLAlchemy query
    print(id)
    return seed

@router.delete("/seedvault/{id}", status_code=status.HTTP_204_NO_CONTENT)  #delete seed of a specific id
def delete_seed(id: int, db: Session = Depends(get_db)):  
    delseed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.id == id)  # using SQLAlchemy query SELECT
    seed = delseed.first() 
    if seed == None:
        print("no seed by that ID")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(seed)
    db.commit()
    return {"seed deleted"}

@router.post("/seedvault", status_code=status.HTTP_201_CREATED, response_model=pydanticmodels.CreateSeed)    #INSERT/create new seed
def create_new_seed(seed: pydanticmodels.CreateSeed, db: Session = Depends(get_db)):
    #new_seed = sqlalchmodels.Seed(id=seed.id, seed_type=seed.seed_type, coll_loc = seed.coll_loc, 
    #coll_date = seed.coll_date, num_coll = seed.num_coll)          
    new_seed = sqlalchmodels.Seed(**seed.dict())
    if new_seed.seed_type == None:
        return {"Please provide a seed type"}
    else:    
        db.add(new_seed)
        db.commit()
        db.refresh(new_seed) #flush
        return new_seed

#@router.put("/seedvault/{seed_type}", response_model=pydanticmodels.EditSeed) 
@router.put("/seedvault/{id}", response_model=pydanticmodels.EditSeed) 
def edit_seed(id: int, seed: pydanticmodels.Seed, db: Session = Depends(get_db)):   #inputs to method from HTTP response
#def edit_seed(seed_type: str, seed: pydanticmodels.Seed, db: Session = Depends(get_db)):   #inputs to method from HTTP response
    #edseed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.seed_type == 'seed_type').one_or_none() #find seed by type
    #edseed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.id == id).get(id)  #find seed by ID
    edseed = db.query(sqlalchmodels.Seed).where(sqlalchmodels.Seed.id == id).one()  #find seed by ID
    print({edseed})
    if edseed == None:
        print("no seed by that ID")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    json_data = jsonable_encoder(edseed)
    
    #db.execute(update(seed).values(sqlalchmodels.Seed(seed.dict())))
    
    #db.execute(update(seed.dict()))
   
    
    #newedseed = (edseed.dict())
    #newedseed = dict(sqlalchmodels.Seed)
    #edseed = dict()
    #newedseed = dict(edseed)
    #newedseed = {sqlalchmodels.Seed}
    
    
    
    #for key, value in newedseed.items():
        #setattr(newedseed, key, value)
        
    for key, value in json_data.items():
        setattr(json_data, key, value)
    
    #stmt = db.seedvault.update().where(db.seedvault.id == id).values()
    
    #db.execute(stmt)
    #db.execute(update().where(sqlalchmodels.Seed.id == id).           
               #values({'seed_type': 'fakeflower', 'coll_loc': 'field', 'num_coll': '34'}))
               #values(**{'seed_type': 'seed_type', 'coll_loc': 'call_loc', 'num_coll': 'num_coll'}))
            
                #values('seed_type', 'coll_loc', 'num_coll'))
                #values(sqlalchmodels.Seed(**seed.dict())))
    db.add(edseed)
    #db.refresh
    db.commit()
    #return edseed
    return JSONResponse(content=json_data)
   
   
    
#@router.patch("/seedvault/{id}", response_model=pydanticmodels.EditSeed) 
@router.patch("/seedvault/{id}", response_model=None) 
def edit_seed_attrib(id: int, updated_seed: pydanticmodels.EditSeed, db: Session = Depends(get_db)): 
    edseed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.id == id).one() # using SQLAlchemy query
    updated_seed = edseed.first()
    if updated_seed == None:
        print("no seed by that ID")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    #edseed.update({'seed_type': 'sweet pea', 'coll_loc': 'field', 'num_coll': '34'})  #hardcode DEBUG
    edseed.update({'id': id, 'seed_type': 'seed_type', 'coll_loc': 'coll_loc',              #NO ID
    'coll_date': 'coll_date', 'num_coll': 'num_coll'}, synchronize_session=False)

    #edseed.update(updated_seed.dict(), synchronize_session=False)
    db.add(edseed)
    db.commit()
    return edseed.first()