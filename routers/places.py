from fastapi import APIRouter

from models.Place import Place

router = APIRouter()

@router.get("/all")
async def get_all_places():
    places = Place.select().execute()
    return {"places": [place.__data__ for place in places]}