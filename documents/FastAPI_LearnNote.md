<!-- documents\FastAPI_LearnNote.md -->

# Exp: `db_tank = models.Tank(**tank.model_dump())`
Situation:
```
@tank_router.post("tank/", response_model=schemas.Tank)
def create_tank(tank: schemas.TankCreate, db: Session = Depends(get_db)):
  db_tank = models.Tank(**tank.model_dump())
```
Processes:
  1. When call this HTTP API
    attach header: `Content-Type: application/json` is required
    [Send and Parse]
    the format of body should follows TankCreate (inherit BaseModel imported from pydantic).
      such as:
        {
          "name": "Tiger-I",
          "capacity": 500.5,
          "model_type": "Heavy Tank"
        }
      [Validation]this data will be validate by pydantic
      [Instantiation]After validating, FastAPI will creates an object instance of schemas.TankCreate and assign to tank as the parameter of create_tank()

# Router handler function parameter format
## Exp:
```
@tank_touter.post("/")
def create_tank(
  tank: schemas.TankCreate = Body(...),           # Body parameter
  db: Session = Depands(get_db),                  # Dependency injection
  current_user: User = Depends(get_current_user)  # Dependency injection
)
```
## 3 kinds of parameter of router handler function
1. **Path Parameter**: 
  Receive from URL
  Exp: `@router.get("/{tank_id}")`
  Type Limit: Allow simple type
2. **Query Parameter**:
  Receive from URL
  Exp: ``def get_tank(limit: int = 10)`
  Type Limit: Allow simple type
3. **Dependency Injection**:
  Receive when defining
  Exp: `db: Session = Depends(get_db)`
  Type Limit: Pydantic model (inherited from `class Base(DeclarativeBase)`)

## FastAPI recognize parameter's job by **Type Hints**

## Explicit Declaration
Exp:
  API Defination:
```
from fastapi import Body

@router.post("/update-name")
def update_name(name: str = Body(...)):
  return {"new_name": name}
```
  HTTP Request Body Format:
    JSON
    `{"name": "..."}`

## Recombination Body Parameter
Exp:
  API Defination:
```
  @router.post("/complex")
  def create_complex(tank: schemas.TankCreate, user: schemas.UserCreate):
  #...
  pass
```
  HTTP Request Body Format:
    JSON
```
{
  "tank": {...},
  "user": {...}
}
```
  Summary:
    if multiple pydantic model passed as parameters, FastAPI will expect to receive a recombination JSON combined by those models.

# Ellipsis (`...`) in Python
Name: Ellipsis, 省略号
Main Function: Tell program this parameter is Required, and has no default parameter.
Exps:
  - **Optional Parameter with default value:**
```
@router.post("/")
def create(name: str = Body("Default Name"))
```
  - **Optional Parameter with no default value (Could be None):**
```
@router.post("/")
def create(name: str | None = Body(None)):
```
  - **Required Parameter:**
  Must use `...` in this situation
```
@router.post("/")
def create(name: str = Body(..., min_length=3, description="Name of tank")) # optional parameters for Body()
```
  If miss this parameter, throw error 422

# FastAPI Framwork Data Model Combination
Soul: FastAPI is a "Clue Layer" basically, it translating and adapt different data models
## 3 Parts of the data format relay race
1. **From HTTP to Pydantic - Input Params Adaption**
Direction: `HTTP Request (JSON str)` -> `Python dict` -> `Pydantic object`
Modules: FastAPI, Pydantic
Adaptions:
  - JSON has only basic types: string, number, bool, array, object
  - Pydantic will cast those basic types into **Strong Type** of Python by force, like `datetime` object, `Enum` object, `EmailStr` object...
  - This process is start at JSON/dict, so `from_attributes` is not required
2. **From Pydantic to ORM - Adaption For Store**
Direction: `Pydantic object` -> `Python dict` -> `SQLAlchemy model instance`
Modules: Pydantic, SQLAlchemy
Adaptions:
  - Manually adaption: `models.Tank(**tank.model_dump())`
  - `model_dump()` convert `Pydantic obejct` into `dict`, `**` expands dict to the parameters that SQLAlchemy construct function needs.
Soul: unpack
3. **From ORM To Pydantic To HTTP - Output Params Adaption**
Direction: `SQLAlchemy model instance (object)` -> `Pydantic object` -> `JSON string`
Conflicts:
  - Data of **SQLAlchemy obejct** stores in **attributes**, access by `obj.name`
  - Data of **Pydantic object** stores in **dict key-value pairs**, access by `obj["name"]`
Adaption:
  - When weave this Pydantic class, add `class Config` as attribute, with attribute `from_attributes = True` inside.

# Cooperation Of SQLAlchemy And Pydantic
Soul Mindset: **Separation Of Concerns**
**Separation Of Concerns**:
  - **SQLAlchemy Model**: Face **Database**. Defines table structure, index, relationship
  - **Pydantic Model**: Face **Client (API User)**. Defines Input validation rules, output desensitization rules.
Adaption:
  - Enable Pydantic to read SQLAlchemy object attributes as dict key-value pairs.
      Config: When instantiating SQLAlchemy engine, pass parameter `connect_args={"check_same_thread": False}`
      | "thread" means 线程
        Exp:
          ```
          engine = create_engine("sqlite:///./db/sql_app.db", connect_args={
            "check_same_thread": False,
          })
          ```

# SQLAlchemy Connext Different Databases According To Connect Strings / Database URLs
## The way to connect:
```
engine = create_engine("sqlite:///./db/sql_app.db", connect_args={
  "check_same_thread": False
})
```
## The Database URLs
- **PostgreSQL**: `postgresql://user:password@localhost/dbname`
- **MySQL**: `mysql+pymysql://user:password@localhost/dbname`
- **SQL Server**: `mssql+pyodbc://user:password@dsn`
## The **Dialect** System Will Adapt Different Database Language
## SQLAlchemy Use ORM To Operate Table Like Operate Object
Access SQLAlchemy object data by attributes

# Alembic

# B-Tree

# Recombination Index