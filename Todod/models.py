from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from database import Base

class Todos(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)



