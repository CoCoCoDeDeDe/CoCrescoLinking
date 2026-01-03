# app\database.py

# Main Task: Use Base to create models for SQLAlchemy

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Table
from .database import Base
from sqlalchemy.orm import relationship
import enum

class Tank(Base):
  __tablename__ = "tanks"
  
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  temperature = Column(Float)
  ph_level = Column(Float)

class PointType(enum.Enum):
  INPUT = "input"
  OUTPUT = "output"
  
class Device(Base):
  __tablename__ = "devices"
  id = Column(Integer, primary_key=True)
  name = Column(String)
  points = relationship("DataPoint", back_populates="device")
  
group_point_mapping = Table(
  "group_point_mapping",
  Base.metadata,
  Column("group_id", Integer, ForeignKey("group.id"), primary_key=True),
  Column("point_id", Integer, ForeignKey("data_points.id"), primary_key=True)
)
  
class DataPoint(Base):
  __tablename__ = "data_points"
  id = Column(Integer, primary_key=True)
  device_id = Column(Integer, ForeignKey("devices.id")) # Indicates its the multiple side in the one-to-multiple relationshipe with device
  name = Column(String)
  point_type = Column(Enum(PointType))
  
  device = relationship("Device", back_populates="points")
  # Multiple-to-Multiple relationshipe with Group
  groups = relationship("Group", secondary="group_point_mapping", back_populates="points")
  
class Group(Base):
  __tablename__ = "group"
  id = Column(Integer, primary_key=True)
  name = Column(String)
  user_id = Column(Integer)
  
  # Recombination of points in logical
  points = relationship("DataPoint", secondary="group_point_mapping", back_populates="groups")
