from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.database.database import Base


class User(Base):
    _tablename_ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    sobrenome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha_hash = Column(String(20), nullable=False)

    tasks = relationship("Task", back_populates="owner")

    def _repr_(self):
        return f"<User(id={self.id}, nome='{self.nome}', email='{self.email}')>"