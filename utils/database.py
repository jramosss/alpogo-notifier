import os
from peewee import SqliteDatabase

DB_NAME = os.getenv("DB_NAME")
if not DB_NAME:
    raise ValueError("DB_NAME environment variable is not set")

db = SqliteDatabase(DB_NAME)

def setup_database():
    pass