from pydantic import BaseModel, Field
from datetime import datetime


class EventoBase(BaseModel):
    titulo: str = Field(..., min_length=2, max_length=100)
    descricao: str = Field(..., min_length=2, max_length=255)
    local: str = Field(..., min_length=2, max_length=255)
    data_evento: datetime

class EventoCreate(EventoBase):
    pass

class EventoRead(EventoBase):
    id: int
    user_id: int
    data_criacao: datetime
    class Config:
        from_attributes = True

class EventoUpdate(BaseModel):
    titulo: str | None = Field(None, min_length=2, max_length=100)
    descricao: str | None = Field(None, min_length=2, max_length=255)
    local: str | None = Field(None, min_length=2, max_length=255)
    data_evento: datetime | None = None
