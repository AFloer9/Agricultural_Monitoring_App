# Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

#for creating table with raw SQL
import sqlite3
db = sqlite3.connect("database.db")
cursor = db.cursor()

cursor.execute(  # create new table in SQL DB
    "CREATE TABLE my_supplies (id integer, supply_type text, brand_name text, purch_date text, num_supply integer, amt integer, unit text)")  # SQL

db.commit()
