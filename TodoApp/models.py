from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    author = Column(String(255))


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String(255))
    priority = Column(Integer)
    completed = Column(Boolean, default=False)