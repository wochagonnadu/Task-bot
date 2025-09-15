"""
Модели для клиентов и проектов
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship

from src.database.base import Base

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Отношения
    projects = relationship('Project', back_populates='client')
    tasks = relationship('Task', back_populates='client')
    reports = relationship('ClientReport', back_populates='client')

    def to_dict(self) -> dict:
        """
        Преобразование объекта в словарь
        """
        return {
            'id': self.id,
            'name': self.name
        }

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'))
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(50), default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Отношения
    client = relationship('Client', back_populates='projects')
    tasks = relationship('Task', back_populates='project')
    reports = relationship('ProjectReport', back_populates='project')

    def to_dict(self) -> dict:
        """
        Преобразование объекта в словарь
        """
        return {
            'id': self.id,
            'name': self.name,
            'client_id': self.client_id,
            'description': self.description,
            'status': self.status
        }
