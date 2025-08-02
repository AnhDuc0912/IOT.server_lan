#!/usr/bin/env python3
"""
Test Client cho IoT Server LAN
- Test kết nối cơ bản
- Test gửi JSON data
- Test QR code data format
- Test device info
"""

import socket
import json
import time
import sys
from datetime import datetime

class IoTTestClient:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.socket = None
        
    def connect(self):
        """Kết nối đến server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # 10 seconds timeout
            
            print(f"🔌 Đang kết nối đến {self.host}:{self.port}...")
            self.socket.connect((self.host, self.port))
            print(f"✅ Kết nối thành công!")
            return True
            
        except socket.timeout:
            print(f"❌ Timeout khi kết nối đến {self.host}:{self.port}")
            return False
        except ConnectionRefusedError:
            print(f"❌ Không thể kết nối - Server có đang chạy không?")
            return False
        except Exception as e:
            print(f"❌ Lỗi kết nối: {e}")
            return False
    
    def send_data(self, data):
        """Gửi dữ liệu đến server"""
        try:
            if isinstance(data, dict):
                json_data = json.dumps(data, ensure_ascii=False)
            else:
                json_data = str(data)
                
            print(f"📤 Gửi dữ liệu: {json_data}")
            self.socket.send(json_data.encode('utf-8'))
            
            # Nhận response
            response = self.socket.recv(4096).decode('utf-8')
            print(f"📥 Nhận response: {response}")
            
            try:
                response_json = json.loads(response)
                self.display_response(response_json)
            except json.JSONDecodeError:
                print(f"📝 Text response: {response}")
                
            return True
            
        except Exception as e:
            print(f"❌ Lỗi gửi dữ liệu: {e}")
            return False
    
    def display_response(self, response_json):
        """Hiển thị response từ server"""
        print(f"\n{'='*50}")
        print(f"📋 RESPONSE TỪ SERVER")
        print(f"{'='*50}")
        
        if "status" in response_json:
            status = response_json["status"]
            status_icon = "✅" if status == "success" else "❌"
            print(f"{status_icon} Status: {status}")
            
        if "message" in response_json:
            print(f"💬 Message: {response_json['message']}")
            
        if "timestamp" in response_json:
            print(f"🕒 Timestamp: {response_json['timestamp']}")
            
        if "server_info" in response_json:
            info = response_json["server_info"]
            print(f"📦 Shelf ID: {info.get('shelf_id', 'N/A')}")
            print(f"👨‍💼 Employee ID: {info.get('employee_id', 'N/A')}")
            print(f"🌐 Server IP: {info.get('server_ip', 'N/A')}")
            print(f"🔌 Server Port: {info.get('server_port', 'N/A')}")
            
        print(f"{'='*50}")
    
    def disconnect(self):
        """Đóng kết nối"""
        if self.socket:
            try:
                self.socket.close()
                print(f"🔌 Đã đóng kết nối")
            except:
                pass
    
    def test_basic_connection(self):
        """Test kết nối cơ bản"""
        print(f"\n🧪 TEST 1: Kết nối cơ bản")
        print("-" * 40)
        
        if not self.connect():
            return False
            
        # Gửi tin nhắn đơn giản
        success = self.send_data("Hello from test client!")
        self.disconnect()
        return success
    
    def test_json_data(self):
        """Test gửi JSON data"""
        print(f"\n🧪 TEST 2: Gửi JSON data")
        print("-" * 40)
        
        if not self.connect():
            return False
            
        test_data = {
            "action": "test_connection",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "test_type": "json_data",
            "message": "Test JSON message from client"
        }
        
        success = self.send_data(test_data)
        self.disconnect()
        return success
    
    def test_qr_data_format(self):
        """Test format dữ liệu QR"""
        print(f"\n🧪 TEST 3: QR Data Format")
        print("-" * 40)
        
        if not self.connect():
            return False
            
        qr_data = {
            "action": "connect_to_shelf",
            "qr_data": {
                "ip": self.host,
                "port": self.port,
                "shelf_id": "SHELF001",
                "employee_id": "EMP123"
            },
            "device_info": {
                "model": "Test Device",
                "android_version": "11.0",
                "app_name": "IoT Test Client",
                "app_version": "1.0.0"
            },
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        success = self.send_data(qr_data)
        self.disconnect()
        return success
    
    def test_android_app_simulation(self):
        """Mô phỏng Android app kết nối"""
        print(f"\n🧪 TEST 4: Mô phỏng Android App")
        print("-" * 40)
        
        if not self.connect():
            return False
            
        android_data = {
            "action": "android_connection",
            "qr_data": {
                "ip": self.host,
                "port": self.port,
                "shelf_id": "SHELF001",
                "employee_id": "EMP123",
                "action": "connect_to_shelf"
            },
            "device_info": {
                "model": "Samsung Galaxy S21",
                "android_version": "12.0",
                "app_name": "IoT Shelf Manager",
                "app_version": "2.1.0",
                "device_id": "test_device_001"
            },
            "user_info": {
                "employee_id": "EMP123",
                "employee_name": "Nguyen Van A",
                "department": "Warehouse"
            },
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        success = self.send_data(android_data)
        self.disconnect()
        return success
    
    def run_all_tests(self):
        """Chạy tất cả các test"""
        print(f"{'='*60}")
        print(f"        🧪 IOT SERVER CONNECTION TESTS")
        print(f"{'='*60}")
        print(f"🎯 Target: {self.host}:{self.port}")
        print(f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        tests = [
            ("Basic Connection", self.test_basic_connection),
            ("JSON Data", self.test_json_data),
            ("QR Data Format", self.test_qr_data_format),
            ("Android App Simulation", self.test_android_app_simulation)
        ]
        
        results = []
        
        for test_name, test_func in tests:
            try:
                print(f"\n🚀 Đang chạy: {test_name}")
                success = test_func()
                results.append((test_name, success))
                
                if success:
                    print(f"✅ {test_name}: PASSED")
                else:
                    print(f"❌ {test_name}: FAILED")
                    
                time.sleep(1)  # Delay giữa các test
                
            except Exception as e:
                print(f"❌ {test_name}: ERROR - {e}")
                results.append((test_name, False))
        
        # Hiển thị kết quả tổng kết
        self.display_test_summary(results)
    
    def display_test_summary(self, results):
        """Hiển thị tổng kết test"""
        print(f"\n{'='*60}")
        print(f"📊 KẾT QUẢ TEST TỔNG KẾT")
        print(f"{'='*60}")
        
        passed = 0
        total = len(results)
        
        for test_name, success in results:
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"{status:<12} {test_name}")
            if success:
                passed += 1
        
        print(f"\n📈 Tổng kết: {passed}/{total} tests passed")
        
        if passed == total:
            print(f"🎉 Tất cả tests đều PASSED! Server hoạt động tốt.")
        else:
            print(f"⚠️  Có {total - passed} tests FAILED. Kiểm tra server.")
        
        print(f"{'='*60}")

def main():
    """Main function"""
    print("🧪 IoT Server Connection Test Client")
    
    # Lấy thông tin server
    host = input("📝 Nhập IP Server (Enter = localhost): ").strip()
    if not host:
        host = "localhost"
    
    port_input = input("📝 Nhập Port (Enter = 8080): ").strip()
    if port_input and port_input.isdigit():
        port = int(port_input)
    else:
        port = 8080
    
    # Tạo test client
    test_client = IoTTestClient(host, port)
    
    print(f"\n🎯 Sẽ test server tại: {host}:{port}")
    print("💡 Đảm bảo server đang chạy trước khi test!")
    
    # Hỏi user muốn chạy test nào
    print(f"\n📋 Chọn loại test:")
    print("1. Chạy tất cả tests")
    print("2. Test kết nối cơ bản")
    print("3. Test JSON data")
    print("4. Test QR data format")
    print("5. Test Android app simulation")
    
    choice = input("📝 Nhập lựa chọn (1-5): ").strip()
    
    try:
        if choice == "1":
            test_client.run_all_tests()
        elif choice == "2":
            test_client.test_basic_connection()
        elif choice == "3":
            test_client.test_json_data()
        elif choice == "4":
            test_client.test_qr_data_format()
        elif choice == "5":
            test_client.test_android_app_simulation()
        else:
            print("❌ Lựa chọn không hợp lệ")
            
    except KeyboardInterrupt:
        print("\n⏹️  Test bị dừng bởi user")
    except Exception as e:
        print(f"❌ Lỗi trong quá trình test: {e}")
    finally:
        test_client.disconnect()
        print("👋 Test hoàn thành!")

if __name__ == "__main__":
    main()
