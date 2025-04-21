from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserResponse
from app.db_services.user import UserDbServices
from app.database.database import get_db
from sqlalchemy.orm import Session
from typing import List


user_router = APIRouter(prefix="/users")


@user_router.get("/",response_model=List[UserResponse], tags=["users"] )
async def read_users(db: Session = Depends(get_db)):
    users = UserDbServices.get_all_users(db=db)
    return users

@user_router.post("/create_user/", response_model=UserResponse, tags=["users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserDbServices.create_user(user=user, db=db)

@user_router.get("/{user_id}", response_model=UserResponse, tags=["users"])
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = UserDbServices.get_user_by_id(db=db, user_id=user_id)
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found.")
    return user