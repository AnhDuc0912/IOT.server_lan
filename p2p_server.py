#!/usr/bin/env python3
"""
IoT P2P Server - Peer to Peer Communication
Cho phép các thiết bị kết nối trực tiếp với nhau
"""

import socket
import threading
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Set

class IoTPeer:
    def __init__(self, host=None, port=8080, peer_name=None):
        self.host = host if host else self.get_local_ip()
        self.port = port
        self.peer_name = peer_name if peer_name else f"Peer_{self.host}_{port}"
        
        # P2P State
        self.server_socket = None
        self.running = False
        self.peers: Dict[str, dict] = {}  # Known peers
        self.connections: Dict[str, socket.socket] = {}  # Active connections
        self.discovery_port = port + 1000  # Discovery port
        
    def get_local_ip(self):
        """Lấy IP local"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "localhost"
    
    def start_peer(self):
        """Khởi động P2P peer"""
        print(f"🚀 Starting P2P IoT Peer: {self.peer_name}")
        print(f"🌐 Address: {self.host}:{self.port}")
        print(f"🔍 Discovery: {self.host}:{self.discovery_port}")
        print("-" * 60)
        
        # Start server thread
        server_thread = threading.Thread(target=self.start_server, daemon=True)
        server_thread.start()
        
        # Start discovery thread
        discovery_thread = threading.Thread(target=self.start_discovery, daemon=True)
        discovery_thread.start()
        
        # Start peer discovery broadcast
        broadcast_thread = threading.Thread(target=self.broadcast_presence, daemon=True)
        broadcast_thread.start()
        
        # Main loop
        self.running = True
        try:
            self.main_loop()
        except KeyboardInterrupt:
            self.stop_peer()
    
    def start_server(self):
        """Khởi động server để nhận kết nối"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(10)
            
            print(f"📡 Server listening on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"📲 New P2P connection from: {client_address}")
                    
                    # Handle P2P connection
                    client_thread = threading.Thread(
                        target=self.handle_peer_connection,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except Exception as e:
                    if self.running:
                        print(f"❌ Server accept error: {e}")
                        
        except Exception as e:
            print(f"❌ Server start error: {e}")
    
    def start_discovery(self):
        """Khởi động UDP discovery service"""
        try:
            discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            discovery_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            discovery_socket.bind(('0.0.0.0', self.discovery_port))
            
            print(f"🔍 Discovery service on port {self.discovery_port}")
            
            while self.running:
                try:
                    data, addr = discovery_socket.recvfrom(1024)
                    self.handle_discovery_message(data, addr)
                except Exception as e:
                    if self.running:
                        print(f"❌ Discovery error: {e}")
                        
        except Exception as e:
            print(f"❌ Discovery start error: {e}")
    
    def broadcast_presence(self):
        """Broadcast sự hiện diện của peer"""
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        while self.running:
            try:
                discovery_data = {
                    "type": "peer_discovery",
                    "peer_name": self.peer_name,
                    "host": self.host,
                    "port": self.port,
                    "timestamp": datetime.now().isoformat(),
                    "services": ["iot_shelf", "p2p_communication"]
                }
                
                message = json.dumps(discovery_data).encode('utf-8')
                
                # Broadcast to local network
                broadcast_socket.sendto(message, ('<broadcast>', self.discovery_port))
                
                time.sleep(30)  # Broadcast every 30 seconds
                
            except Exception as e:
                print(f"❌ Broadcast error: {e}")
                time.sleep(30)
    
    def handle_discovery_message(self, data, addr):
        """Xử lý discovery message"""
        try:
            message = json.loads(data.decode('utf-8'))
            
            if message.get("type") == "peer_discovery":
                peer_name = message.get("peer_name")
                peer_host = message.get("host")
                peer_port = message.get("port")
                
                # Don't add self
                if peer_name == self.peer_name:
                    return
                
                # Add to known peers
                peer_id = f"{peer_host}:{peer_port}"
                self.peers[peer_id] = {
                    "name": peer_name,
                    "host": peer_host,
                    "port": peer_port,
                    "last_seen": datetime.now(),
                    "services": message.get("services", [])
                }
                
                print(f"🔍 Discovered peer: {peer_name} at {peer_id}")
                
        except Exception as e:
            print(f"❌ Discovery message error: {e}")
    
    def handle_peer_connection(self, client_socket, client_address):
        """Xử lý kết nối P2P"""
        peer_id = f"{client_address[0]}:{client_address[1]}"
        
        try:
            client_socket.settimeout(60)
            
            while self.running:
                data = client_socket.recv(4096).decode('utf-8')
                
                if not data:
                    break
                
                print(f"📨 P2P Message from {peer_id}:")
                print(f"   Content: {data}")
                
                try:
                    json_data = json.loads(data)
                    response = self.process_p2p_message(json_data, peer_id)
                    
                    response_json = json.dumps(response, ensure_ascii=False)
                    client_socket.send(response_json.encode('utf-8'))
                    
                except json.JSONDecodeError:
                    # Plain text message
                    response = {
                        "type": "text_response",
                        "message": f"Message received by {self.peer_name}",
                        "timestamp": datetime.now().isoformat()
                    }
                    client_socket.send(json.dumps(response).encode('utf-8'))
                
        except socket.timeout:
            print(f"⏰ P2P connection timeout: {peer_id}")
        except Exception as e:
            print(f"❌ P2P connection error {peer_id}: {e}")
        finally:
            try:
                client_socket.close()
                print(f"🔌 Closed P2P connection: {peer_id}")
            except:
                pass
    
    def process_p2p_message(self, message_data, peer_id):
        """Xử lý P2P message"""
        message_type = message_data.get("type", "unknown")
        
        if message_type == "peer_handshake":
            return self.handle_peer_handshake(message_data, peer_id)
        elif message_type == "iot_shelf_data":
            return self.handle_iot_shelf_data(message_data, peer_id)
        elif message_type == "peer_discovery_request":
            return self.handle_discovery_request(message_data, peer_id)
        else:
            return {
                "type": "p2p_response",
                "status": "success",
                "message": f"Message processed by {self.peer_name}",
                "original_type": message_type,
                "timestamp": datetime.now().isoformat(),
                "peer_info": {
                    "name": self.peer_name,
                    "host": self.host,
                    "port": self.port
                }
            }
    
    def handle_peer_handshake(self, data, peer_id):
        """Xử lý handshake P2P"""
        peer_name = data.get("peer_name", "Unknown")
        
        print(f"🤝 P2P Handshake from: {peer_name} ({peer_id})")
        
        return {
            "type": "handshake_response",
            "status": "success",
            "peer_name": self.peer_name,
            "message": f"Handshake accepted by {self.peer_name}",
            "capabilities": ["iot_shelf", "p2p_communication", "data_sync"],
            "timestamp": datetime.now().isoformat()
        }
    
    def handle_iot_shelf_data(self, data, peer_id):
        """Xử lý dữ liệu IoT shelf"""
        shelf_id = data.get("shelf_id", "Unknown")
        employee_id = data.get("employee_id", "Unknown")
        action = data.get("action", "Unknown")
        
        print(f"📦 IoT Shelf Data from {peer_id}:")
        print(f"   Shelf ID: {shelf_id}")
        print(f"   Employee ID: {employee_id}")
        print(f"   Action: {action}")
        
        # Process IoT data here
        # Can sync with local database, forward to other peers, etc.
        
        return {
            "type": "iot_shelf_response",
            "status": "success",
            "message": f"Shelf data processed by {self.peer_name}",
            "processed_data": {
                "shelf_id": shelf_id,
                "employee_id": employee_id,
                "action": action,
                "processed_by": self.peer_name,
                "processing_time": datetime.now().isoformat()
            }
        }
    
    def handle_discovery_request(self, data, peer_id):
        """Xử lý yêu cầu discovery"""
        return {
            "type": "discovery_response",
            "known_peers": [
                {
                    "peer_id": pid,
                    "name": info["name"],
                    "host": info["host"],
                    "port": info["port"],
                    "services": info.get("services", [])
                }
                for pid, info in self.peers.items()
            ],
            "timestamp": datetime.now().isoformat()
        }
    
    def connect_to_peer(self, peer_host, peer_port):
        """Kết nối đến peer khác"""
        peer_id = f"{peer_host}:{peer_port}"
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((peer_host, peer_port))
            
            # Handshake
            handshake_data = {
                "type": "peer_handshake",
                "peer_name": self.peer_name,
                "host": self.host,
                "port": self.port,
                "timestamp": datetime.now().isoformat()
            }
            
            sock.send(json.dumps(handshake_data).encode('utf-8'))
            response = sock.recv(4096).decode('utf-8')
            
            print(f"🤝 Connected to peer: {peer_id}")
            print(f"📥 Handshake response: {response}")
            
            self.connections[peer_id] = sock
            return sock
            
        except Exception as e:
            print(f"❌ Failed to connect to peer {peer_id}: {e}")
            return None
    
    def send_to_peer(self, peer_id, message_data):
        """Gửi message đến peer cụ thể"""
        if peer_id not in self.connections:
            # Try to connect
            host, port = peer_id.split(':')
            if not self.connect_to_peer(host, int(port)):
                return False
        
        try:
            sock = self.connections[peer_id]
            message = json.dumps(message_data, ensure_ascii=False)
            sock.send(message.encode('utf-8'))
            
            response = sock.recv(4096).decode('utf-8')
            print(f"🔄 Response from {peer_id}: {response}")
            return True
            
        except Exception as e:
            print(f"❌ Send to peer error {peer_id}: {e}")
            # Remove failed connection
            if peer_id in self.connections:
                del self.connections[peer_id]
            return False
    
    def broadcast_to_peers(self, message_data):
        """Broadcast message đến tất cả peers"""
        print(f"📢 Broadcasting to {len(self.peers)} known peers...")
        
        for peer_id in list(self.peers.keys()):
            success = self.send_to_peer(peer_id, message_data)
            if success:
                print(f"✅ Broadcasted to {peer_id}")
            else:
                print(f"❌ Failed to broadcast to {peer_id}")
    
    def main_loop(self):
        """Main command loop"""
        print(f"\n💡 P2P IoT Peer Commands:")
        print("  'peers' - Show known peers")
        print("  'connect <host> <port>' - Connect to peer")
        print("  'send <peer_id> <message>' - Send message")
        print("  'broadcast <message>' - Broadcast to all peers")
        print("  'shelf <shelf_id> <employee_id> <action>' - Send IoT shelf data")
        print("  'quit' - Exit")
        print("-" * 60)
        
        while self.running:
            try:
                command = input(f"[{self.peer_name}]> ").strip()
                
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0].lower()
                
                if cmd == 'quit':
                    break
                elif cmd == 'peers':
                    self.show_peers()
                elif cmd == 'connect' and len(parts) >= 3:
                    self.connect_to_peer(parts[1], int(parts[2]))
                elif cmd == 'send' and len(parts) >= 3:
                    peer_id = parts[1]
                    message = ' '.join(parts[2:])
                    self.send_message_to_peer(peer_id, message)
                elif cmd == 'broadcast' and len(parts) >= 2:
                    message = ' '.join(parts[1:])
                    self.broadcast_message(message)
                elif cmd == 'shelf' and len(parts) >= 4:
                    self.send_shelf_data(parts[1], parts[2], parts[3])
                else:
                    print("❌ Invalid command or parameters")
                    
            except EOFError:
                break
            except Exception as e:
                print(f"❌ Command error: {e}")
    
    def show_peers(self):
        """Hiển thị danh sách peers"""
        print(f"\n📋 Known Peers ({len(self.peers)}):")
        print("-" * 50)
        
        if not self.peers:
            print("   No peers discovered yet")
        else:
            for peer_id, info in self.peers.items():
                status = "🟢 Connected" if peer_id in self.connections else "🔴 Not connected"
                last_seen = info['last_seen'].strftime('%H:%M:%S')
                print(f"   {info['name']} ({peer_id}) - {status}")
                print(f"      Last seen: {last_seen}")
                print(f"      Services: {', '.join(info.get('services', []))}")
        
        print("-" * 50)
    
    def send_message_to_peer(self, peer_id, message):
        """Gửi text message đến peer"""
        message_data = {
            "type": "text_message",
            "message": message,
            "from": self.peer_name,
            "timestamp": datetime.now().isoformat()
        }
        
        self.send_to_peer(peer_id, message_data)
    
    def broadcast_message(self, message):
        """Broadcast text message"""
        message_data = {
            "type": "broadcast_message",
            "message": message,
            "from": self.peer_name,
            "timestamp": datetime.now().isoformat()
        }
        
        self.broadcast_to_peers(message_data)
    
    def send_shelf_data(self, shelf_id, employee_id, action):
        """Gửi dữ liệu IoT shelf"""
        shelf_data = {
            "type": "iot_shelf_data",
            "shelf_id": shelf_id,
            "employee_id": employee_id,
            "action": action,
            "from": self.peer_name,
            "timestamp": datetime.now().isoformat()
        }
        
        self.broadcast_to_peers(shelf_data)
    
    def stop_peer(self):
        """Dừng P2P peer"""
        print("\n🛑 Stopping P2P peer...")
        self.running = False
        
        # Close all connections
        for peer_id, sock in self.connections.items():
            try:
                sock.close()
            except:
                pass
        
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("👋 P2P peer stopped!")

def main():
    print("="*60)
    print("        🌐 IOT P2P SERVER - PEER TO PEER")
    print("="*60)
    
    # Configuration
    host = input("📝 Enter IP (Enter = auto-detect): ").strip()
    if not host:
        peer = IoTPeer()
        host = peer.get_local_ip()
    
    port_input = input(f"📝 Enter Port (Enter = 8080): ").strip()
    port = int(port_input) if port_input.isdigit() else 8080
    
    peer_name = input(f"📝 Enter Peer Name (Enter = auto): ").strip()
    if not peer_name:
        peer_name = f"IoTPeer_{host}_{port}"
    
    print(f"\n🎯 Starting P2P Peer:")
    print(f"   Name: {peer_name}")
    print(f"   Address: {host}:{port}")
    print(f"   Discovery: {host}:{port + 1000}")
    
    # Create and start peer
    peer = IoTPeer(host, port, peer_name)
    
    try:
        peer.start_peer()
    except KeyboardInterrupt:
        peer.stop_peer()

if __name__ == "__main__":
    main()
