#for creating table with raw SQL
import sqlite3
db = sqlite3.connect("database.db")
cursor = db.cursor()
cursor.execute(
    "CREATE TABLE users (uid integer, name text, user_name text, join_date text, pw text, email text, zipcode text)")

db.commit()
