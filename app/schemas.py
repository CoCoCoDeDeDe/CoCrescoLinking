# app\schemas.py

from pydantic import BaseModel
from typing import List, Optional
from .models import PointType

class TankBase(BaseModel):
  name: str
  temperature: float
  ph_level: float
  
class TankCreate(TankBase):
  pass

class Tank(TankBase):
  id: int

  class Config:
    from_attributes = True  # Allow Pydanyic (dict) read SQLAlchemy model (object)
    
# DataPoint
class DataPointBase(BaseModel):
  name: str
  point_type: PointType

# DataPoint when creating
class DataPointCreate(DataPointBase):
  pass

# Device
class DeviceCreate(BaseModel):
  name: str
  points: List[DataPointCreate] = []  # A list of DataPoint object
