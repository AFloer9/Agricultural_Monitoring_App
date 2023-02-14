import sqlite3
db = sqlite3.connect("database.db")
cursor = db.cursor()

cursor.execute(  # create new table in SQL DB
    "CREATE TABLE wishlist (plant_type text, watering text, sunlight text)")  # SQL

db.commit()
