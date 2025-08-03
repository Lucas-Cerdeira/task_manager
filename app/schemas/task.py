from pydantic import BaseModel, Field
from datetime import datetime


class TaskBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: str = Field(..., min_length=2, max_length=255)
    completed: bool = False
    data_entrega: datetime | None = None
    diaria: bool = False


class TaskCreate(TaskBase):
    ...

class TaskFull(TaskBase):
    id: int
    user_id: int
    data_criacao: datetime
    class Config:
        orm_mode = True


class TaskResponse(TaskBase):
    ...
    class Config:
        orm_mode = True