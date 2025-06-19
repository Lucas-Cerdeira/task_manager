from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from app.schemas.task import TaskCreate
from app.models.task import Task
from app.models.user import User


logger = logging.getLogger(__name__)


class TaskDbServices():
    
    @staticmethod
    def create_task(db: Session, task: TaskCreate, user_id: int):
        """
        Cria uma nova task.
        Args:
            db (Session): Sessão ativa do SQLAlchemy.
            task: Dados válidos da task.
            user_id: Id do usuário.
        Returns:
            task: Schema da task criada
        """

        try:
            new_task: Task = Task(**task.model_dump(), user_id=user_id)
            db.add(new_task)
            db.commit()
            db.flush()
            return new_task
        
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Erro ao criar usuário: {str(e)}")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Erro ao criar usuário no banco de dados: Dados duplicados.")

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Erro ao criar usuário: {str(e)}")
            raise Exception("Erro ao criar usuário no banco de dados.")
        
        except Exception as e:
            raise e
        
    @staticmethod
    def get_tasks_by_user_id(db: Session, user_id: int):
        """
        Retorna todas as tasks de um usuário:
        Args:
            db (Session): Sessão ativa do SQLAlchemy. 
            user_id: Id do usuário.
        Returns:
            tasks: Lista com todas as tarefas.
        """
        try:
            user = db.query(User).filter(User.id==user_id).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")
            tasks = user.tasks
            return tasks
        
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Erro ao pegar tasks: {e}")
            raise SQLAlchemyError(f"Erro ao pegar tasks: {e}")
        
        except Exception as e:
            raise e
    
    @staticmethod    
    def update_tasks(db: Session, task_id: int, nome: str = None, descricao: str = None):
        try:
            task = db.query(Task).filter(Task.id==task_id).first()
        except SQLAlchemyError as erro:
            db.rollback()
            logger.error(f"Erro ao pegar tasks: {erro}")
            raise SQLAlchemyError(f"Erro ao pegar tasks: {erro}")
        
        if task:
            if nome:
                task.nome = nome
            if descricao:
                task.descricao = descricao
        return task

    @staticmethod
    def delete_task(db: Session, user_id: int, task_id: int):
        """
        Deleta uma task de um usuário específico.
        Args:
            db (Session): Sessão ativa do SQLAlchemy.
            user_id: Id do usuário.
            task_id: Id da task.
        Returns:
            task: A task deletada.
        """
        try:
            task = db.query(Task).filter(Task.id==task_id, Task.user_id==user_id).first()
            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
            db.delete(task)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Erro ao deletar task: {str(e)}")
            raise HTTPException(status_code=status.HTTP_200_OK, detail="Erro ao deletar task.")
        except Exception as e:
            raise e
        return task