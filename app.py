from fastapi import FastAPI
from utils.database import setup_database, db
from models.Place import Place
from models.Event import Event

app = FastAPI()
setup_database()
db.create_tables([Place, Event])

@app.get("/")
def read_root():
    return {"Hello": "World"}

