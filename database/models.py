# Modelos de la base de datos
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import String, Integer, Text, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import Table
from sqlalchemy.sql import func

# Importamos el declarative_base para crear las tablas físicas
from database.database import Base
from schemes import StatusType

# La tabla pivote la declaramos antes de referenciarla en la tabla de tareas
task_tag = Table(
    'task_tag',
    Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(20), unique=True)
    description = Column(Text())
    status = Column(Enum(StatusType))
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    category = relationship('Category', lazy='joined', back_populates='tasks')
    user = relationship('User', lazy='joined', back_populates='tasks')

    # Ahora referenciamos la tabla pivote que para eso la declaramos antes de esta linea
    tags = relationship('Tag', secondary=task_tag, back_populates='tasks')


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True)

    tasks = relationship('Task', back_populates='category', lazy='joined')


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    surname = Column(String(100))
    email = Column(String(100))
    website = Column(String(100))
    hashed_password = Column(String(255))

    tasks = relationship('Task', back_populates='user', lazy='joined')


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True)

    tasks = relationship('Task', secondary=task_tag, back_populates='tags')


class AccessToken(Base):
    __tablename__ = "access_tokens"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    access_token = Column(String(255))
    expiration_date = Column(DateTime(timezone=True))
    user = relationship('User', lazy='joined')
