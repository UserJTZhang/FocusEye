"""
文本转语音服务
使用阿里云 CosyVoice API
"""
import os
import requests
import time
import hashlib
import hmac
import base64
from typing import Optional, Dict


def generate_temp_token() -> Optional[Dict]:
    """
    生成临时鉴权 Token（60秒有效）
    用于前端直接连接 WebSocket
    
    注意：阿里云目前没有提供临时 Token API，
    这里直接返回 API Key，生产环境应该使用其他安全方案
    
    Returns:
        包含 token 和过期时间的字典
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("未配置 API_KEY")
    
    # 直接返回 API Key
    # 生产环境建议：
    # 1. 使用子账号 RAM 角色临时凭证
    # 2. 设置 IP 白名单
    # 3. 限制单日调用次数
    print("🔑 返回 API Key（生产环境请使用更安全的方案）")
    return {
        "token": api_key,
        "expires_at": int(time.time()) + 3600  # 1小时后过期（仅用于前端判断）
    }


def synthesize_speech(
    text: str,
    model: str = None,
    voice: str = None
) -> Optional[bytes]:
    """
    调用阿里云 CosyVoice API 进行语音合成
    使用 DashScope Python SDK
    
    Args:
        text: 要合成的文本
        model: 模型名称（默认从环境变量读取）
        voice: 音色名称（默认从环境变量读取）
        
    Returns:
        音频二进制数据，失败返回 None
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("未配置 API_KEY")
    
    # 从环境变量读取配置
    if model is None:
        model = os.getenv("TTS_MODEL", "cosyvoice-v3-flash")
    if voice is None:
        voice = os.getenv("TTS_VOICE", "longanyang")
    
    try:
        # 使用 DashScope SDK
        from http import HTTPStatus
        import dashscope
        from dashscope.audio.tts_v2 import SpeechSynthesizer
        
        # 设置 API Key
        dashscope.api_key = api_key
        
        print(f"🎤 调用 CosyVoice API: {text[:50]}...")
        print(f"🎵 模型: {model}, 音色: {voice}")
        
        # 创建合成器（使用默认格式，不指定 format 参数）
        synthesizer = SpeechSynthesizer(
            model=model,
            voice=voice
        )
        
        # 调用合成（直接返回 bytes）
        audio_data = synthesizer.call(text)
        
        if audio_data and isinstance(audio_data, bytes):
            print(f"✅ 语音合成成功，大小: {len(audio_data)} 字节")
            return audio_data
        else:
            print("❌ 语音合成失败：未返回数据或类型错误")
            return None
            
    except ImportError:
        print("❌ 未安装 dashscope，尝试使用 HTTP API...")
        return synthesize_speech_http(text, model, voice, api_key)
    except Exception as e:
        print(f"❌ 语音合成异常: {str(e)}")
        # 降级到 HTTP 方式
        return synthesize_speech_http(text, model, voice, api_key)


def synthesize_speech_http(
    text: str,
    model: str,
    voice: str,
    api_key: str
) -> Optional[bytes]:
    """
    HTTP 方式调用（降级方案）
    """
    url = os.getenv("TTS_API_URL", "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/synthesis")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "input": {
            "text": text
        },
        "parameters": {
            "voice": voice,
            "format": "mp3",
            "sample_rate": 22050,
            "volume": 50,
            "speech_rate": 1.0,
            "pitch_rate": 1.0
        }
    }
    
    try:
        print(f"🎤 HTTP 降级：调用 {url}")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            # 成功返回音频数据
            audio_data = response.content
            print(f"✅ HTTP 方式合成成功，大小: {len(audio_data)} 字节")
            return audio_data
        else:
            print(f"❌ HTTP API 错误: {response.status_code}")
            print(f"响应: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ HTTP 请求异常: {str(e)}")
        return None
    
    try:
        print(f"🎤 调用 CosyVoice API: {text[:50]}...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            
            if 'audio' in content_type or 'octet-stream' in content_type:
                print(f"✅ 语音合成成功，大小: {len(response.content)} 字节")
                return response.content
            else:
                try:
                    result = response.json()
                    if 'output' in result and 'audio_url' in result['output']:
                        audio_url = result['output']['audio_url']
                        audio_response = requests.get(audio_url, timeout=10)
                        if audio_response.status_code == 200:
                            print(f"✅ 语音合成成功（从URL），大小: {len(audio_response.content)} 字节")
                            return audio_response.content
                    
                    print(f"❌ API 返回格式不正确: {result}")
                    return None
                except Exception as e:
                    print(f"❌ 解析响应失败: {e}")
                    return None
        else:
            print(f"❌ API 调用失败: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"错误详情: {error_detail}")
            except:
                print(f"响应内容: {response.text[:200]}")
            return None
            
    except requests.Timeout:
        print("❌ API 调用超时")
        return None
    except Exception as e:
        print(f"❌ 语音合成异常: {str(e)}")
        return None
