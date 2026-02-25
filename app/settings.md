# class Settings 的内部类 class Config
## 是什么
- 是 Pydantic（包括 BaseSettings）中用于**配置模型行为**的特殊内部类
  - 不是普通业务逻辑类，而是元配置容器
  - 用于告诉 Pydantic：
    - 从哪里加载配置
    - 如何解析字段
      - 如：是否忽略大小写
    - 是否允许额外字段
    - 等等

## Config 不会在 Settings 实例化时被实例化
- Config 只是一个类定义，Pydantic 在内部会读取这个类的属性（如 env_file，extra）
- Config 相当于一个**静态配置模版**，Pydantic 用它来知道如何加载和验证 Settings
- Config 是类级别的元数据，不是实例

## Config 是遵循 BaseSettings 的约定而建立的
- BaseSettings（来自 Pydantic-settings）专门设计为支持 Config 内部类，并且定义了可以识别的配置项
- 常见的 Config 属性：
  - env_file：指定 .env 文件路径
  - env_file_encoding：编码方式（如："utf-8"）
  - extra：控制是否允许未声明字段（"forbid"/"allow"/"ignore"）
  - case_sensitive：是否区分环境变量大小写（默认 False）

## 一个 Settings 实例同时读取多个文件
```
class Config:
  env_file = [BASE_DIR / ".env", BASE_DIR / ".env.local", BASE_DIR / ".env.prod"]
  env_file_encoding = "utf-8"
```
- 将要读取的文件的路径以数组方式传入 Config.env_file
- 版本要求：pydantic-settings >= 2.0

# Settings 读取全局变量（即系统环境变量）
- 默认会读取所有的系统环境变量
- 优先级：传入的初始化参数 > 系统环境变量 > 配置文件中的变量 > 字段默认值
  
# 传入初始化参数
```
Settings(DATABASE_URL="...")
```

# Field(...) 或 Field(Ellipsis)
- 将 ... 作为第一个参数传入给 Filed 作为 default 参数
  - 意味着：
    - 不给该属性赋默认值
    - 且该属性必须要提供（不管是通过初始化时提供、全局变量还是 env 文件等方法）
  - 若直接不提供 default 参数，则意味着该属性可选
- ... 是 Python 的内置**常量**，叫**Ellipsis（省略号）**
  - `type(...) is type(Ellipsis)`为`true`
- ... 完全等价于 Ellipsis
  - ... 是 Ellipsis 对象的**字面量**写法（syntactic sugar）
  - Ellipsis 是该对象的**内置名称**（built-in constant）
  - 普遍使用 ... 而非 Ellipsis

# __file__
## 是什么
- __file__ 是 Python 解释器自动为每个**模块（.py 文件）**注入的**内置变量**
  - 表示**当前脚本文件的路径**（相对于启动位置，可能是相对路径）

## Test Example
```
# /app/setting.py
print(__file__)
print(Path(__file__).resolve())
print(Path(__file__).resolve(True))
print(Path(__file__).resolve().parent)
print(Path(__file__).resolve().parent.parent)
```
Console:
```
D:\YYFCode\Project_AQAQ\AquaponicsAquarium\FastAPI\V1\FastAPI\app\settings.py
D:\YYFCode\Project_AQAQ\AquaponicsAquarium\FastAPI\V1\FastAPI\app\settings.py
D:\YYFCode\Project_AQAQ\AquaponicsAquarium\FastAPI\V1\FastAPI\app\settings.py
D:\YYFCode\Project_AQAQ\AquaponicsAquarium\FastAPI\V1\FastAPI\app
D:\YYFCode\Project_AQAQ\AquaponicsAquarium\FastAPI\V1\FastAPI
```

### 获取当前文件相对于其他文件的相对路径
```
current_file = Path(__file__).resolve()   # 保证获取绝对路径
target_file_path = current_file.parent.parent  # 具体获取方式取决于实际项目目录结构
relative_path = current_file.relative_to(target_file_path)
```
- `__file__`是当前文件的路径的纯字符串数据。可能是绝对路径，也可能是相对路径，取决于具体运行环境。
- 根据初始化时输入的路径字符串的形式不同，`Path(path)`得到的可能是相对也可能是绝对路径
  - 调用`resolve()`保证获取其绝对路径
    - 会解析 .. 和 .
    - `resolve()`的严格模式
      - 开启后（`resolve(True)`）（默认）：会检查文件系统，解析符号链接。当文件不存在可能报错
      - 关闭时（`resolve(False)`）：不访问文件系统，仅做路径字符串层面的规范化。即使文件不存在也能运行
- `Path(__file__)`将`__file__`转化为具有便捷功能的类

# `BASE_DIR / ".env"`中的`/`操作符
- `BASE_DIR / ".env"`这里的`/`是被`Path`类重写了的运算符，可以像拼接字符串一样拼接路径
  - 是`pathlib.Path`对象的**重载操作符**
- `BASE_DIR / ".env"`在正常运行下等价于`os.path.join(BASE_DIR, ".env")`
  - pathlib 提供的`/`更简洁，跨平台能力强

# Path
- 是 python 强大的文件系统操作工具
- 可以读写配置文件、日志文件、静态资源等等
- 完全适配各种操作系统
  - 强于 os.path
  - 注意 windows 文件系统不区分大小写，而 linux 区分
  - 某些接口在不同系统支持程度不同

## Example
```
current_file = Path(__file__).resolve()
target_file = current_file.parent.parent # FastAPI
target_file.write_text()
```

# 路径类型转换
## `pathlib`
- str -> Path：`Path("/a/b")`
- Path -> str：`str(Path("/a/b"))`
- 获取绝对路径：`Path("x").resolve()`
- 获取父目录：`Path("x/y").parent`
- 拼接路径：`Path("a") / "b" / "c"`
## os
- `os.path.join("a", "b")`
- `os/getcwd()`
- `os.path.abspath()`

# `Union[X, None]`、`Optional[X]`、`X | None`
- 这三个在语义上完全等价
  - 都表示：类型为`X`或者为`None`的可选值

## `Union[]`
- 来自于 Python 的`typing`模块（since Python 3.5+）
- 表示一个变量可以是列表中的任意一种类型
- 可以将类型元组解包赋给`Union`
  - 
```
from typing import Union
types = (int, str, float)
x: Union[*types]
```
  - 解包操作符`*`
  - Python >= 3.11

## `Optional[X]`
- 来自`typing`模块
- 定义：`Optional[X]`相当于`Union[X, None]`或`X | None`

## `X | None`
- since: Python 3.10
- **联合类型表达式**