"""
Vercel Serverless Function 入口
处理 HTTP 请求并路由到对应的服务
"""
import json
import sys
from pathlib import Path
from typing import Dict, Any

# 添加项目根目录到 Python Path（Vercel 环境需要）
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.service import analyze_status, check_health


def create_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """
    创建标准的 HTTP 响应
    
    Args:
        status_code: HTTP 状态码
        body: 响应体
        
    Returns:
        Dict: Vercel 格式的响应
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # CORS
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(body, ensure_ascii=False)
    }


def handle_analyze(body: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理分析请求
    
    Args:
        body: 请求体，应包含 image 字段
        
    Returns:
        Dict: 分析结果
    """
    # 获取图片数据
    image_base64 = body.get("image")
    if not image_base64:
        return create_response(400, {
            "success": False,
            "error": "缺少 image 字段"
        })
    
    # 获取可选的上下文
    context = body.get("context")
    
    # 调用服务层
    result = analyze_status(image_base64, context)
    
    # 根据结果返回状态码
    status_code = 200 if result.get("success") else 500
    
    return create_response(status_code, result)


def handle_health() -> Dict[str, Any]:
    """
    处理健康检查请求
    
    Returns:
        Dict: 健康状态
    """
    result = check_health()
    status_code = 200 if result.get("success") else 500
    
    return create_response(status_code, result)


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Vercel Serverless Function 主入口
    
    Args:
        event: 请求事件对象
        context: Lambda 上下文（可选）
        
    Returns:
        Dict: HTTP 响应
    """
    try:
        # 处理 OPTIONS 请求（CORS 预检）
        method = event.get("httpMethod") or event.get("method", "GET")
        if method == "OPTIONS":
            return create_response(200, {})
        
        # 解析请求体
        body_str = event.get("body", "{}")
        if isinstance(body_str, str):
            body = json.loads(body_str) if body_str else {}
        else:
            body = body_str
        
        # 路由
        path = event.get("path", "/")
        
        if path == "/api/health" or method == "GET":
            return handle_health()
        elif path == "/api/analyze" or path == "/" or method == "POST":
            return handle_analyze(body)
        else:
            return create_response(404, {
                "success": False,
                "error": f"未知路径: {path}"
            })
            
    except json.JSONDecodeError:
        return create_response(400, {
            "success": False,
            "error": "无效的 JSON 格式"
        })
    except Exception as e:
        return create_response(500, {
            "success": False,
            "error": f"服务器错误: {str(e)}"
        })


# Vercel 默认导出
def default(event, context=None):
    """Vercel 默认处理函数"""
    return handler(event, context)
