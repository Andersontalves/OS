from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class User(Base):
    """User model for authentication and role management"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # admin, monitoramento, execucao, campo
    telegram_id = Column(BigInteger, unique=True, nullable=True, index=True)
    nome = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    ordens_abertas = relationship(
        "OrdemServico",
        foreign_keys="OrdemServico.tecnico_campo_id",
        back_populates="tecnico_campo"
    )
    ordens_executadas = relationship(
        "OrdemServico",
        foreign_keys="OrdemServico.tecnico_executor_id",
        back_populates="tecnico_executor"
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
