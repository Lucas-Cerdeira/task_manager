from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserResponse, UserBase, UserUpdate
from app.schemas.task import TaskCreate, TaskResponse
from app.db_services.user import UserDbServices
from app.db_services.task import TaskDbServices
from app.database.database import get_db
from sqlalchemy.orm import Session
from typing import List


user_router = APIRouter(prefix="/users")


@user_router.get("/", 
        response_model=List[UserResponse], 
        tags=["users"], 
        status_code=status.HTTP_200_OK)
async def read_users(db: Session = Depends(get_db)):
    users = UserDbServices.get_all_users(db=db)
    return users

@user_router.post(
        "/create_user/", 
        response_model=UserResponse, 
        tags=["users"],
        status_code=status.HTTP_201_CREATED,
        operation_id="CreateUser"
        )
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = UserDbServices.create_user(user=user, db=db)
    return user

@user_router.get(
        "/email/",
        response_model=UserResponse,
        tags=["users"],
        status_code=status.HTTP_200_OK,
        operation_id="GetUserByEmail"
)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user: UserResponse = UserDbServices.get_user_by_email(db=db, email=email)
    return user

@user_router.get(
        "/{user_id}/", 
        response_model=UserResponse, 
        tags=["users"],
        status_code=status.HTTP_200_OK,
        operation_id="GetUserById"
        )
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = UserDbServices.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found.")
    return user

@user_router.put(
        "/update/{user_id}/",
        response_model=UserResponse,
        tags=["users"],
        status_code=status.HTTP_200_OK,
        operation_id="UpdateUser"
)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    user = UserDbServices.update_user(db=db, userbase=user, user_id=user_id)
    return user


@user_router.post(
    "/{user_id}/create_task/", 
    response_model=TaskResponse,
    tags=["users"],
    status_code=status.HTTP_201_CREATED,
    operation_id="CreateTaskForUser")
def create_task_for_user(user_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    task = TaskDbServices.create_task(db=db, task=task, user_id=user_id)
    return task