"""
图片处理工具
Base64 图片的校验、清洗和预处理
"""
import re
import base64
from typing import Tuple, Optional


def validate_base64_image(base64_string: str) -> Tuple[bool, str]:
    """
    校验 Base64 图片格式
    
    Args:
        base64_string: Base64 编码的图片字符串
        
    Returns:
        Tuple[bool, str]: (是否有效, 错误信息)
    """
    if not base64_string:
        return False, "图片数据为空"
    
    # 检查是否包含 Data URI 头部
    if not base64_string.startswith("data:image/"):
        return False, "缺少 data:image/ 前缀"
    
    # 检查是否包含 base64 标记
    if ";base64," not in base64_string:
        return False, "缺少 ;base64, 标记"
    
    try:
        # 提取纯 Base64 部分并尝试解码
        _, encoded = base64_string.split(";base64,", 1)
        base64.b64decode(encoded, validate=True)
        return True, ""
    except Exception as e:
        return False, f"Base64 解码失败: {str(e)}"


def extract_image_format(base64_string: str) -> Optional[str]:
    """
    从 Data URI 中提取图片格式
    
    Args:
        base64_string: Base64 编码的图片字符串
        
    Returns:
        Optional[str]: 图片格式 (如 'jpeg', 'png') 或 None
    """
    pattern = r"data:image/(\w+);base64,"
    match = re.match(pattern, base64_string)
    
    if match:
        return match.group(1)
    return None


def normalize_base64_image(base64_string: str) -> str:
    """
    规范化 Base64 图片字符串
    确保格式符合 OpenAI API 要求
    
    Args:
        base64_string: 原始 Base64 字符串
        
    Returns:
        str: 规范化后的字符串
    """
    # 如果已经包含 Data URI，直接返回
    if base64_string.startswith("data:image/"):
        return base64_string
    
    # 否则假设是 JPEG 格式，添加前缀
    return f"data:image/jpeg;base64,{base64_string}"


def get_image_size_estimate(base64_string: str) -> int:
    """
    估算图片大小（字节）
    
    Args:
        base64_string: Base64 编码的图片
        
    Returns:
        int: 估算的字节数
    """
    try:
        if ";base64," in base64_string:
            _, encoded = base64_string.split(";base64,", 1)
        else:
            encoded = base64_string
        
        # Base64 编码后大约是原始大小的 4/3
        return len(encoded) * 3 // 4
    except Exception:
        return 0


def validate_image_size(base64_string: str, max_size_mb: float = 5.0) -> Tuple[bool, str]:
    """
    验证图片大小是否在允许范围内
    
    Args:
        base64_string: Base64 编码的图片
        max_size_mb: 最大允许大小（MB）
        
    Returns:
        Tuple[bool, str]: (是否有效, 错误信息)
    """
    size_bytes = get_image_size_estimate(base64_string)
    max_bytes = int(max_size_mb * 1024 * 1024)
    
    if size_bytes > max_bytes:
        return False, f"图片过大: {size_bytes/1024/1024:.2f}MB, 最大允许 {max_size_mb}MB"
    
    return True, ""


def clean_base64_string(base64_string: str) -> str:
    """
    清理 Base64 字符串中的空白字符
    
    Args:
        base64_string: 原始字符串
        
    Returns:
        str: 清理后的字符串
    """
    # 移除所有空白字符（但保留 Data URI 头部）
    if ";base64," in base64_string:
        prefix, data = base64_string.split(";base64,", 1)
        data = re.sub(r'\s+', '', data)
        return f"{prefix};base64,{data}"
    
    return re.sub(r'\s+', '', base64_string)
