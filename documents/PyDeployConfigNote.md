
# 启动
## 热重载
`uvicorn main:app --reload`
- `main:app`表示从`main.py`文件中导入`app`对象
- `--reload`会在代码变更时自动重启服务（only dev env）
`uvicorn main:app --host 0.0.0.0 --port 8000`
- `--host 0.0.0.0` 监听所有可用 IP 接口

# `uvicorn`
- `uvicorn` 高性能 ASGI 服务器
- ASGI: Asynchronous Server Gateway Interface
- 用于运行异步 Python 应用（框架）。包括：
  - FastAPI
  - Starlette
  - Quart （异步版本 Flask）
特点：
- 完全支持异步/await。基于`asyncio`
- 支持热重载（`--reload`）（HMR）
- 符合 ASGI 标准（类似 WSGI，但支持异步）

## 开发部署步骤
1. 安装
`pip install fastapi uvicorn[standard]`
2. 创建`main.py`
```
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
  return {"message": "Hello from Uvicorn!"}
```
3. 启动开发服务器
`uvicorn main:app --reload --host 0.0.0.0 --port 8000`

## 常用参数
- `--host` 监听地址配置
- `--port`
- `--reload`
- `--workers` 工作进程数量配置（仅生产环境进行可配置大于1）

## Dev & Product Env
| Scene       | 开发环境         | 生产环境                        |
| :---------- | :--------------- | :------------------------------ |
| `--reload`  | 开启             | 禁用                            |
| `--workers` | 1                | >= 2（多核）                    |
| `--host`    | `0.0.0.0`        | `0.0.0.0`（配合反向代理）       |
| 日志        | 详细             | 结构化 + 收集                   |
| 服务器      | 直接用 `Uvicorn` | Uvicorn + Gunicorn 或纯 Uvicorn |

### Dev Env Deployment
```
# 单进程（小项目）
uvicorn main:app --host 0.0.0.0 --port 8000

# 多进程（用 Gunicorn 管理 Uvicorn workders）
gunicorn -k uvicorn.workers.UvicornWorker main:app -w 4 -b 0.0.0.0:8000
```
生产环境不要暴露 Uvicorn 直接对外，建议前面加 Nginx 做反向代理、SSL 终止等等。

## 启动方式标准化
1. 使用 `pyproject.toml`、`Makefile`命令或`run_dev.py`/`run_prod.py`脚本
  - `run_dev.py`
```
# run_dev.py
import uvicorn

if __name__ == "__main__":
  uvicorn.run(
    "src.main:app",
    host="0.0.0.0",
    port=8000,
    reload=True,
    log_level="debug"
  )
```
2. 运行脚本
`python run_dev.py`

