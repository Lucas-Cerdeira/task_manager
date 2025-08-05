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
            db.refresh(new_task)
            return new_task
        
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Erro ao criar usuário: {str(e)}")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Erro ao criar task no banco de dados: Dados duplicados.")

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
    def update_task(db: Session, task_id: int, user_id: int, task_data: dict):
        """
        Atualiza uma tarefa existente.
        Args:
            db (Session): Sessão ativa do SQLAlchemy.
            task_id: Id da tarefa a ser atualizada.
            user_id: Id do usuário dono da tarefa.
            task_data: Dicionário com os campos a serem atualizados.
        Returns:
            Task: A tarefa atualizada.
        """
        try:
            task = db.query(Task).filter(
                Task.id == task_id,
                Task.user_id == user_id
            ).first()

            if not task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found or doesn't belong to the user"
                )
            
            # Atualiza apenas os campos fornecidos
            for field, value in task_data.items():
                if value is not None:  # Só atualiza se o valor não for None
                    setattr(task, field, value)
            
            db.commit()
            db.refresh(task)
            return task

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Erro ao atualizar task: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar task."
            )
        except Exception as e:
            raise e

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
            return task  # Retorna a task deletada para garantir compatibilidade com o response_model TaskResponse
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Erro ao deletar task: {str(e)}")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Erro ao deletar task.")
        except Exception as e:
            raise e