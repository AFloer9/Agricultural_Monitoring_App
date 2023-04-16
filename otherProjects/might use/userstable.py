# Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

#for creating table with raw SQL
import sqlite3
db = sqlite3.connect("database.db")
cursor = db.cursor()
cursor.execute(
    "CREATE TABLE users (name text, user_name text, join_date text, pw text, email text, zipcode text)")

db.commit()
