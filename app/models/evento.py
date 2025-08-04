from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from app.database.database import Base
from datetime import datetime

class Evento(Base):
    __tablename__ = "evento"

    id = Column(Integer, primary_key=True, nullable=False)
    titulo = Column(String(100), nullable=False)
    descricao = Column(String(255))
    local = Column(String(255), nullable=False)
    data_evento = Column(TIMESTAMP(timezone=True), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="eventos")

    def __repr__(self):
        return f"<Evento(id={self.id}, titulo='{self.titulo}', data_evento='{self.data_evento}')>"
