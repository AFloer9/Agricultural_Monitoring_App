# Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

from fastapi import Body, FastAPI, Depends, HTTPException, status, Request, WebSocket # import library/framework
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # classes inherit from base model
from datetime import date  # for default today's date insertion to date fields
from sqlalchemy.orm import Session
from routers import gardenpathop, userspathop, sensorpathop, sensorpathop2, db_serial_arduino
from dbsetup import engine
import sqlalchmodels
import json
#import sys
#sys.path.append("../otherProjects/arduino")
from routers.db_serial_arduino import show_sensor_data, show_sensors



#sqlalchmodels.Base.metadata.drop_all(bind=engine) #tclears DB upon restarting main--COMMENT OUT FOR PERSISTENT DB
sqlalchmodels.Base.metadata.create_all(bind=engine) #creates all tables according to SQLAlchemy models--

#from db_filler import fill_db  #uncomment for populating DB for demo

#populate table if desired (comment out if not):
#fill_db() 

#from passlib.context import CryptContext  #stub for user password implementation
#pwd_context = CryptContext(schemes=["bcrypt"]) #hash algorithm type--only needed for user passowrd implementation


app = FastAPI()  # create instance of FastAPI named 'app'

#app.mount('/templates', StaticFiles(directory="templates"), name="templates")

origins = [
    "http://localhost",
    "http://localhost:5050",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates") #create template object for HTML

app.include_router(gardenpathop.router) #router object--directs API to routes in other .py files
app.include_router(userspathop.router)
app.include_router(sensorpathop.router)
app.include_router(sensorpathop2.router) 

@app.websocket("/ws")
async def websocket_getDbData(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        data = data.split()

        if data[0] == 'sensor':
            data = []
            temp = show_sensors()
            for i in temp:
                data.append({'Sensor Name': i[0], 'Sensor Id': i[1]})
        elif data[0] == 'data':
            temp = show_sensor_data()
            data = []
            flag = True
            for i in temp:
                if flag:
                    flag = False
                    continue
                data.append({'Sensor Name': i[0], 'Data': i[1], 'Location': i[2], 'Date': i[3]})
        data = json.dumps(data)
        await websocket.send_text(data)