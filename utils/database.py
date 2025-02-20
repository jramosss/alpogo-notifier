import os
from peewee import SqliteDatabase

db = SqliteDatabase(os.getenv("DB_NAME"))

def setup_database():
    db.connect()