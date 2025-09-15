"""
Модель для инвайт-кодов
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from src.database.base import Base

class Invitation(Base):
    """
    Модель для хранения инвайт-кодов
    """
    __tablename__ = 'invitations'

    id = Column(Integer, primary_key=True)
    code = Column(String(6), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_used = Column(Boolean, default=False)  # Флаг для отметки использованных кодов
