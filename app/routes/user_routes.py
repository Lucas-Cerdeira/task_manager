from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserResponse, UserBase, UserUpdate
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.db_services.user import UserDbServices
from app.db_services.task import TaskDbServices
from app.database.database import get_db
from app.security.auth import get_current_user
from app.models.user import User
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
    tags=["tasks"],
    status_code=status.HTTP_201_CREATED,
    operation_id="CreateTaskForUser")
def create_task_for_user(user_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    task = TaskDbServices.create_task(db=db, task=task, user_id=user_id)
    return task

@user_router.get(
    "/{user_id}/tasks/",
    response_model=List[TaskResponse],
    tags=["tasks"],
    status_code=status.HTTP_200_OK,
    operation_id="GetTasksByUserId"
)
def get_tasks_by_user_id(user_id: int, db: Session = Depends(get_db)):
    tasks = TaskDbServices.get_tasks_by_user_id(db=db, user_id=user_id)
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No tasks found for user with ID {user_id}.")
    return tasks

@user_router.delete(
    "/{user_id}/tasks/{task_id}/",
    response_model=TaskResponse,
    tags=["tasks"],
    status_code=status.HTTP_200_OK,
    operation_id="DeleteTaskForUser"
)
def delete_task_for_user(
    user_id: int, 
    task_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verifica se o usuário tem permissão para deletar a tarefa
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )
    
    task = TaskDbServices.delete_task(db=db, user_id=user_id, task_id=task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task not found.")
    return task

@user_router.put(
    "/{user_id}/tasks/{task_id}/",
    response_model=TaskResponse,
    tags=["tasks"],
    status_code=status.HTTP_200_OK,
    operation_id="UpdateTaskForUser"
)
def update_task(
    user_id: int,
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza uma tarefa existente.
    - Requer autenticação
    - Apenas o dono da tarefa pode atualizá-la
    - Campos não fornecidos não serão alterados
    """
    # Verifica se o usuário tem permissão para atualizar a tarefa
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Remove campos None do modelo de atualização
    update_data = task_update.model_dump(exclude_unset=True)
    
    # Atualiza a tarefa
    updated_task = TaskDbServices.update_task(
        db=db,
        task_id=task_id,
        user_id=user_id,
        task_data=update_data
    )
    
    return updated_task