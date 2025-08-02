# IoT P2P Server Guide

## 🌐 Peer-to-Peer IoT Communication

P2P Server cho phép các thiết bị IoT kết nối trực tiếp với nhau mà không cần server trung tâm.

## 🚀 Features

- ✅ **Peer Discovery**: Tự động tìm các peers trong mạng
- ✅ **Direct Communication**: Giao tiếp trực tiếp giữa các peers
- ✅ **IoT Data Sync**: Đồng bộ dữ liệu IoT shelf giữa các thiết bị
- ✅ **Broadcast Messages**: Gửi message đến tất cả peers
- ✅ **Auto-Reconnection**: Tự động kết nối lại khi peer online
- ✅ **Service Discovery**: Tìm kiếm services của peers

## 🛠 Cách sử dụng

### 1. Chạy P2P Server

#### Local:
```bash
python p2p_server.py
```

#### Docker:
```bash
# Start P2P server
docker-compose up -d p2p-server

# View logs
docker-compose logs -f p2p-server

# Interactive mode
docker-compose exec p2p-server python p2p_server.py
```

### 2. P2P Commands

Khi server đang chạy, bạn có thể sử dụng các commands:

```bash
# Xem danh sách peers
peers

# Kết nối đến peer khác
connect 192.168.1.100 8080

# Gửi message đến peer cụ thể
send 192.168.1.100:8080 Hello from peer!

# Broadcast message đến tất cả peers
broadcast Hello everyone!

# Gửi dữ liệu IoT shelf
shelf SHELF001 EMP123 scan_item

# Thoát
quit
```

### 3. Test P2P Connection

```bash
# Test kết nối P2P
python test_p2p.py <peer_ip>
python test_p2p.py <peer_ip> <peer_port>

# Example:
python test_p2p.py 192.168.1.100 8080
```

## 🏗 P2P Architecture

```
[Peer A] ←→ [Peer B] ←→ [Peer C]
    ↑           ↑           ↑
UDP Discovery  TCP Data   Broadcast
Port: 9080    Port: 8080   Messages
```

### Components:

1. **TCP Server**: Nhận kết nối P2P (port 8080)
2. **UDP Discovery**: Broadcast và nhận discovery (port 9080)
3. **Message Handler**: Xử lý các loại messages
4. **Peer Manager**: Quản lý danh sách peers

## 📡 Message Types

### 1. Peer Handshake
```json
{
  "type": "peer_handshake",
  "peer_name": "IoTPeer_192.168.1.100_8080",
  "host": "192.168.1.100",
  "port": 8080,
  "timestamp": "2025-08-02T10:30:00"
}
```

### 2. IoT Shelf Data
```json
{
  "type": "iot_shelf_data",
  "shelf_id": "SHELF001",
  "employee_id": "EMP123",
  "action": "scan_item",
  "from": "IoTPeer_192.168.1.100_8080",
  "timestamp": "2025-08-02T10:30:00"
}
```

### 3. Text Message
```json
{
  "type": "text_message",
  "message": "Hello from peer!",
  "from": "IoTPeer_192.168.1.100_8080",
  "timestamp": "2025-08-02T10:30:00"
}
```

### 4. Broadcast Message
```json
{
  "type": "broadcast_message",
  "message": "System maintenance in 5 minutes",
  "from": "IoTPeer_192.168.1.100_8080",
  "timestamp": "2025-08-02T10:30:00"
}
```

## 🔧 Configuration

### Environment Variables:
```bash
HOST=0.0.0.0           # Bind address
PORT=8080              # P2P communication port
PEER_NAME=MyIoTPeer    # Peer identifier
```

### Docker Ports:
- `8082:8080` - P2P communication
- `9082:9080` - P2P discovery (UDP)

## 🧪 Testing Scenarios

### Scenario 1: Two Peers Communication
```bash
# Terminal 1 - Peer A
python p2p_server.py
# Enter: IP=192.168.1.100, Port=8080, Name=PeerA

# Terminal 2 - Peer B  
python p2p_server.py
# Enter: IP=192.168.1.101, Port=8080, Name=PeerB

# In Peer A:
peers                           # Should show PeerB
connect 192.168.1.101 8080     # Connect to PeerB
send 192.168.1.101:8080 Hello! # Send message
```

### Scenario 2: IoT Shelf Data Sync
```bash
# Peer A sends shelf data
shelf SHELF001 EMP123 pick_item

# All connected peers receive and process the data
```

### Scenario 3: Broadcast Alert
```bash
# Send alert to all peers
broadcast "Emergency: Evacuate warehouse area A"
```

## 🔍 Troubleshooting

### Peer Discovery Issues:
```bash
# Check UDP port
netstat -u | grep 9080

# Test UDP broadcast
python -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.sendto(b'test', ('<broadcast>', 9080))
"
```

### Connection Issues:
```bash
# Check TCP port
netstat -t | grep 8080

# Test TCP connection
telnet 192.168.1.100 8080
```

### Docker Issues:
```bash
# Check container
docker-compose ps p2p-server

# View logs
docker-compose logs p2p-server

# Enter interactive mode
docker-compose exec p2p-server bash
```

## 📊 Monitoring

### Log Messages:
- 🔍 `Discovered peer: PeerName at IP:Port`
- 🤝 `P2P Handshake from: PeerName`
- 📦 `IoT Shelf Data from IP:Port`
- 📢 `Broadcasting to X known peers`

### Status Commands:
```bash
peers          # Show all known peers
connections    # Show active connections (if implemented)
```

## 🚀 Advanced Usage

### Custom Message Types:
Extend `process_p2p_message()` để xử lý message types mới:

```python
def process_p2p_message(self, message_data, peer_id):
    message_type = message_data.get("type", "unknown")
    
    if message_type == "custom_iot_command":
        return self.handle_custom_iot_command(message_data, peer_id)
    # ... existing handlers
```

### Load Balancing:
Phân phối công việc giữa các peers:

```python
def distribute_work(self, work_data):
    available_peers = [p for p in self.peers if self.is_peer_available(p)]
    selected_peer = self.select_least_busy_peer(available_peers)
    self.send_to_peer(selected_peer, work_data)
```

## 🔒 Security Notes

- Hiện tại chưa có encryption - chỉ dùng trong mạng nội bộ tin cậy
- Validate tất cả input từ peers
- Monitor cho unusual traffic patterns
- Consider implementing authentication cho production

## 📈 Performance Tips

- Sử dụng connection pooling cho frequent communication
- Implement heartbeat để detect dead peers
- Cache peer capabilities để tránh repeated discovery
- Use compression cho large data transfers
