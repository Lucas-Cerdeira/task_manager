from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from app.models.evento import Evento
from app.schemas.evento import EventoCreate, EventoUpdate
from datetime import datetime

logger = logging.getLogger(__name__)

class EventoDbServices:
    
    @staticmethod
    def create_evento(db: Session, evento: EventoCreate, user_id: int):
        """
        Cria um novo evento.
        Args:
            db (Session): Sessão ativa do SQLAlchemy.
            evento: Dados válidos do evento.
            user_id: Id do usuário.
        Returns:
            evento: Schema do evento criado
        """
        try:
            new_evento = Evento(**evento.model_dump(), user_id=user_id)
            db.add(new_evento)
            db.commit()
            db.refresh(new_evento)
            return new_evento

        except IntegrityError as e:
            db.rollback()
            logger.error(f"Erro ao criar evento: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Erro ao criar evento no banco de dados: Dados duplicados."
            )

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Erro ao criar evento: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar evento no banco de dados."
            )
    
    @staticmethod
    def get_eventos_by_user_id(db: Session, user_id: int):
        """
        Retorna todos os eventos de um usuário.
        Args:
            db (Session): Sessão ativa do SQLAlchemy.
            user_id: Id do usuário.
        Returns:
            List[Evento]: Lista com todos os eventos.
        """
        try:
            eventos = db.query(Evento).filter(Evento.user_id == user_id).all()
            return eventos
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Erro ao buscar eventos: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao buscar eventos."
            )
    
    @staticmethod
    def update_evento(db: Session, evento_id: int, evento_update: EventoUpdate):
        """
        Atualiza um evento existente.
        Args:
            db (Session): Sessão ativa do SQLAlchemy.
            evento_id: Id do evento a ser atualizado.
            evento_update: Dados para atualização.
        Returns:
            Evento: Evento atualizado.
        """
        try:
            evento = db.query(Evento).filter(Evento.id == evento_id).first()
            if not evento:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Evento não encontrado."
                )
            
            update_data = evento_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(evento, field, value)
            
            db.commit()
            db.refresh(evento)
            return evento
            
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Erro ao atualizar evento: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar evento."
            )
    
    @staticmethod
    def delete_evento(db: Session, evento_id: int, user_id: int):
        """
        Deleta um evento.
        Args:
            db (Session): Sessão ativa do SQLAlchemy.
            evento_id: Id do evento.
            user_id: Id do usuário.
        Returns:
            Evento: O evento deletado.
        """
        try:
            evento = db.query(Evento).filter(
                Evento.id == evento_id,
                Evento.user_id == user_id
            ).first()
            
            if not evento:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Evento não encontrado."
                )
            
            db.delete(evento)
            db.commit()
            return evento
            
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Erro ao deletar evento: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao deletar evento."
            )
