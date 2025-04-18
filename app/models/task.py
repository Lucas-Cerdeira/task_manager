from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database.database import Base

class Tarefa(Base):
    _tablename_ = "tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    titulo = Column(String(100), nullable=False)
    descricao = Column(String(255))
    concluida = Column(Boolean, server_default='0')
    data_criacao = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'))

    owner = relationship("User", back_populates="tasks")

    def _repr_(self):
        return f"<Task(id={self.id}, nome='{self.titulo}')>"