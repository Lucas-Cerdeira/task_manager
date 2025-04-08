from fastapi import APIRouter
from app.schemas.user import UserBase

user_router = APIRouter()



@user_router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]