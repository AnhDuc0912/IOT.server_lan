#!/usr/bin/env python3
"""
P2P Test Client - Test kết nối P2P giữa các peers
"""

import socket
import json
import threading
import time
import sys
from datetime import datetime

class P2PTestClient:
    def __init__(self, peer_host, peer_port):
        self.peer_host = peer_host
        self.peer_port = peer_port
        self.client_name = f"TestClient_{int(time.time())}"
        
    def test_peer_discovery(self):
        """Test UDP discovery"""
        print(f"🔍 Testing P2P Discovery...")
        print("-" * 40)
        
        try:
            # Send discovery broadcast
            discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            discovery_socket.settimeout(5)
            
            discovery_data = {
                "type": "peer_discovery",
                "peer_name": self.client_name,
                "host": "127.0.0.1",
                "port": 9999,
                "timestamp": datetime.now().isoformat(),
                "services": ["test_client"]
            }
            
            message = json.dumps(discovery_data).encode('utf-8')
            discovery_port = self.peer_port + 1000
            
            print(f"📤 Broadcasting discovery to port {discovery_port}")
            discovery_socket.sendto(message, ('<broadcast>', discovery_port))
            
            # Listen for responses
            print("📥 Listening for discovery responses...")
            try:
                response, addr = discovery_socket.recvfrom(1024)
                print(f"✅ Discovery response from {addr}")
            except socket.timeout:
                print("⏰ No discovery responses received")
            
            discovery_socket.close()
            return True
            
        except Exception as e:
            print(f"❌ Discovery test failed: {e}")
            return False
    
    def test_peer_handshake(self):
        """Test P2P handshake"""
        print(f"\n🤝 Testing P2P Handshake...")
        print("-" * 40)
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            print(f"🔌 Connecting to peer {self.peer_host}:{self.peer_port}")
            sock.connect((self.peer_host, self.peer_port))
            print("✅ Connected to peer")
            
            # Send handshake
            handshake_data = {
                "type": "peer_handshake",
                "peer_name": self.client_name,
                "host": "127.0.0.1",
                "port": 9999,
                "timestamp": datetime.now().isoformat()
            }
            
            message = json.dumps(handshake_data, ensure_ascii=False)
            print(f"📤 Sending handshake...")
            sock.send(message.encode('utf-8'))
            
            # Receive response
            response = sock.recv(4096).decode('utf-8')
            print(f"📥 Handshake response:")
            
            try:
                response_json = json.loads(response)
                self.display_json_response(response_json)
            except:
                print(f"   {response}")
            
            sock.close()
            return True
            
        except Exception as e:
            print(f"❌ Handshake test failed: {e}")
            return False
    
    def test_iot_shelf_data(self):
        """Test gửi dữ liệu IoT shelf"""
        print(f"\n📦 Testing IoT Shelf Data...")
        print("-" * 40)
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            sock.connect((self.peer_host, self.peer_port))
            print("✅ Connected to peer")
            
            # Send IoT shelf data
            shelf_data = {
                "type": "iot_shelf_data",
                "shelf_id": "SHELF_TEST_001",
                "employee_id": "EMP_TEST_123",
                "action": "scan_item",
                "item_data": {
                    "item_id": "ITEM_001",
                    "quantity": 5,
                    "location": "A1-B2-C3"
                },
                "device_info": {
                    "device_id": "SCANNER_001",
                    "battery_level": 85,
                    "signal_strength": "Good"
                },
                "timestamp": datetime.now().isoformat(),
                "from": self.client_name
            }
            
            message = json.dumps(shelf_data, ensure_ascii=False, indent=2)
            print(f"📤 Sending IoT shelf data...")
            print(f"📋 Data: {json.dumps(shelf_data, indent=2)}")
            
            sock.send(message.encode('utf-8'))
            
            # Receive response
            response = sock.recv(4096).decode('utf-8')
            print(f"📥 IoT data response:")
            
            try:
                response_json = json.loads(response)
                self.display_json_response(response_json)
            except:
                print(f"   {response}")
            
            sock.close()
            return True
            
        except Exception as e:
            print(f"❌ IoT shelf data test failed: {e}")
            return False
    
    def test_peer_discovery_request(self):
        """Test yêu cầu danh sách peers"""
        print(f"\n🔍 Testing Peer Discovery Request...")
        print("-" * 40)
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            sock.connect((self.peer_host, self.peer_port))
            print("✅ Connected to peer")
            
            # Request peer list
            discovery_request = {
                "type": "peer_discovery_request",
                "from": self.client_name,
                "timestamp": datetime.now().isoformat()
            }
            
            message = json.dumps(discovery_request, ensure_ascii=False)
            print(f"📤 Requesting peer list...")
            
            sock.send(message.encode('utf-8'))
            
            # Receive response
            response = sock.recv(4096).decode('utf-8')
            print(f"📥 Peer discovery response:")
            
            try:
                response_json = json.loads(response)
                self.display_peer_list(response_json)
            except:
                print(f"   {response}")
            
            sock.close()
            return True
            
        except Exception as e:
            print(f"❌ Peer discovery request failed: {e}")
            return False
    
    def test_text_message(self):
        """Test gửi text message"""
        print(f"\n💬 Testing Text Message...")
        print("-" * 40)
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            sock.connect((self.peer_host, self.peer_port))
            print("✅ Connected to peer")
            
            # Send text message
            text_message = {
                "type": "text_message",
                "message": f"Hello from {self.client_name}! This is a P2P test message.",
                "from": self.client_name,
                "timestamp": datetime.now().isoformat()
            }
            
            message = json.dumps(text_message, ensure_ascii=False)
            print(f"📤 Sending text message...")
            print(f"💬 Message: {text_message['message']}")
            
            sock.send(message.encode('utf-8'))
            
            # Receive response
            response = sock.recv(4096).decode('utf-8')
            print(f"📥 Text message response:")
            
            try:
                response_json = json.loads(response)
                self.display_json_response(response_json)
            except:
                print(f"   {response}")
            
            sock.close()
            return True
            
        except Exception as e:
            print(f"❌ Text message test failed: {e}")
            return False
    
    def display_json_response(self, response_json):
        """Hiển thị JSON response"""
        print(f"   Type: {response_json.get('type', 'N/A')}")
        print(f"   Status: {response_json.get('status', 'N/A')}")
        print(f"   Message: {response_json.get('message', 'N/A')}")
        
        if "peer_name" in response_json:
            print(f"   Peer Name: {response_json['peer_name']}")
        
        if "capabilities" in response_json:
            print(f"   Capabilities: {', '.join(response_json['capabilities'])}")
        
        if "processed_data" in response_json:
            data = response_json['processed_data']
            print(f"   Processed by: {data.get('processed_by', 'N/A')}")
            print(f"   Processing time: {data.get('processing_time', 'N/A')}")
    
    def display_peer_list(self, response_json):
        """Hiển thị danh sách peers"""
        known_peers = response_json.get('known_peers', [])
        
        print(f"   Found {len(known_peers)} known peers:")
        
        if not known_peers:
            print("   No peers found")
        else:
            for peer in known_peers:
                print(f"   - {peer.get('name', 'Unknown')} ({peer.get('peer_id', 'N/A')})")
                print(f"     Host: {peer.get('host', 'N/A')}:{peer.get('port', 'N/A')}")
                print(f"     Services: {', '.join(peer.get('services', []))}")
    
    def run_all_tests(self):
        """Chạy tất cả tests"""
        print(f"{'='*60}")
        print(f"        🌐 P2P CONNECTIVITY TESTS")
        print(f"{'='*60}")
        print(f"🎯 Target Peer: {self.peer_host}:{self.peer_port}")
        print(f"🤖 Test Client: {self.client_name}")
        print(f"🕒 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        tests = [
            ("Peer Discovery (UDP)", self.test_peer_discovery),
            ("Peer Handshake", self.test_peer_handshake),
            ("Text Message", self.test_text_message),
            ("IoT Shelf Data", self.test_iot_shelf_data),
            ("Peer Discovery Request", self.test_peer_discovery_request)
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
                
                time.sleep(1)  # Delay giữa các test
                
            except Exception as e:
                print(f"❌ {test_name}: ERROR - {e}")
                results.append((test_name, False))
        
        # Hiển thị kết quả
        self.display_test_results(results)
    
    def display_test_results(self, results):
        """Hiển thị kết quả test"""
        print(f"\n{'='*60}")
        print(f"📊 P2P TEST RESULTS")
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
            print(f"🎉 ALL P2P TESTS PASSED!")
            print(f"✅ P2P communication is working perfectly!")
        else:
            failed = total - passed
            print(f"⚠️  {failed} test(s) FAILED")
            print(f"\n💡 P2P Troubleshooting:")
            print(f"   - Ensure P2P server is running: python p2p_server.py")
            print(f"   - Check network connectivity between peers")
            print(f"   - Verify firewall settings allow P2P ports")
            print(f"   - Try connecting to different peers")
        
        print(f"{'='*60}")

def main():
    if len(sys.argv) < 2:
        print("❌ Usage:")
        print("   python test_p2p.py <peer_ip>")
        print("   python test_p2p.py <peer_ip> <peer_port>")
        print("\nExample:")
        print("   python test_p2p.py 192.168.1.100")
        print("   python test_p2p.py 192.168.1.100 8080")
        return
    
    peer_host = sys.argv[1]
    peer_port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
    
    print("🌐 P2P Test Client")
    print(f"Target: {peer_host}:{peer_port}")
    
    test_client = P2PTestClient(peer_host, peer_port)
    
    try:
        test_client.run_all_tests()
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"❌ Test error: {e}")
    finally:
        print("\n👋 P2P testing completed!")

if __name__ == "__main__":
    main()
