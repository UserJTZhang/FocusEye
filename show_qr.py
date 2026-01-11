#!/usr/bin/env python3
"""
生成局域网访问二维码
"""
import socket
import sys

def get_local_ip():
    """获取本机局域网IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "无法获取IP"

def main():
    ip = get_local_ip()
    url = f"http://{ip}:3000"
    
    print("=" * 60)
    print("📱 FocusEye 移动端访问")
    print("=" * 60)
    print(f"\n🌐 局域网访问地址: {url}")
    print(f"\n📍 本机IP: {ip}")
    print("\n" + "=" * 60)
    print("📋 使用说明:")
    print("=" * 60)
    print("\n1. 确保手机和电脑在同一WiFi网络")
    print("2. 确保后端服务运行在 5001 端口")
    print("3. 确保前端服务运行在 3000 端口")
    print(f"\n4. 在手机浏览器输入: {url}")
    print("\n5. 授权摄像头权限（需要 HTTPS 或 localhost）")
    print("\n⚠️  注意: 移动浏览器可能需要 HTTPS 才能访问摄像头")
    print("   如果无法访问摄像头，请使用 ngrok 创建 HTTPS 隧道")
    print("\n" + "=" * 60)
    
    # 尝试生成二维码
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        
        print("\n📱 扫描二维码访问:\n")
        qr.print_ascii(invert=True)
        print("\n" + "=" * 60)
    except ImportError:
        print("\n💡 提示: 安装 qrcode 可以显示二维码")
        print("   pip install qrcode")
        print("\n" + "=" * 60)

if __name__ == '__main__':
    main()
