from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,index = True)
    email = Column(String, unique=True,index = True)
    username = Column(String(100), unique=True,index = True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
    phone_number = Column(String)
    address_id = Column(Integer, ForeignKey('address.id'), nullable=True)
    todos = relationship("Todos", back_populates="owner")
    address = relationship("Address", back_populates="user_address")
class Todos(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="todos")


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, index=True)
    address1 = Column(String)
    address2 = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postalcode = Column(String)
    user_address = relationship("User", back_populates="address")
