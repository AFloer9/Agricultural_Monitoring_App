# Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

from fastapi import Body, FastAPI, Depends, HTTPException, status, APIRouter, Response, Request, Form  # import library/framework
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import HTTPConnection
from pydantic import BaseModel  # classes inherit from base model
from datetime import date  # for default today's date insertion to date fields
from sqlalchemy.orm import Session
from sqlalchemy.types import SchemaType, PickleType
from sqlalchemy import update, JSON  
from typing import Dict, Optional, List, Annotated
from jinja2 import Environment, FileSystemLoader, Template
import sqlalchmodels
import pydanticmodels
from dbsetup import get_db

router = APIRouter()

templates = Jinja2Templates(directory="./templates/") #create template object for HTML

#path operations:
# API server drills down thru request functions until it finds an HTTP request match:

# @decorator(wrapper--extends behavior of following function (i.e. show_root))    
# path operation/route URL (i.e. "/")   http method(i.e. GET) to endpoint

#methods formatted as below are for Python-language DB queries using SQLAlchemy library:

# id is a "path parameter"--always returned as a string!

#garden DB info-related routes (non-user-related)

#**if paths are identical, first route will be taken**

#@router.get("/")   
#def show_root():  
    #displayed to user: (gets converted to JSON) (key:value pair)
    #return {"Welcome to the Agricultural Monitoring Project"}
    #shows on webpage at path address
    
 #FOR HTML/JS
# @router.get("/")   
# def show_main(request: Request, db: Session = Depends(get_db)):
#     return templates.TemplateResponse("index.html", {"request": request})


# @router.get("/seedvault")  #get inventory of all seeds collected         db version--HTTP--no front end
# #@router.get("/seedvault", response_model=List[pydanticmodels.Seed]) 
# def show_seeds(db: Session = Depends(get_db)):  # dependency
#     seeds = db.query(sqlalchmodels.Seed).all() 
#      #print(seeds)  # print to terminal
#     return seeds   #(gets converted to JSON) (key:value pair)

 #FOR HTML/JS
# #@router.get("/seedvault")
@router.get("/", response_class=HTMLResponse)  #TEST for jinja template
# #@router.get("/seedvault", response_model=List[pydanticmodels.Seed]) 
def test_show_main(request: HTTPConnection, db: Session = Depends(get_db)):  # dependency
    #seeds = db.query(sqlalchmodels.Seed).all() 
#     #seeds = ("daisy")
#     print(seeds)
#     print(request)
    #return seeds
#     return templates.TemplateResponse("index.html", {'request': request, 'seeds':seeds} )
    return templates.TemplateResponse("index.html", {"request": request})
#     #return template(seed_type=seeds)
   
# #FOR HTML/JS  
@router.get("/seedvault/", response_class=HTMLResponse)  #TEST for jinja template
# #@router.get("/seedvault", response_model=List[pydanticmodels.Seed]) 
def test_show_seeds(request: HTTPConnection, db: Session = Depends(get_db)):  # dependency
    seeds = db.query(sqlalchmodels.Seed).all() 
#     #return templates.TemplateResponse("seedvault.html", {'request': request} )
    return templates.TemplateResponse('index.html', {"request": request})

    
@router.get("/my_plants")  # get inventory of plants owned (all listings)
def show_my_plants(db: Session = Depends(get_db)): #opens DB session for queries
    plants = db.query(sqlalchmodels.Plant).all()  # using SQLAlchemy query
    return plants

@router.get("/wishlist") #get list of all plants/seeds on wishlist
def show_wishlist(db: Session = Depends(get_db)):  
    plants = db.query(sqlalchmodels.Plant).all() 
    #print(wishlist)  # print to terminal
    return plants

@router.get("/my_supplies") #get gadening supply inventory
def show_supplies(db: Session = Depends(get_db)):  
    supplies = db.query(sqlalchmodels.Supply).all() 
    #print(supplies)  # print to terminal
    return supplies

@router.get("/myclimate") #for external API calls--stub for now
def show_climatedata():
    return


@router.get("/seedvault/{seed_type}")  #get all seeds of a certain type
def get_seed_by_type(seed_type: str, db: Session = Depends(get_db)): 
#if id can be successfully converted to int, go to get_seed_by_id()...   int(id)
    seed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.seed_type == seed_type).all() # using SQLAlchemy query
    print(seed)
    return seed

@router.get("/seedvault/{id}")  #get a single seed by id    #FIX--read as a string by API, need to distinguish from above method
#if id can be successfully converted to int, continue...   int(id)
def get_seed_by_id(id: int, db: Session = Depends(get_db)):  #auto-converts id to int
    seed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.id == id).first()  # using SQLAlchemy query
    print(id)
    print(seed)
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
    print("seed deleted")
    return {"seed deleted"}

@router.post("/seedvault", status_code=status.HTTP_201_CREATED)    #INSERT/create new seed
def create_new_seed(seed: pydanticmodels.CreateSeed, db: Session = Depends(get_db)):  #<<FOR POSTMAN    
    #FOR WEBPAGE FORM
#def create_new_seed(seed_type: Annotated[str, Form()], coll_loc: Annotated[str, Form()], coll_date: Annotated[str, Form()], num_coll: Annotated[str, Form()],   db: Session = Depends(get_db)):
    #new_seed = sqlalchmodels.Seed(seed_type=seed_type, coll_loc = coll_loc, 
    #coll_date = coll_date, num_coll = num_coll)   
    #new_seed = sqlalchmodels.Seed(seed_type=seed_type, coll_loc = coll_loc, 
    #coll_date = coll_date, num_coll = num_coll)   
    new_seed = sqlalchmodels.Seed(**seed.dict())
    #if new_seed.seed_type == None:
        #return {"Please provide a seed type"}
    #else:    
    #print(seed_type, coll_loc, coll_date, num_coll)
    print(new_seed)
    #db.add(seed_type, coll_loc, coll_date, num_coll) # type: ignore #, coll_date, coll_loc, num_coll)
    db.add(new_seed)
    db.commit()
    db.refresh(new_seed) #flush
    #return JSONResponse(seed_type) #return JSON model of newly-created seed to user
    #return templates.TemplateResponse("seedvault.html",)
    return new_seed


#@router.put("/seedvault/{seed_type}", response_model=pydanticmodels.EditSeed) 
#@router.put("/seedvault/{id}", response_model=pydanticmodels.EditSeed) 
#@router.put("/seedvault/{id}")
#def edit_seed(id: int, seed: pydanticmodels.Seed, db: Session = Depends(get_db)):   #inputs to method from HTTP response
#def edit_seed(seed_type: str, seed: pydanticmodels.Seed, db: Session = Depends(get_db)):   #inputs to method from HTTP response
    #edseed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.seed_type == 'seed_type').one_or_none() #find seed by type
    #edseed = db.query(sqlalchmodels.Seed).filter(sqlalchmodels.Seed.id == id).get(id)  #find seed by ID
    edseed = db.query(sqlalchmodels.Seed).where(sqlalchmodels.Seed.id == id).first()  #find seed by ID
    
    if edseed == None:
        print("no seed by that ID")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    #json_data = jsonable_encoder(edseed)
    
    #db.execute(update(seed).values(sqlalchmodels.Seed(seed.dict())))
    
    #db.execute(update(seed.dict()))
   
    #newedseed = dict(edseed.__dict__)
    #print(edseed.__dict__)
    #newedseed = dict(sqlalchmodels.Seed)
    #edseed = dict()
    newedseed = dict(edseed)
    #newedseed = {sqlalchmodels.Seed}
    
    #for key, value in newedseed.items():
        #setattr(newedseed, key, value)
        
    #for key, value in newedseed.items():
        #setattr(newedseed, key, value)
        
    #print(*newedseed)
    #stmt = db.seedvault.update().where(db.seedvault.id == id).values()
    
    #db.execute(stmt)
    #db.execute(update().where(sqlalchmodels.Seed.id == id).           
               #values({'seed_type': 'fakeflower', 'coll_loc': 'field', 'num_coll': '34'}))
               #values(**{'seed_type': 'seed_type', 'coll_loc': 'call_loc', 'num_coll': 'num_coll'}))
            
                #values('seed_type', 'coll_loc', 'num_coll'))
                #values(sqlalchmodels.Seed(**seed.dict())))
    db.add(newedseed)
    db.commit()
    db.refresh(newedseed)
    return newedseed
    #return JSONResponse(content=json_data)
   
   