# Testing Guide - IoT Server LAN

## 🧪 Hướng dẫn test kết nối giữa máy local và Docker container

### 1. Chuẩn bị

#### Trên máy Server (Docker host):
```bash
# Clone repo và start Docker container
git clone https://github.com/AnhDuc0912/IOT.server_lan.git
cd IOT.server_lan

# Start Docker container
docker-compose up -d

# Check container status
docker-compose ps
docker-compose logs iot-server
```

#### Trên máy Local (Test client):
```bash
# Clone repo (hoặc chỉ copy file test)
git clone https://github.com/AnhDuc0912/IOT.server_lan.git
cd IOT.server_lan

# Hoặc chỉ cần download các file test:
# - test_docker.py
# - test_network.py  
# - test_quick.py
```

### 2. Các loại test

## 🚀 Test nhanh (Quick Test)
```bash
# Test cơ bản
python test_quick.py

# Test với IP và port cụ thể
python test_quick.py 192.168.1.100 8081
```

## 🐳 Test Docker connectivity
```bash
# Test kết nối đến Docker container
python test_docker.py <SERVER_IP>
python test_docker.py <SERVER_IP> <PORT>

# Ví dụ:
python test_docker.py 192.168.1.100
python test_docker.py 192.168.1.100 8081
```

## 🌐 Test network toàn diện
```bash
# Test đầy đủ (ping, port, connection, data)
python test_network.py
```

### 3. Kết quả mong đợi

#### ✅ Test thành công:
```
🎉 Docker connection test PASSED!
✅ Your machine can connect to the Docker container
```

#### ❌ Test thất bại:
```
❌ Docker connection test FAILED!
💡 Troubleshooting checklist:
   1. Is Docker container running?
   2. Check container logs
   3. Verify port mapping
   4. Check server firewall
```

### 4. Troubleshooting

#### Lỗi "Connection refused"
```bash
# Check Docker container
docker-compose ps
docker-compose logs iot-server

# Restart if needed
docker-compose restart iot-server
```

#### Lỗi "Connection timeout"
```bash
# Check firewall on server
# Windows:
netsh advfirewall firewall add rule name="IoT Server" dir=in action=allow protocol=TCP localport=8081

# Linux:
sudo ufw allow 8081
```

#### Lỗi "Port not reachable"
```bash
# Check port mapping in docker-compose.yml
ports:
  - "8081:8080"  # External:Internal

# Check if port is in use
netstat -tulpn | grep 8081
```

### 5. Kiểm tra manual

#### Test với telnet:
```bash
telnet <SERVER_IP> 8081
```

#### Test với curl:
```bash
curl -v telnet://<SERVER_IP>:8081
```

#### Check Docker container:
```bash
# Container status
docker-compose ps

# Container logs
docker-compose logs -f iot-server

# Execute command in container
docker-compose exec iot-server python --version
```

### 6. Network topology

```
[Local Machine] -----> [Server Machine] -----> [Docker Container]
     |                        |                        |
  test_*.py              Docker Host                iot-server
                         Port: 8081                Port: 8080
```

- **Local Machine**: Chạy test scripts
- **Server Machine**: Host Docker container  
- **Docker Container**: IoT Server application

### 7. Expected Data Flow

1. **Local machine** gửi JSON data đến **Docker container**
2. **Docker container** nhận data và xử lý
3. **Docker container** gửi response về **Local machine**
4. **Local machine** hiển thị kết quả

### 8. Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Connection refused | Container not running | `docker-compose up -d` |
| Timeout | Firewall blocking | Open port 8081 |
| Port not reachable | Wrong port mapping | Check docker-compose.yml |
| DNS resolution | Wrong IP/hostname | Use IP address instead |

### 9. Test với nhiều clients

```bash
# Terminal 1
python test_docker.py 192.168.1.100 8081

# Terminal 2 (cùng lúc)
python test_docker.py 192.168.1.100 8081

# Terminal 3 (stress test)
for i in {1..10}; do python test_quick.py 192.168.1.100 8081; done
```
