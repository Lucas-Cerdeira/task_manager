from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.db_services.evento import EventoDbServices
from app.schemas.evento import EventoCreate, EventoRead, EventoUpdate

router = APIRouter(
    prefix="/users",
    tags=["eventos"]
)

@router.post("/{user_id}/create_evento/", status_code=status.HTTP_201_CREATED, response_model=EventoRead)
def create_evento(user_id: int, evento: EventoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo evento para um usuário específico.
    - user_id: ID do usuário
    - evento: Dados do evento a ser criado
    """
    return EventoDbServices.create_evento(db=db, evento=evento, user_id=user_id)

@router.get("/{user_id}/eventos/", response_model=List[EventoRead])
def get_eventos_by_user_id(user_id: int, db: Session = Depends(get_db)):
    """
    Retorna todos os eventos de um usuário específico.
    - user_id: ID do usuário
    """
    return EventoDbServices.get_eventos_by_user_id(db=db, user_id=user_id)

@router.put("/{user_id}/eventos/{evento_id}/", response_model=EventoRead)
def update_evento(user_id: int, evento_id: int, evento_update: EventoUpdate, db: Session = Depends(get_db)):
    """
    Atualiza um evento específico.
    - user_id: ID do usuário
    - evento_id: ID do evento a ser atualizado
    - evento_update: Dados a serem atualizados
    """
    return EventoDbServices.update_evento(db=db, evento_id=evento_id, evento_update=evento_update)

@router.delete("/{user_id}/eventos/{evento_id}/", status_code=status.HTTP_200_OK, response_model=EventoRead)
def delete_evento(user_id: int, evento_id: int, db: Session = Depends(get_db)):
    """
    Remove um evento específico.
    - user_id: ID do usuário
    - evento_id: ID do evento a ser removido
    """
    return EventoDbServices.delete_evento(db=db, evento_id=evento_id, user_id=user_id)
