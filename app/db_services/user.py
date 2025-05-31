from pydantic import EmailStr
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from app.models.user import User
from app.schemas.user import UserCreate, UserBase


logger = logging.getLogger(__name__)


class UserDbServices():

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """
        Cria um novo usuário no banco de dados.

        Args:
            db (Session): Sessão ativa do SQLAlchemy.
            user_data (UserCreate): Dados validados do novo usuário.

        Returns:
            User: Instância do usuário criado.
        """
        try:
            new_user = User(**user.model_dump())  # Mais seguro que dict()
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        
        #IntegrityError
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Erro ao criar usuário: {str(e)}")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Erro ao criar usuário no banco de dados: Dados duplicados.")

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Erro ao criar usuário: {str(e)}")
            raise HTTPException("Erro ao criar usuário no banco de dados.")
            

        except Exception as e:
            logger.exception("Erro inesperado ao criar usuário.")
            raise


    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        """
        Pega o usuário no banco pelo id.
        Args:
            db (Session): Sessão ativa do SQLAlchemy.
            user_id: id do usuários.
        returns:
            User: instância do usuário criado.
        """
        try:
            user = db.query(User).filter(User.id == user_id).first()
            return user
        except SQLAlchemyError as erro:
            db.rollback()
            logger.error(f"Erro ao resgatar usuário: {str(erro)}")
            raise HTTPException("Erro ao pegar usuario.")
        except Exception as e:
            raise

    @staticmethod
    def get_all_users(db: Session):
        """
        Retorna todos os registros de usuários cadastrados.
        Args:
            db (Session): Sessão ativa do do SQLAlchemy.
        returns:
            List[User]: Lista de usuários.
        """
        try:
            users = db.query(User).all()
            return users
        except SQLAlchemyError as erro:
            db.rollback()
            logger.error(f"Erro ao buscar usuários: {str(erro)}")
        except Exception as e:
            raise HTTPException(f"Erro ao buscar usuários: {str(erro)}")

    @staticmethod
    def get_user_by_email(db: Session, email: EmailStr):
        """
        Retorna um usuário do banco de dados a partir do email.
        Args:
            db (Session): Sessão ativa do SQLAlchemy.
            email: Email do usuário.
        Return
            User: instância do usuário criado.
        """
        try:
            user = db.query(User).filter(User.email==email).first()
            return user
        except SQLAlchemyError as erro:
            db.rollback()
            logger.error(f"Erro ao buscar usuário pelo email.")
        except Exception as e:
            raise

    def update_user(db: Session, userbase: UserBase, user_id: int):
        """
        Altera dados do usuário.
        Args:
            db (Session): Sessão ativa do SQLAlchemy.
            email: Email do usuário.
        Return
            User: instância do usuário com os dados modificados.
        """
        try:
            user = db.query(User).filter(User.id==user_id).first()
        except SQLAlchemyError as erro:
            db.rollback()
            logger.error(f"Erro ao buscar usuário pelo email.")
        
        if user:
            if userbase.nome:
                user.nome = userbase.nome
            if userbase.sobrenome:
                user.sobrenome = userbase.sobrenome

        db.commit()
        db.flush()

        return user

    def delete_user(db: Session, user_id: int):
        try:
            user = db.query(User).filter(User.id==user_id).first()
            return user
        except SQLAlchemyError as erro:
            db.rollback()
            logger.error(f"Usuário não encontrado.")
            raise HTTPException(f"Erro ao buscar usuário pelo email.", status_code=status.HTTP_404_NOT_FOUND)