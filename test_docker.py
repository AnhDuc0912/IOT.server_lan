#!/usr/bin/env python3
"""
Docker Connectivity Test - Test nhanh kết nối đến Docker container
"""

import socket
import json
import sys
import time

def test_docker_connection(server_ip, port=8081):
    """Test kết nối đến Docker container"""
    print(f"🐳 Docker Container Test")
    print(f"Target: {server_ip}:{port}")
    print("-" * 40)
    
    try:
        # Test 1: Port connectivity
        print("🔍 Step 1: Checking port connectivity...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        result = sock.connect_ex((server_ip, port))
        if result != 0:
            print(f"❌ Port {port} is not reachable on {server_ip}")
            return False
        
        print("✅ Port is reachable")
        sock.close()
        
        # Test 2: Full connection with data
        print("🔌 Step 2: Testing full connection...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        
        sock.connect((server_ip, port))
        print("✅ Connected to Docker container")
        
        # Test data
        test_data = {
            "action": "docker_test",
            "message": "Test from external machine to Docker container",
            "qr_data": {
                "ip": server_ip,
                "port": port,
                "shelf_id": "SHELF001",
                "employee_id": "EMP123"
            }
        }
        
        json_data = json.dumps(test_data, ensure_ascii=False)
        print(f"📤 Sending test data...")
        
        sock.send(json_data.encode('utf-8'))
        
        # Receive response
        print("📥 Waiting for response...")
        response = sock.recv(4096).decode('utf-8')
        
        print("✅ Received response:")
        print(f"📋 {response}")
        
        sock.close()
        print("🔌 Connection closed successfully")
        
        return True
        
    except ConnectionRefusedError:
        print("❌ Connection refused")
        print("💡 Possible issues:")
        print("   - Docker container is not running")
        print("   - Port is not exposed in docker-compose.yml")
        return False
        
    except socket.timeout:
        print("❌ Connection timeout")
        print("💡 Possible issues:")
        print("   - Server is not responding")
        print("   - Network connectivity issues")
        print("   - Firewall blocking the connection")
        return False
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("❌ Usage: python test_docker.py <server_ip> [port]")
        print("   Example: python test_docker.py 192.168.1.100")
        print("   Example: python test_docker.py 192.168.1.100 8081")
        return
    
    server_ip = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8081
    
    print("=" * 50)
    print("   🐳 DOCKER CONNECTIVITY TEST")
    print("=" * 50)
    
    success = test_docker_connection(server_ip, port)
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Docker connection test PASSED!")
        print("✅ Your machine can connect to the Docker container")
    else:
        print("❌ Docker connection test FAILED!")
        print("\n💡 Troubleshooting checklist:")
        print("   1. Is Docker container running?")
        print("      docker-compose ps")
        print("   2. Check container logs:")
        print("      docker-compose logs iot-server")
        print("   3. Verify port mapping in docker-compose.yml:")
        print(f"      ports: - \"{port}:8080\"")
        print("   4. Check server firewall")
        print("   5. Test with telnet:")
        print(f"      telnet {server_ip} {port}")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
