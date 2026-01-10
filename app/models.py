# app\database.py

# Main Task: Use Base to create models for SQLAlchemy

import uuid
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base
import enum
from .utils.GUID import GUID

try:
  from uuid import uuid7
except ImportError:
  from uuid6 import uuid7

class PointType(enum.Enum):
  INPUT = "input"
  OUTPUT = "output"
  
class DeviceStatus(str, enum.Enum):
  # Connection
  ONLINE = "online"
  OFFLINE = "offline"
  UNACTIVATED = "unactivated"
  SCRAPPED = "scrapped"
  # Business
  IDLE = "idle"
  BUSY = "busy"
  FAULT = "fault"
  UPGRADING = "upgrading"
  
group_device_mapping = Table(
  "group_device_mapping",
  Base.metadata,
  Column("group_id", Integer, ForeignKey("device_groups.id"), primary_key=True),
  Column("device_id", Integer, ForeignKey("devices.id"), primary_key=True)
)

group_point_mapping = Table(
  "group_point_mapping",
  Base.metadata,
  Column("group_id", Integer, ForeignKey("data_point_groups.id"), primary_key=True),
  Column("point_id", Integer, ForeignKey("data_points.id"), primary_key=True)
)
  
class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True)
  name = Column(String, index=True, nullable=False)
  devices = relationship("Device", back_populates="owner", cascade="all, delete-orphan")
  device_groups = relationship("DeviceGroup", back_populates="owner", cascade="all, delete-orphan")
  point_groups = relationship("DataPointGroup", back_populates="owner", cascade="all, delete-orphan")
  
class Device(Base):
  __tablename__ = "devices"
  id = Column(Integer, primary_key=True)
  name = Column(String, index=True, nullable=False)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  
  __table_args__ = (
    UniqueConstraint('user_id', 'name', name='_user_device_uc'),  # Append a ',' if a tuple has only one item, in case it cant be recognize as a tuple
  )
  
  owner = relationship("User", back_populates="devices")
  points = relationship("DataPoint", back_populates="device", cascade="all, delete-orphan")
  groups = relationship("DeviceGroup", secondary="group_device_mapping", back_populates="devices")
  
class DataPoint(Base):
  __tablename__ = "data_points"
  id = Column(Integer, primary_key=True)
  device_id = Column(Integer, ForeignKey("devices.id"), nullable=False) # Indicates its the multiple side in the one-to-multiple relationshipe with device
  name = Column(String, index=True, nullable=False)
  point_type = Column(Enum(PointType))
  
  device = relationship("Device", back_populates="points")
  # Multiple-to-Multiple relationshipe with Group
  groups = relationship("DataPointGroup", secondary="group_point_mapping", back_populates="points")
  
class GroupMixin(Base):
  __abstract__ = True   # Tell SQLAlchemy dont build table for this class
  
  id = Column(Integer, primary_key=True)
  name = Column(String, index=True, nullable=False)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  
  
  
class DeviceGroup(GroupMixin):
  __tablename__ = "device_groups"
  
  owner = relationship("User", back_populates="device_groups")
  devices = relationship("Device", secondary="group_device_mapping", back_populates="groups")

class DataPointGroup(GroupMixin):
  __tablename__ = "data_point_groups"
  
  owner = relationship("User", back_populates="point_groups")
  # Recombination of points in logical
  points = relationship("DataPoint", secondary="group_point_mapping", back_populates="groups")
  