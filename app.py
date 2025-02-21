from dotenv import load_dotenv
import os

env_file = ".env.development" if os.getenv("ENV") == "DEV" else ".env.test"
load_dotenv(env_file)

from fastapi import FastAPI

from utils.database import setup_database, db
from models.Place import Place
from models.Event import Event
from models.User import User
from models.Subscription import Subscription

from routers.subscription import router as subscription_router
from routers.user import router as user_router
from routers.places import router as places_router

from fastapi_utilities import repeat_every

from crons.scrape_places import cron as scrape_places_cron
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_database()
db.create_tables([Place, Event, User, Subscription])

app.include_router(subscription_router, prefix="/subscription", tags=["Subscriptions"])
app.include_router(user_router, prefix="/user", tags=["Users"])
app.include_router(places_router, prefix="/places", tags=["Places"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

@repeat_every(seconds=86400)
def run_cron():
    scrape_places_cron()
