from pydantic import BaseModel
from datetime import date


class TaskBase(BaseModel):
    nome: str
    descricao: str
    completed: bool | None


class TaskCreate(TaskBase):
    user_id: int


class TaskResponse(TaskBase):
    data_criacao: date