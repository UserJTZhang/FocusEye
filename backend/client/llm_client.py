"""
LLM 客户端模块
封装 LangChain ChatOpenAI 实例，适配 Qwen-VL 服务
"""
from typing import Optional
from langchain_openai import ChatOpenAI
from backend.config import settings


class LLMClient:
    """LLM 客户端管理类"""
    
    _instance: Optional[ChatOpenAI] = None
    
    @classmethod
    def get_client(cls) -> ChatOpenAI:
        """
        获取 ChatOpenAI 客户端实例（单例模式）
        
        Returns:
            ChatOpenAI: 配置好的 LLM 客户端
        """
        if cls._instance is None:
            cls._instance = cls._create_client()
        
        return cls._instance
    
    @classmethod
    def _create_client(cls) -> ChatOpenAI:
        """
        创建 ChatOpenAI 客户端实例
        
        配置要点：
        1. base_url: 指向 Qwen-VL 服务地址
        2. api_key: 使用配置的 API Key
        3. model: 指定模型名称 qwen3-vl:32b
        4. timeout: 设置请求超时时间
        
        Returns:
            ChatOpenAI: 新创建的客户端实例
        """
        # 确保配置有效
        settings.validate()
        
        # 初始化 ChatOpenAI 客户端
        client = ChatOpenAI(
            base_url=settings.API_BASE,
            api_key=settings.API_KEY,
            model=settings.MODEL_NAME,
            timeout=settings.REQUEST_TIMEOUT,
            temperature=0.5,  # 控制输出的随机性
            max_tokens=500,   # 限制输出长度
            # default_headers={
            #         "Authorization": settings.API_KEY  # 直接覆盖Authorization头
            #     }
        )
        
        return client
    
    @classmethod
    def reset_client(cls) -> None:
        """重置客户端实例（用于测试或配置更新）"""
        cls._instance = None


# 便捷函数：获取客户端
def get_llm_client() -> ChatOpenAI:
    """
    获取 LLM 客户端实例
    
    Returns:
        ChatOpenAI: 配置好的客户端
    """
    return LLMClient.get_client()
