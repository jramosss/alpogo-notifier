from fastapi import FastAPI
from utils.database import setup_database, db
from models.Place import Place
from models.Event import Event
from models.User import User
from models.Subscription import Subscription

from routers.subscription import router as subscription_router

from fastapi_utilities import repeat_every

from crons.scrape_places import cron as scrape_places_cron


app = FastAPI()
setup_database()
db.create_tables([Place, Event, User, Subscription])

app.include_router(subscription_router, prefix="/subscription", tags=["Subscriptions"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

@repeat_every(seconds=86400)
def run_cron():
    scrape_places_cron()
