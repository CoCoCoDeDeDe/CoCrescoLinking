# app\main.py

from fastapi import FastAPI
# from .routers import tanks
# from .database import Base, engine
# from . import database

# # Initialize database table
# Base.metadata.create_all(bind=engine)

# # Database dependencies
# def get_db():
#   db = database.SessionLocal()
#   try:
#     yield db
#   finally:
#     db.close()
    

app = FastAPI(title="My_App")

# # Register the router of module tanks to main app
# app.include_router(tanks.router)

# @app.get("/")
# def root():
#   return {"message": "Welcome to use AQAQ Sys."}
