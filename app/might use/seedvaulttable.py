# Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

#for creating table with raw SQL
import sqlite3
db = sqlite3.connect("database.db")
cursor = db.cursor()

cursor.execute(
    "CREATE TABLE seedvault (id integer, seed_type text, coll_loc text, coll_date text, num_coll integer)")

db.commit()
