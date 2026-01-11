"""
配置管理模块
加载环境变量并提供配置常量
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """应用配置类"""
    
    # AI 服务配置
    API_KEY: str = os.getenv("API_KEY", "apikey")
    API_BASE: str = os.getenv("API_BASE", "https://igw.livzon.cn/ai/qwenvl/v1")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "qwen3-vl:32b")
    
    # 监督配置
    MONITOR_INTERVAL: int = int(os.getenv("MONITOR_INTERVAL", "20"))
    
    # 图片处理配置
    MAX_IMAGE_SIZE: int = int(os.getenv("MAX_IMAGE_SIZE", "800"))
    IMAGE_QUALITY: float = float(os.getenv("IMAGE_QUALITY", "0.5"))
    
    # 超时配置
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    
    @classmethod
    def validate(cls) -> bool:
        """验证必要配置是否存在"""
        required = ["API_KEY", "API_BASE", "MODEL_NAME"]
        missing = [key for key in required if not getattr(cls, key)]
        
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        
        return True


# 创建全局配置实例
settings = Settings()

# 导出配置常量（向后兼容）
API_KEY = settings.API_KEY
API_BASE = settings.API_BASE
MODEL_NAME = settings.MODEL_NAME
MONITOR_INTERVAL = settings.MONITOR_INTERVAL
MAX_IMAGE_SIZE = settings.MAX_IMAGE_SIZE
IMAGE_QUALITY = settings.IMAGE_QUALITY
REQUEST_TIMEOUT = settings.REQUEST_TIMEOUT
