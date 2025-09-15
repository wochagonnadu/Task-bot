"""
Модели для пользователей и команд
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import relationship

from src.database.db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=True)  # nullable для временных записей
    username = Column(String(255), nullable=True)  # Можно создать пользователя без username
    full_name = Column(String(255), nullable=True)  # Можно создать пользователя без полного имени
    role = Column(String(50), default='user')
    created_at = Column(DateTime, default=datetime.utcnow)

    # Отношения
    tasks_created = relationship('Task', back_populates='creator', foreign_keys='Task.creator_id')
    tasks_assigned = relationship('Task', back_populates='assignee', foreign_keys='Task.assignee_id')
    work_times = relationship('TaskTime', back_populates='user')
    work_reports = relationship('WorkReport', back_populates='user')

    def to_dict(self) -> dict:
        """
        Преобразование объекта в словарь
        """
        return {
            'id': self.id,
            'name': self.full_name or self.username or f"User {self.telegram_id}",
            'telegram_id': self.telegram_id,
            'username': self.username,
            'role': self.role
        }