#!/usr/bin/env python3
"""
Network Connectivity Test - Test kết nối giữa máy local và Docker container
"""

import socket
import json
import sys
import time
import subprocess
import platform
from datetime import datetime

class NetworkConnectivityTest:
    def __init__(self, server_ip, server_port=8081):
        self.server_ip = server_ip
        self.server_port = server_port
        self.local_ip = self.get_local_ip()
        
    def get_local_ip(self):
        """Lấy IP local của máy hiện tại"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "localhost"
    
    def ping_test(self):
        """Test ping đến server"""
        print(f"🏓 PING TEST đến {self.server_ip}")
        print("-" * 40)
        
        try:
            # Xác định command ping theo OS
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", "4", self.server_ip]
            else:
                cmd = ["ping", "-c", "4", self.server_ip]
            
            print(f"📤 Executing: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                print("✅ PING SUCCESS")
                print(f"📊 Output:\n{result.stdout}")
                return True
            else:
                print("❌ PING FAILED")
                print(f"❌ Error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ PING TIMEOUT (15s)")
            return False
        except Exception as e:
            print(f"❌ PING ERROR: {e}")
            return False
    
    def port_connectivity_test(self):
        """Test kết nối đến port cụ thể"""
        print(f"\n🔌 PORT CONNECTIVITY TEST đến {self.server_ip}:{self.server_port}")
        print("-" * 40)
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            print(f"🔍 Checking port {self.server_port}...")
            result = sock.connect_ex((self.server_ip, self.server_port))
            
            if result == 0:
                print("✅ PORT IS OPEN and reachable")
                sock.close()
                return True
            else:
                print(f"❌ PORT IS CLOSED or unreachable (error code: {result})")
                return False
                
        except socket.timeout:
            print("❌ CONNECTION TIMEOUT")
            return False
        except Exception as e:
            print(f"❌ CONNECTION ERROR: {e}")
            return False
    
    def docker_container_test(self):
        """Test kết nối cụ thể đến Docker container"""
        print(f"\n🐳 DOCKER CONTAINER TEST")
        print("-" * 40)
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            print(f"🔌 Connecting to Docker container at {self.server_ip}:{self.server_port}...")
            sock.connect((self.server_ip, self.server_port))
            print("✅ Connected to Docker container!")
            
            # Gửi test data
            test_data = {
                "action": "docker_connectivity_test",
                "test_type": "local_to_docker",
                "local_machine": {
                    "ip": self.local_ip,
                    "platform": platform.system(),
                    "hostname": socket.gethostname()
                },
                "target_docker": {
                    "ip": self.server_ip,
                    "port": self.server_port
                },
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "message": f"Test from {self.local_ip} to Docker container {self.server_ip}:{self.server_port}"
            }
            
            json_data = json.dumps(test_data, ensure_ascii=False, indent=2)
            print(f"📤 Sending test data...")
            
            sock.send(json_data.encode('utf-8'))
            
            # Nhận response
            print(f"📥 Waiting for response...")
            response = sock.recv(4096).decode('utf-8')
            
            print(f"✅ Received response from Docker container:")
            print(f"📋 Response: {response}")
            
            try:
                response_json = json.loads(response)
                self.display_docker_response(response_json)
            except json.JSONDecodeError:
                print(f"📝 Raw response: {response}")
            
            sock.close()
            print("🔌 Connection closed")
            return True
            
        except ConnectionRefusedError:
            print("❌ Connection refused - Docker container not running or port not exposed")
            return False
        except socket.timeout:
            print("❌ Connection timeout - Docker container not responding")
            return False
        except Exception as e:
            print(f"❌ Docker connection error: {e}")
            return False
    
    def display_docker_response(self, response_json):
        """Hiển thị response từ Docker container"""
        print(f"\n{'='*50}")
        print(f"📋 DOCKER CONTAINER RESPONSE")
        print(f"{'='*50}")
        
        if "status" in response_json:
            status = response_json["status"]
            print(f"📊 Status: {status}")
        
        if "message" in response_json:
            print(f"💬 Message: {response_json['message']}")
        
        if "server_info" in response_json:
            info = response_json["server_info"]
            print(f"🐳 Container Info:")
            print(f"   📦 Shelf ID: {info.get('shelf_id', 'N/A')}")
            print(f"   👨‍💼 Employee ID: {info.get('employee_id', 'N/A')}")
            print(f"   🌐 Server IP: {info.get('server_ip', 'N/A')}")
            print(f"   🔌 Server Port: {info.get('server_port', 'N/A')}")
        
        if "timestamp" in response_json:
            print(f"🕒 Server Time: {response_json['timestamp']}")
        
        print(f"{'='*50}")
    
    def network_info_test(self):
        """Hiển thị thông tin network"""
        print(f"\n🌐 NETWORK INFORMATION")
        print("-" * 40)
        
        print(f"🖥️  Local Machine:")
        print(f"   IP Address: {self.local_ip}")
        print(f"   Hostname: {socket.gethostname()}")
        print(f"   Platform: {platform.system()} {platform.release()}")
        
        print(f"\n🐳 Docker Server:")
        print(f"   IP Address: {self.server_ip}")
        print(f"   Port: {self.server_port}")
        
        # Test DNS resolution
        try:
            print(f"\n🔍 DNS Resolution test for {self.server_ip}:")
            resolved_ip = socket.gethostbyname(self.server_ip)
            print(f"   ✅ Resolved to: {resolved_ip}")
        except socket.gaierror:
            print(f"   ❌ Cannot resolve hostname: {self.server_ip}")
        
        return True
    
    def comprehensive_test(self):
        """Chạy tất cả các test"""
        print(f"{'='*60}")
        print(f"   🌐 NETWORK CONNECTIVITY TEST")
        print(f"   Local Machine ↔ Docker Container")
        print(f"{'='*60}")
        print(f"🕒 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        tests = [
            ("Network Information", self.network_info_test),
            ("Ping Test", self.ping_test),
            ("Port Connectivity", self.port_connectivity_test),
            ("Docker Container Connection", self.docker_container_test)
        ]
        
        results = []
        
        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            try:
                success = test_func()
                results.append((test_name, success))
                
                if success:
                    print(f"✅ {test_name}: PASSED")
                else:
                    print(f"❌ {test_name}: FAILED")
                
                # Delay giữa các test
                if test_func != self.network_info_test:
                    time.sleep(2)
                    
            except Exception as e:
                print(f"❌ {test_name}: ERROR - {e}")
                results.append((test_name, False))
        
        # Hiển thị kết quả tổng kết
        self.display_final_results(results)
    
    def display_final_results(self, results):
        """Hiển thị kết quả cuối cùng"""
        print(f"\n{'='*60}")
        print(f"📊 FINAL TEST RESULTS")
        print(f"{'='*60}")
        
        passed = 0
        total = len(results)
        
        for test_name, success in results:
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"{status:<12} {test_name}")
            if success:
                passed += 1
        
        print(f"\n📈 Summary: {passed}/{total} tests passed")
        
        if passed == total:
            print(f"🎉 ALL TESTS PASSED!")
            print(f"✅ Network connectivity between local machine and Docker container is working!")
        else:
            failed = total - passed
            print(f"⚠️  {failed} test(s) FAILED")
            print(f"\n💡 Troubleshooting tips:")
            
            if not any(result[1] for result in results if result[0] == "Ping Test"):
                print(f"   🏓 Ping failed - Check network connectivity and firewall")
                
            if not any(result[1] for result in results if result[0] == "Port Connectivity"):
                print(f"   🔌 Port connectivity failed - Check:")
                print(f"      - Docker container is running")
                print(f"      - Port {self.server_port} is exposed in docker-compose.yml")
                print(f"      - Server firewall allows port {self.server_port}")
                
            if not any(result[1] for result in results if result[0] == "Docker Container Connection"):
                print(f"   🐳 Docker connection failed - Check:")
                print(f"      - Docker service is running: docker-compose up -d")
                print(f"      - Container is healthy: docker-compose ps")
                print(f"      - Container logs: docker-compose logs iot-server")
        
        print(f"{'='*60}")

def main():
    """Main function"""
    print("🌐 Network Connectivity Test - Local Machine to Docker Container")
    
    # Lấy thông tin server
    server_ip = input("📝 Nhập IP của Docker Server: ").strip()
    if not server_ip:
        print("❌ IP Server không thể để trống!")
        return
    
    port_input = input("📝 Nhập Port Docker container (Enter = 8081): ").strip()
    if port_input and port_input.isdigit():
        port = int(port_input)
    else:
        port = 8081
    
    print(f"\n🎯 Sẽ test kết nối từ máy local đến Docker container:")
    print(f"   Target: {server_ip}:{port}")
    
    # Xác nhận
    confirm = input(f"\n❓ Tiếp tục với test? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("👋 Test bị hủy!")
        return
    
    # Tạo test instance
    test = NetworkConnectivityTest(server_ip, port)
    
    try:
        test.comprehensive_test()
    except KeyboardInterrupt:
        print("\n⏹️  Test bị dừng bởi user")
    except Exception as e:
        print(f"❌ Lỗi trong quá trình test: {e}")
    finally:
        print("\n👋 Test hoàn thành!")

if __name__ == "__main__":
    main()
