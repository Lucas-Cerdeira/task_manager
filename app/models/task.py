from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database.database import Base

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, nullable=False)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    data_criacao = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'))
    completed = Column(Boolean, server_default='0')
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="tasks")

    def _repr_(self):
        return f"<Task(id={self.id}, nome='{self.titulo}')>"