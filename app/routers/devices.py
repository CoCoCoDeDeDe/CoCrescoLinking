# app\routers\devices.py

from fastapi import APIRouter
from sqlalchemy.orm import Session
from ..schemas import DeviceCreate
from ..models import Device

devices_router = APIRouter(
  prefix="/devices",
  tags=["鱼缸管理"]
)

@devices_router.post("/")
def create_device(device_data: DeviceCreate, db: Session):
  new_deivce = Device()

