# app\settings.py
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

# 获取 settings.py 所在目录的父目录 - 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
  DATABASE_URL: str = Field(Ellipsis, description="PostgreSQL 连接串")
  JWT_SECRET_KEY: str = Field(Ellipsis, min_length=32)
  
  THIRD_PARTY_API_KEY: Optional[str] = None
  
  DEBUG: bool = Field(False, description="是否开启调试模式")
  ENVIRONMENT: str = Field("production", description="允许环境")
  
  class Config:
    env_file = BASE_DIR / ".env"
    env_file_encoding = "utf-8"
    extra = "forbid"    # 拒绝未声明的环境变量
    
  def safe_dict(self) -> dict:
    """返回脱敏配置（用于健康检测）"""
    return {
      "debug": self.DEBUG,
      "environment": self.ENVIROMENT,
      # 故意不返回任何密钥字段
    }
    
settings = Settings()