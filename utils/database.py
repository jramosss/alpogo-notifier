import os
from peewee import SqliteDatabase

if not os.getenv("DB_NAME"):
    raise ValueError("DB_NAME environment variable is not set")

db = SqliteDatabase(os.getenv("DB_NAME"))

def setup_database():
    db.connect()