# app\main.py
from fastapi import FastAPI
from .settings import settings
from contextlib import asynccontextmanager
# from .routers import tanks
# from .database import Base, engine

# # Initialize database table
# Base.metadata.create_all(bind=engine)
  
@asynccontextmanager
async def lifespan(app: FastAPI):
  # 启动验证
  if not settings.JWT_SECRET_KEY or len(settings.JWT_SECRET_KEY) < 32:
    raise ValueError("JWT_SECRET_KEY must be at leat 32 characters long")
  yield
  # shutdoen 逻辑（如果有）

app = FastAPI(
  title="CoCresco Link Brain", 
  docs_url="/api/docs", 
  redoc_url="/api/redoc", 
  openapi_url="/api/openapi.json", 
  lifespan=lifespan   # 注册 lifespan
)

@app.get("/api")
def root():
  return {
    "message": "Welcome to CoCresco Link's Brain.",
    "JWT_SECRET_KEY": settings.JWT_SECRET_KEY,
    "DATABASE_URL": settings.DATABASE_URL,  
  }

# @app.on_event("startup")
# async def validate_secrets():
#   if not settings.JWT_SECRET_KEY or len(settings.JWT_SECRET_KEY) < 32:
#     raise ValueError("JWT_SECRET_KEY 必须 >= 32 字符")

# # Register the router of module tanks to main app
# app.include_router(tanks.router)
