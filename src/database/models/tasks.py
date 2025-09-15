"""
Модели для задач и учета времени
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Time, ForeignKey, event
from sqlalchemy.orm import relationship, validates

from src.database.db import Base

class Task(Base):
    __tablename__ = 'tasks'

    # Статусы задач
    STATUS_NOT_STARTED = 'not_started'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'

    VALID_STATUSES = [
        STATUS_NOT_STARTED,
        STATUS_IN_PROGRESS,
        STATUS_COMPLETED
    ]

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default=STATUS_NOT_STARTED)
    creator_id = Column(Integer, ForeignKey('users.id'))
    assignee_id = Column(Integer, ForeignKey('users.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Отношения
    creator = relationship('User', back_populates='tasks_created', foreign_keys=[creator_id])
    assignee = relationship('User', back_populates='tasks_assigned', foreign_keys=[assignee_id])
    client = relationship('Client', back_populates='tasks')
    project = relationship('Project', back_populates='tasks')
    times = relationship('TaskTime', back_populates='task')

    @validates('status')
    def validate_status(self, key, status):
        """Проверка валидности статуса"""
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Некорректный статус задачи: {status}")
        return status

    @property
    def deadline(self):
        """Свойство для обратной совместимости с кодом, использующим deadline вместо due_date"""
        return self.due_date

    @property
    def is_active(self):
        """Проверка, является ли задача активной"""
        return self.status in [self.STATUS_NOT_STARTED, self.STATUS_IN_PROGRESS]

    @property
    def can_be_started(self):
        """Проверка, можно ли начать работу над задачей"""
        return self.status == self.STATUS_NOT_STARTED

    @property
    def can_be_completed(self):
        """Проверка, можно ли завершить задачу"""
        return self.status == self.STATUS_IN_PROGRESS

    def start_task(self):
        """Начать работу над задачей"""
        if not self.can_be_started:
            raise ValueError("Невозможно начать работу над задачей в текущем статусе")
        self.status = self.STATUS_IN_PROGRESS

    def complete_task(self):
        """Завершить задачу"""
        if not self.can_be_completed:
            raise ValueError("Невозможно завершить задачу в текущем статусе")
        self.status = self.STATUS_COMPLETED

class TaskTime(Base):
    __tablename__ = 'task_times'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    work_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time)
    status = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Отношения
    task = relationship('Task', back_populates='times')
    user = relationship('User', back_populates='work_times')

# События SQLAlchemy для автоматического создания записи TaskTime
@event.listens_for(Task, 'after_update')
def task_status_changed(mapper, connection, target):
    """Создание записи TaskTime при изменении статуса задачи"""
    if target.status == Task.STATUS_IN_PROGRESS:
        # Создаем запись о начале работы
        now = datetime.now()
        connection.execute(
            TaskTime.__table__.insert().values(
                task_id=target.id,
                user_id=target.assignee_id,
                work_date=now.date(),
                start_time=now.time(),
                status='started'
            )
        )
    elif target.status == Task.STATUS_COMPLETED:
        # Завершаем последнюю запись о работе
        now = datetime.now()
        latest_time = connection.execute(
            TaskTime.__table__.select()
            .where(TaskTime.task_id == target.id)
            .order_by(TaskTime.id.desc())
            .limit(1)
        ).first()
        
        if latest_time and not latest_time.end_time:
            connection.execute(
                TaskTime.__table__.update()
                .where(TaskTime.id == latest_time.id)
                .values(
                    end_time=now.time(),
                    status='completed'
                )
            )