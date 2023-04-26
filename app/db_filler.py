# Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

import random
import sqlalchmodels
from sqlalchemy.orm import sessionmaker
from faker import Faker
from faker.providers import BaseProvider, lorem

from sqlalchemy.orm import Session

fake = Faker() #fake object for testing

fake = Faker() #fake object for testing

class SeedProvider(BaseProvider):
    def seed(self):
        seed = ['sunflower', 'zinnia', 'pansy']
        
        return random.choice(seed)

fake.add_provider(SeedProvider)
#fake.seed()



#need to make provider lists for: seed names, plant names, scientific plant names, supply types, supply brands, supply units, sensor typres, sensor locations

def fill_db():
    i = 1
    while i < 100:
        i += 1
        demoseed = sqlalchmodels.Seed(
            id = fake.unique.random_int(1, 3000),
            seed_type = fake.word(),
            #seed_type = fake.seed(),
            #seed_type = fake.random.seed(),
            coll_loc = fake.city(), 
            coll_date = fake.date(), 
            num_coll = fake.random_int(1, 200)
        )  
        
        demouser = sqlalchmodels.User(  # extends demo = sqlalchmodels.() Base--allows auto-validation of user input adherence to format--Seed inherits from Pydantic model
            uid = fake.unique.random_int(1, 3000),
            name = fake.name(),
            user_name = fake.word(),
            # str = date.today()  # default = current date
            #join_date = Column(DATE, server_default=text('today()'))
            join_date = fake.date(),
            pw = fake.password(),
            email = fake.email(),
            zipcode = fake.zip()
        )

        demoplant = sqlalchmodels.Plant(  # extends demo = sqlalchmodels.Basemodel--allows auto-validation of user input adherence to format--Seed inherits from Pydantic model
            id =  fake.unique.random_int(1, 3000),
            plant_type = fake.word(),
            sci_name =  fake.word(),
            # str = date.today()  # default = current date
            date_acq = fake.date(),
            num_plants = fake.random_int(1, 20),  # int = "1"  # default = 1 plant
            watering_week = fake.random_int(0, 20),    #qaurts? gallons?
            sunlight_hrs_day = fake.random_int(1, 12),
        )

        demosupply = sqlalchmodels.Supply(  # extends demo = sqlalchmodels.Basemodel--allows auto-validation of user input adherence to format--Seed inherits from Pydantic model
            id =  fake.unique.random_int(1, 3000),
            supply_type = fake.word(),
            brand_name =  fake.word(),
            # str = date.today()  # default = current date
            purch_acq = fake.date(),
            # int = "1"  # default = 1 item/container
            num_supply =  fake.random_int(1, 50),
            # int = "1"  # default = 1 unit
            amt =  fake.random_int(1, 5),
            # str = "lbs."  # default = pounds; could be ounces, etc.
            unit = fake.word()
        )

        demosensor = sqlalchmodels.Sensor(  #table of sensors owned by user
            ID =  fake.unique.random_int(1, 3000),
            sensor_type = fake.word(),
            #sensor_loc =  fake.word()   #commented out for Alex's version
        )
        
        demodata = sqlalchmodels.SensorData(  #data from sensors  commented out: my version
            #id =  fake.unique.random_int(1, 3000),   #my version
            data_id =  fake.unique.random_int(1, 3000),   #Alex
            data = fake.word(),   #Alex
            #humidity =  fake.random_int(20, 100), #percentage (realistic likely range)
            #temperature =  fake.random_int(10, 110), #Fahrenheit
            #shade =  fake.random_int(0, 100),  #percentage
            #water_level =  fake.random_int(1, 100)  #percentage--will depend on vessel
            sensor_loc =  fake.word()  #pasted for Alex's version
        )
        Session.add_all
        Session.commit  