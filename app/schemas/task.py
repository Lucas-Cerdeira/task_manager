from pydantic import BaseModel
from datetime import datetime


class TaskBase(BaseModel):
    nome: str
    descricao: str
    completed: bool | None


class TaskCreate(TaskBase):
    ...

class TaskFull(TaskBase):
    ...


class TaskResponse(TaskBase):
    data_criacao: datetime