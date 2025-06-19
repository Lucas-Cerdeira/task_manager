from pydantic import BaseModel, Field
from datetime import datetime


class TaskBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: str = Field(..., min_length=2, max_length=255)
    completed: bool | None


class TaskCreate(TaskBase):
    ...

class TaskFull(TaskBase):
    ...


class TaskResponse(TaskBase):
    data_criacao: datetime