"""
Модели для отчетов
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship

from src.database.base import Base

class WorkReport(Base):
    __tablename__ = 'work_reports'

    id = Column(Integer, primary_key=True)
    report_date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    total_tasks = Column(Integer)
    total_time = Column(Integer)  # в минутах
    report_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Отношения
    user = relationship('User', back_populates='work_reports')

class ProjectReport(Base):
    __tablename__ = 'project_reports'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    report_date = Column(Date, nullable=False)
    total_tasks = Column(Integer)
    completed_tasks = Column(Integer)
    total_time = Column(Integer)  # в минутах
    milestone_status = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Отношения
    project = relationship('Project', back_populates='reports')

class ClientReport(Base):
    __tablename__ = 'client_reports'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    report_date = Column(Date, nullable=False)
    total_projects = Column(Integer)
    total_tasks = Column(Integer)
    total_time = Column(Integer)  # в минутах
    created_at = Column(DateTime, default=datetime.utcnow)

    # Отношения
    client = relationship('Client', back_populates='reports')
