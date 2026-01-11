"""
本地开发服务器
用于在本地同时启动前后端进行测试
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.service import analyze_status, check_health
from backend.service.tts import synthesize_speech, generate_temp_token

# 创建 Flask 应用
app = Flask(__name__)
CORS(app)  # 允许跨域


@app.route('/api/health', methods=['GET'])
def health():
    """健康检查接口"""
    result = check_health()
    status_code = 200 if result.get("success") else 500
    return jsonify(result), status_code


@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    """图片分析接口"""
    # 处理 OPTIONS 预检请求
    if request.method == 'OPTIONS':
        print("📨 收到 OPTIONS 预检请求")
        return '', 200
    
    print("\n" + "="*50)
    print("📨 收到 POST 请求: /api/analyze")
    print("="*50)
    
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            print("❌ 错误: 缺少 image 字段")
            return jsonify({
                "success": False,
                "error": "缺少 image 字段"
            }), 400
        
        image_base64 = data.get('image')
        stats = data.get('stats')  # 获取统计信息
        
        print(f"📷 图片大小: {len(image_base64)} 字符")
        if stats:
            print(f"📊 统计信息: {stats}")
        
        # 调用服务层
        print("🤖 开始 AI 分析...")
        result = analyze_status(image_base64, stats)
        
        print(f"✅ 分析完成: {result}")
        print("="*50 + "\n")
        
        status_code = 200 if result.get("success") else 500
        return jsonify(result), status_code
        
    except Exception as e:
        print(f"❌ 服务器错误: {str(e)}")
        print("="*50 + "\n")
        return jsonify({
            "success": False,
            "error": f"服务器错误: {str(e)}"
        }), 500


@app.route('/api/tts/token', methods=['GET', 'OPTIONS'])
def get_tts_token():
    """获取临时 Token 用于前端直接连接 WebSocket"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        print("🔑 生成临时 TTS Token...")
        token_data = generate_temp_token()
        
        if token_data:
            return jsonify({
                "success": True,
                "token": token_data["token"],
                "expires_at": token_data["expires_at"]
            })
        else:
            return jsonify({
                "success": False,
                "error": "生成 Token 失败"
            }), 500
            
    except Exception as e:
        print(f"❌ 生成 Token 错误: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/tts', methods=['POST', 'OPTIONS'])
def tts():
    """文本转语音接口"""
    # 处理 OPTIONS 预检请求
    if request.method == 'OPTIONS':
        print("📨 收到 TTS OPTIONS 预检请求")
        return '', 200
    
    print("\n" + "="*50)
    print("📨 收到 TTS 请求")
    print("="*50)
    
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            print("❌ 错误: 缺少 text 字段")
            return jsonify({
                "success": False,
                "error": "缺少 text 字段"
            }), 400
        
        text = data.get('text')
        model = data.get('model', 'cosyvoice-v3-flash')
        voice = data.get('voice', 'longanyang')
        
        print(f"📝 文本: {text}")
        print(f"🎵 模型: {model}, 音色: {voice}")
        
        # 调用 TTS 服务
        print("🎤 开始语音合成...")
        audio_data = synthesize_speech(text, model, voice)
        
        if audio_data:
            print(f"✅ 语音合成成功，大小: {len(audio_data)} 字节")
            print("="*50 + "\n")
            # 返回音频数据
            from flask import make_response
            response = make_response(audio_data)
            response.headers['Content-Type'] = 'audio/mpeg'
            response.headers['Content-Length'] = len(audio_data)
            return response
        else:
            print("❌ 语音合成失败")
            print("="*50 + "\n")
            return jsonify({
                "success": False,
                "error": "语音合成失败"
            }), 500
            
    except Exception as e:
        print(f"❌ TTS 服务器错误: {str(e)}")
        print("="*50 + "\n")
        return jsonify({
            "success": False,
            "error": f"服务器错误: {str(e)}"
        }), 500


@app.route('/')
def index():
    """根路径"""
    return jsonify({
        "message": "FocusEye API Server",
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "analyze": "/api/analyze"
        }
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 FocusEye 本地开发服务器")
    print("=" * 60)
    print("📡 后端 API: http://localhost:5001")
    print("📊 健康检查: http://localhost:5001/api/health")
    print("🔍 图片分析: http://localhost:5001/api/analyze")
    print("=" * 60)
    print("💡 提示: 请在另一个终端启动前端")
    print("   cd frontend && npm run dev")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=5001, debug=True)
