# app\routers\tanks.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..main import get_db

router = APIRouter(
  prefix="/tanks",
  tags=["鱼缸管理"],
)

@router.post("/", response_model=schemas.Tank)
def create_tank(tank: schemas.TankCreate, db: Session = Depends(get_db)):
  db_tank = models.Tank(**tank.model_dump())    # Argument unpacking inputed tank data. model_dump() returns a py dict data. ** will unpack dict as key arguments.
  db.add(db_tank)
  db.commit()
  db.refresh(db_tank)
  return db_tank

@router.get("/", response_model=list[schemas.Tank])
def read_tanks(db: Session = Depends(get_db)):    # 注入函数，解耦功能的实现
  return db.query(models.Tank).all()
