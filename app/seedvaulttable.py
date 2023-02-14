import sqlite3
db = sqlite3.connect("database.db")
cursor = db.cursor()
cursor.execute(
    "CREATE TABLE seedvault (seed_type text, coll_loc text, coll_date text, num_coll integer)")

db.commit()
