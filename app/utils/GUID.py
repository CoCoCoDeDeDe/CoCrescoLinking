# app\utils\GUID.py

import uuid
from sqlalchemy.types import TypeDecorator, CHAR, BLOB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.dialects.sqlite import BLOB as SQLiteBLOB

class GUID(TypeDecorator):
  """"
  平台独立的 GIUD 类型。
  - 在 PostgreSQL 中使用原生的 UUID 类型
  - 在 SQLite 中使用 16 字节的 BLOB 存储
  """
  impl = SQLiteBLOB
  cache_ok = True
  
  def load_dialect_impl(self, dialect):
    if dialect.name == 'postgresql':
      return dialect.type_descriptor(PG_UUID())
    else:
      return dialect.type_descriptor(SQLiteBLOB(16))
    
  def process_bind_param(self, value, dialect):
    if value is None:
      return value
    if dialect.name == 'postgresql':
      return str(value)
    else:
      if not isinstance(value, uuid.UUID):
        value = uuid.UUID(value)
      return value.bytes
    
  def process_result_value(self, value, dialect):
    if value is None:
      return value
    if not isinstance(value, uuid.UUID):
      return uuid.UUID(bytes=value)
    return value
