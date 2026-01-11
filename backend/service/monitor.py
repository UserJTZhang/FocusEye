"""
监督服务层
业务逻辑的组装者：校验 -> 调用 Agent -> 格式化结果
"""
from typing import Dict, Any, Optional
import logging
from backend.utils import validate_base64_image, clean_base64_string, validate_image_size
from backend.Agent import analyze_focus

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MonitorService:
    """监督服务类"""
    
    @staticmethod
    def analyze_user_status(
        image_base64: str,
        stats: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        分析用户学习状态
        
        Args:
            image_base64: Base64 编码的图片
            stats: 监督统计信息 (checkCount, runningTime, focusTime, currentTime, continuousFocusMinutes)
            
        Returns:
            Dict: 包含以下字段的字典
                - success: bool, 是否成功
                - status: str, 状态 (focused/distracted/away/error)
                - message: str, 反馈文本
                - confidence: float, 置信度
                - shouldSpeak: bool, 是否需要语音播放
                - error: str, 错误信息（如果失败）
        """
        try:
            # 1. 清理输入
            image_base64 = clean_base64_string(image_base64)
            
            # 2. 验证图片格式
            is_valid, error_msg = validate_base64_image(image_base64)
            if not is_valid:
                logger.warning(f"图片格式验证失败: {error_msg}")
                return {
                    "success": False,
                    "status": "error",
                    "message": "图片格式不正确",
                    "confidence": 0.0,
                    "error": error_msg
                }
            
            # 3. 验证图片大小
            size_valid, size_error = validate_image_size(image_base64, max_size_mb=5.0)
            if not size_valid:
                logger.warning(f"图片大小验证失败: {size_error}")
                return {
                    "success": False,
                    "status": "error",
                    "message": "图片太大，请压缩后重试",
                    "confidence": 0.0,
                    "error": size_error
                }
            
            # 4. 调用 Agent 分析
            logger.info("开始分析用户状态...")
            result = analyze_focus(image_base64, stats)
            
            # 5. 格式化返回结果
            response = {
                "success": True,
                "status": result.get("status", "unknown"),
                "message": result.get("message", "分析完成"),
                "confidence": result.get("confidence", 0.8),
                "shouldSpeak": result.get("shouldSpeak", True)  # 是否需要语音播放
            }
            
            logger.info(f"分析完成: {response['status']} - {response['message']} - 语音: {response['shouldSpeak']}")
            return response
            
        except Exception as e:
            # 捕获所有异常，返回友好的错误信息
            logger.error(f"分析过程出错: {str(e)}", exc_info=True)
            return {
                "success": False,
                "status": "error",
                "message": "分析失败，请稍后重试",
                "confidence": 0.0,
                "error": str(e)
            }
    
    @staticmethod
    def health_check() -> Dict[str, Any]:
        """
        健康检查接口
        
        Returns:
            Dict: 服务状态信息
        """
        try:
            from backend.config import settings
            import os
            
            # 验证配置
            settings.validate()
            
            # 获取监督配置
            monitor_interval = int(os.getenv('MONITOR_INTERVAL', 60))
            monitor_interval_random = int(os.getenv('MONITOR_INTERVAL_RANDOM', 10))
            encouragement_interval = int(os.getenv('ENCOURAGEMENT_INTERVAL', 20))
            rest_reminder_interval = int(os.getenv('REST_REMINDER_INTERVAL', 3))
            
            return {
                "success": True,
                "status": "healthy",
                "message": "服务运行正常",
                "config": {
                    "model": settings.MODEL_NAME,
                    "api_base": settings.API_BASE[:30] + "...",  # 只显示部分 URL
                    "monitorInterval": monitor_interval,  # 监督间隔（秒）
                    "monitorIntervalRandom": monitor_interval_random,  # 随机波动（秒）
                    "encouragementInterval": encouragement_interval,  # 鼓励间隔（分钟）
                    "restReminderInterval": rest_reminder_interval  # 休息提醒间隔（分钟）
                }
            }
        except Exception as e:
            return {
                "success": False,
                "status": "unhealthy",
                "message": "配置错误",
                "error": str(e)
            }


# 创建全局服务实例
monitor_service = MonitorService()


# 便捷函数
def analyze_status(image_base64: str, stats: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    便捷函数：分析用户状态
    
    Args:
        image_base64: Base64 图片
        stats: 统计信息
        
    Returns:
        Dict: 分析结果
    """
    return monitor_service.analyze_user_status(image_base64, stats)


def check_health() -> Dict[str, Any]:
    """
    便捷函数：健康检查
    
    Returns:
        Dict: 健康状态
    """
    return monitor_service.health_check()
