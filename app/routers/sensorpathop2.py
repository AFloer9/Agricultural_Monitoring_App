# Author: Anna Hyer & Alex Flores Spring 2023 Class: Fundamentals of Software Engineering

from fastapi import Body, FastAPI, Depends, HTTPException, status, APIRouter, Response, Request  # import library/framework
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel  # classes inherit from base model
from datetime import date  # for default today's date insertion to date fields
from sqlalchemy.orm import Session
from sqlalchemy.types import SchemaType, PickleType
from sqlalchemy import update, JSON, func
from typing import Dict, Optional, List


router = APIRouter()

templates = Jinja2Templates(directory="templates") #create template object for HTML

@router.get("/")  #home
def show_main(request: Request):
	return "Welcome! :>)"

@router.get("/sensors")  #**Arduino data* list
def show_sensor_data(request: Request):
	return templates.TemplateResponse("db_interface.html", {"request": request})

@router.get("/climate")  #weather API
def show_climate_data(request: Request):
	return templates.TemplateResponse("json_data.html", {"request": request})
