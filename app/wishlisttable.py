#for creating table with raw SQL
import sqlite3
db = sqlite3.connect("database.db")
cursor = db.cursor()

cursor.execute(  # create new table in SQL DB
    "CREATE TABLE wishlist (id integer, plant_type text, sci_name text, water_week integer, sunlight_hrs_day integer)")  # SQL

db.commit()
