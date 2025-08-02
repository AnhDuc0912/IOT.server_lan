#!/usr/bin/env python3
"""
Quick Test - Test nhanh kết nối IoT Server
"""

import socket
import json
import sys

def quick_test(host='localhost', port=8080):
    """Test nhanh kết nối server"""
    print(f"🧪 Quick Test - Kết nối đến {host}:{port}")
    
    try:
        # Tạo socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        # Kết nối
        print("🔌 Đang kết nối...")
        sock.connect((host, port))
        print("✅ Kết nối thành công!")
        
        # Gửi dữ liệu test
        test_data = {
            "action": "quick_test",
            "message": "Hello from quick test!",
            "qr_data": {
                "ip": host,
                "port": port,
                "shelf_id": "SHELF001",
                "employee_id": "EMP123"
            }
        }
        
        json_data = json.dumps(test_data, ensure_ascii=False)
        print(f"📤 Gửi: {json_data}")
        
        sock.send(json_data.encode('utf-8'))
        
        # Nhận response
        response = sock.recv(4096).decode('utf-8')
        print(f"📥 Nhận: {response}")
        
        # Đóng kết nối
        sock.close()
        print("🔌 Đã đóng kết nối")
        print("✅ Test thành công!")
        
        return True
        
    except ConnectionRefusedError:
        print("❌ Không thể kết nối - Server có đang chạy không?")
        return False
    except socket.timeout:
        print("❌ Timeout - Server không phản hồi")
        return False
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

if __name__ == "__main__":
    # Parse arguments
    host = "localhost"
    port = 8080
    
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    
    print("="*50)
    print("   🚀 QUICK TEST - IoT Server Connection")
    print("="*50)
    
    success = quick_test(host, port)
    
    if success:
        print("\n🎉 Server hoạt động tốt!")
    else:
        print("\n⚠️  Server có vấn đề hoặc không chạy")
        print("💡 Hướng dẫn:")
        print("   1. Đảm bảo server đang chạy")
        print("   2. Kiểm tra IP và Port")
        print("   3. Kiểm tra firewall")
    
    print("\n📋 Cách sử dụng:")
    print("   python test_quick.py")
    print("   python test_quick.py <ip>")
    print("   python test_quick.py <ip> <port>")
