# app\database.py

'''
Task: Offer engine, SessionLocal, Base
'''

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

DATABASE_URL = "postgresql+asyncpg://ccl_commander:mypassword@localhost:5432/CoCrescoLinking_db"

# Create async engine
engine = create_async_engine(
  DATABASE_URL,
  echo=True,         # To check SQL sentences
  poolclass=NullPool
)

# Async SessionLocal
AsyncSessionLocal = async_sessionmaker(
  bind=engine,
  class_=AsyncSession,
  expire_on_commit=False,
)

class Base(DeclarativeBase):
  # This is a private namespace, has its own MetaData object, to manage its tables
  # Declarativebase is public namespace for all tables
  pass
