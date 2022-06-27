from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQL_URL = "sqlite:///./todo.db"
SQL_URL = 'postgresql://postgres:2020@localhost/yaseen'

engine = create_engine(
    SQL_URL,
)
# engine = create_engine(
#     SQL_URL, connect_args={"check_same_thread": False}
# )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

