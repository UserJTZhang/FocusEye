"""
Supervisor Agent 实现
定义完整的监督 Chain：Prompt | LLM | Output Parser
"""
from typing import Dict, Any, Optional
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser
from backend.client import get_llm_client
from backend.Agent.prompts import (
    SupervisorResponse,
    get_system_prompt,
    create_user_message
)


class SupervisorAgent:
    """学习监督 Agent"""
    
    def __init__(self):
        """初始化 Agent"""
        self.llm = get_llm_client()
        self.output_parser = PydanticOutputParser(pydantic_object=SupervisorResponse)
        
    def analyze(
        self, 
        image_base64: str, 
        stats: Optional[Dict[str, Any]] = None
    ) -> SupervisorResponse:
        """
        分析用户状态
        
        Args:
            image_base64: Base64 编码的图片
            stats: 监督统计信息
            
        Returns:
            SupervisorResponse: 结构化的分析结果
            
        Raises:
            ValueError: 图片格式错误
            Exception: LLM 调用失败
        """
        try:
            # 构建消息
            messages = self._build_messages(image_base64, stats)
            
            # 调用 LLM
            response = self.llm.invoke(messages)
            
            # 解析输出
            result = self._parse_response(response.content)
            
            return result
            
        except Exception as e:
            # 返回默认错误响应
            return SupervisorResponse(
                status="error",
                message=f"分析失败：{str(e)[:20]}",
                confidence=0.0
            )
    
    def _build_messages(
        self, 
        image_base64: str, 
        stats: Optional[Dict[str, Any]]
    ) -> list:
        """
        构建完整的消息链
        
        Args:
            image_base64: 图片 Base64
            stats: 统计信息（包含 scene 字段）
            
        Returns:
            list: 消息列表
        """
        # 获取场景
        scene = stats.get('scene', 'reading') if stats else 'reading'
        
        # System Message（根据场景生成）
        system_prompt = get_system_prompt(scene)
        system_prompt += f"\n\n{self.output_parser.get_format_instructions()}"
        
        # User Message (包含图片和统计信息)
        user_content = create_user_message(image_base64, stats)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_content)
        ]
        
        return messages
    
    def _parse_response(self, content: str) -> SupervisorResponse:
        """
        解析 LLM 响应
        
        Args:
            content: LLM 返回的文本
            
        Returns:
            SupervisorResponse: 解析后的结构化数据
        """
        try:
            # 尝试使用 Pydantic Parser
            return self.output_parser.parse(content)
        except Exception:
            # 如果解析失败，尝试手动提取
            return self._fallback_parse(content)
    
    def _fallback_parse(self, content: str) -> SupervisorResponse:
        """
        降级解析策略（当 JSON 解析失败时）
        
        Args:
            content: 原始文本
            
        Returns:
            SupervisorResponse: 默认响应
        """
        # 简单的关键词匹配
        status = "distracted"
        if "专注" in content or "focused" in content.lower():
            status = "focused"
        elif "离开" in content or "away" in content.lower():
            status = "away"
        
        # 提取前30个字作为 message
        message = content[:30].strip()
        
        return SupervisorResponse(
            status=status,
            message=message,
            confidence=0.5
        )


# 单例实例
_agent_instance: Optional[SupervisorAgent] = None


def get_supervisor_agent() -> SupervisorAgent:
    """
    获取 Supervisor Agent 单例
    
    Returns:
        SupervisorAgent: Agent 实例
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = SupervisorAgent()
    return _agent_instance


def analyze_focus(
    image_base64: str, 
    stats: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    便捷函数：分析用户专注状态
    
    Args:
        image_base64: 图片 Base64 字符串
        stats: 统计信息 (checkCount, runningTime, focusTime, currentTime, continuousFocusMinutes, encouragementInterval)
        
    Returns:
        Dict: 包含 status, message, confidence, shouldSpeak 的字典
    """
    # 添加鼓励门槛到 stats
    if stats:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        encouragement_interval = int(stats.get('encouragementInterval',os.getenv('ENCOURAGEMENT_INTERVAL', 20)))
        # encouragement_interval = int(os.getenv('ENCOURAGEMENT_INTERVAL', 20))
        stats['encouragementInterval'] = encouragement_interval
    
    agent = get_supervisor_agent()
    result = agent.analyze(image_base64, stats)
    
    return {
        "status": result.status,
        "message": result.message,
        "confidence": result.confidence,
        "shouldSpeak": result.shouldSpeak
    }
