<!-- documents\FileStructure.md -->
.
|-- .venv/                  <-- Virtual env directory (generate automatically)
|
|-- app/
|   |-- routers/
|   |   |-- __init__.py     <-- As a mark to tell this is the main app folder. Can be used to simplify import path
|   |   |-- tanks.py        <-- Routers about tanks
|   |
|   |-- __init__.py         <-- aka
|   |-- database.py         <-- Connect DB
|   |-- main.py             <-- Assemble
|   |-- models.py           <-- Define SQLAlchemy models
|   |-- schemas.py          <-- Pydantic schemas
|
|-- documents               <-- Explanation files
|   |-- FileStructure.md    <-- This file. Explain file structure
|
|-- .gitignore              <-- aka
|-- requirements.txt        <-- requirement packages
