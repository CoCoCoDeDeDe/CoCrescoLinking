<!-- app\database.md -->

主要风格：SQLAlchemy 2.0+ Async
主要功能：
  - 构建 数据库连接
  - ORM 基础结构
主要目标：
  - 提供一个异步数据库引擎（`engine`）
  - 提供一个可复用的异步会话工厂（`AsyncSessionLocal`）
  - 提供一个ORM基类（`Base`），用于声明式定义数据模型
  - 提供一个依赖注入函数（`get_db`），用于 FastAPI 等框架中获取数据库会话

# 异步会话工厂 `AsyncSessionLocal`
```
AsyncSessionLocal = async_sessionmaker(
  bind=engine,
  class_=AsyncSession,
  expire_on_commit=False
)
```
- `AsyncSessionLocal`：一个可调用对象（callable），用于创建新的`AsyncSession`实例
- 关键参数：
  - `bind=engine`：绑定异步引擎
  - `class_=AsyncSession`：明确使用异步会话类。显式指定更安全
  - `expire_on_commit=False`：
    - 默认为`True`，提交事务后对象属性会被“过期”，下次访问需要重新从 DB 加载
    - 设置为`False`可以避免在提交后立即访问对象时报错
      - 例如场景：Web API 返回刚刚提交创建的新对象
- `AsyncSessionLocal()`每次调用都会返回一个新的、独立的数据库会话（session）

# ORM 声明式基类 `Base`
```
class Base(DeclarativeBase):
  pass
```
- 作用：所有数据模型都继承自`Base`
- 机制：
  - `DeclarativeBase`自动管理元数据（`MetaData`），收集所有继承它的类所定义的表结构
  - 提供`Base.metadata.create_all(engine)`可以自动建表（需要在初始化时调用）
- 命名规范：通常命名为`Base`，是 SQLAlchemy 声明式风格的标准做法

# 依赖注入生成器 `get_db()`
```
async def get_db():
  db = await AsyncSessionLocal()
  try:
    yield db
  finally:
    await db.close()
```
- 作用：提供一个**上下文管理式的数据库会话**，确保每次请求结束后自动关闭连接
- 工作流程：
  1. 调用`AsyncSessionLocal()`创建新会话
  2. `yield db`将会话交给调用者
  3. 请求处理完毕后，执行`finally`快，**显式关闭会话**（释放连接）
- 为什么用`tield`？
  - 这是 Python 的**生成器函数**，配合 FastAPI 的`Depends()`实现依赖注入
  - 确保即使发生异常，也会执行`await db.close()`，防止连接泄漏
- `get_db`本身不是会话，而是一个**异步生成器函数**，用于提供和管理会话的生成和关闭
