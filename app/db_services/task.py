from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.schemas.task import TaskCreate
from app.models.task import Task
from app.models.user import User


logger = logging.getLogger(__name__)


class TaskDbServices():

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
            new_task: TaskCreate = TaskCreate(**task.model_dump(), user_id=user_id)
            db.add(new_task)
            db.commit()
            db.flush()
        
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Erro ao criar usuário: {str(e)}")
            raise Exception("Erro ao criar usuário no banco de dados.")
        
        except Exception as e:
            raise e
        

    def get_task_by_user(db: Session, user_id: int):
        try:
            user = db.query(User).filter(User.id==user_id).first()
            tasks = user.tasks
            return tasks
        
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Erro ao pegar tasks: {e}")
            raise SQLAlchemyError(f"Erro ao pegar tasks: {e}")
        
        except Exception as e:
            raise e