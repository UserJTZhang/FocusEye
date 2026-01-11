#!/usr/bin/env python
"""
测试阿里云 CosyVoice 语音合成 API
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_tts_simple():
    """最简单的测试"""
    import dashscope
    from dashscope.audio.tts_v2 import SpeechSynthesizer
    
    # 设置 API Key
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("❌ 未找到 API_KEY 环境变量")
        return
    
    dashscope.api_key = api_key
    print(f"✅ API Key: {api_key[:20]}...")
    
    # 测试文本
    text = "我的好朋友！恭喜你迈出了重要的一步！现在我来陪你一起专注吧！"
    
    try:
        print(f"\n🎤 开始合成: {text}")
        print(f"🎵 模型: cosyvoice-v3-flash")
        print(f"🎵 音色: longanyang")
        
        # 创建合成器（使用最简单的参数）
        synthesizer = SpeechSynthesizer(
            model="cosyvoice-v3-flash",
            voice="longanyang"
        )
        
        # 调用合成
        print("\n⏳ 正在调用 API...")
        audio_data = synthesizer.call(text)
        
        # 检查结果
        if audio_data:
            print(f"\n✅ 合成成功！")
            print(f"📊 音频大小: {len(audio_data)} 字节")
            print(f"📊 数据类型: {type(audio_data)}")
            
            # 保存到文件
            output_file = "test_output.wav"
            with open(output_file, "wb") as f:
                f.write(audio_data)
            print(f"💾 已保存到: {output_file}")
            
            return True
        else:
            print("❌ 合成失败：未返回数据")
            return False
            
    except Exception as e:
        print(f"\n❌ 异常: {type(e).__name__}")
        print(f"   错误信息: {str(e)}")
        
        # 打印详细的错误堆栈
        import traceback
        print("\n详细错误:")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("阿里云 CosyVoice 语音合成测试")
    print("=" * 60)
    
    # 读取 voice_config.json
    voice_config_path = Path(__file__).parent / "frontend/public/voice_config.json"
    with open(voice_config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    voices = config.get('voices', [])
    model = config.get('model', 'cosyvoice-v3-flash')
    
    # 创建输出目录
    output_dir = Path(__file__).parent / "frontend/public/voice"
    output_dir.mkdir(exist_ok=True)
    
    # 试听文本
    sample_text = "我的好朋友，我是Focus Eye，每天进步一点点！现在我来陪你一起专注吧！"
    
    print(f"\n📋 共有 {len(voices)} 个音色需要生成")
    print(f"📝 试听文本: {sample_text}")
    print(f"🎵 模型: {model}")
    print(f"📁 输出目录: {output_dir}\n")
    
    # 循环生成
    import dashscope
    from dashscope.audio.tts_v2 import SpeechSynthesizer
    
    api_key = os.getenv("API_KEY")
    dashscope.api_key = api_key
    
    success_count = 0
    fail_count = 0
    
    for idx, voice_info in enumerate(voices, 1):
        name = voice_info['name']
        voice_param = voice_info['voice_parameter']
        characteristics = voice_info['characteristics']
        
        print(f"[{idx}/{len(voices)}] 🎤 {name} ({characteristics}) - {voice_param}")
        
        try:
            synthesizer = SpeechSynthesizer(
                model=model,
                voice=voice_param
            )
            
            audio_data = synthesizer.call(sample_text)
            
            if audio_data:
                output_file = output_dir / f"{voice_param}.mp3"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                
                file_size = len(audio_data) / 1024
                print(f"   ✅ 成功: {output_file.name} ({file_size:.1f} KB)\n")
                success_count += 1
            else:
                print(f"   ❌ 失败: 未返回数据\n")
                fail_count += 1
                
        except Exception as e:
            print(f"   ❌ 失败: {str(e)}\n")
            fail_count += 1
    
    print("=" * 60)
    print(f"✅ 成功: {success_count} 个")
    print(f"❌ 失败: {fail_count} 个")
    print("=" * 60)
