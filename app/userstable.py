import sqlite3
db = sqlite3.connect("database.db")
cursor = db.cursor()
cursor.execute(
    "CREATE TABLE users (uid integer, user_name text, pw text, join_date text)")

db.commit()
