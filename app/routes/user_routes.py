from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserResponse
from app.db_services.user import UserDbServices
from app.database.database import get_db
from sqlalchemy.orm import Session


user_router = APIRouter()


@user_router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@user_router.post("/create_user/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserDbServices.create_user(user=user, db=db)