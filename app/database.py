# app\database.py

'''
Task: Offer engine, SessionLocal, Base
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite:///./db/apuarium.db"

# connect_args={"check_same_thread": False} is necessary for SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autoflush=False, bind=engine)

class Base(DeclarativeBase):      # Replace Base = declarative_base(), to get better hint
  pass
