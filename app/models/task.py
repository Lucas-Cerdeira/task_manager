from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database.database import Base
from datetime import datetime

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, nullable=False)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(255))
    completed = Column(Boolean, server_default='0')
    data_criacao = Column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    data_entrega = Column(TIMESTAMP(timezone=True), nullable=True, default=text("NULL"))
    diaria = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="tasks")

    def _repr_(self):
        return f"<Task(id={self.id}, nome='{self.titulo}')>"