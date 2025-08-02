# IoT Server LAN

Hệ thống server LAN cho IoT với khả năng tạo QR code và giao tiếp với Android app.

## 🚀 Chạy với Docker

### Prerequisites
- Docker
- Docker Compose

### Cách sử dụng

#### 1. Clone repository
```bash
git clone https://github.com/AnhDuc0912/IOT.server_lan.git
cd IOT.server_lan
```

#### 2. Chạy server với Docker Compose
```bash
# Chạy server
docker-compose up -d

# Xem logs
docker-compose logs -f iot-server

# Dừng server  
docker-compose down
```

#### 3. Tạo QR Code
```bash
# Chạy QR generator
docker-compose --profile tools run --rm qr-generator

# Hoặc chạy interactive để nhập thông tin
docker-compose --profile tools run --rm qr-generator python qr.py
```

#### 4. Truy cập server
- Server sẽ chạy tại: `http://localhost:8080`
- QR code sẽ được lưu trong thư mục hiện tại

### Environment Variables

Tạo file `.env` từ `.env.example`:
```bash
cp .env.example .env
```

Các biến có thể cấu hình:
- `HOST`: Địa chỉ IP server (mặc định: 0.0.0.0)
- `PORT`: Port server (mặc định: 8080)
- `SHELF_ID`: ID của shelf (mặc định: SHELF001)
- `EMPLOYEE_ID`: ID nhân viên (mặc định: EMP123)

## 🛠 Development

### Chạy local (không dùng Docker)
```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy server
python simple_server.py

# Tạo QR code
python qr.py
```

### Docker Commands hữu ích

```bash
# Build lại image
docker-compose build

# Chạy một command trong container
docker-compose exec iot-server bash

# Xem logs real-time
docker-compose logs -f

# Restart services
docker-compose restart

# Xóa tất cả (containers, networks, volumes)
docker-compose down -v --remove-orphans
```

## 📁 Cấu trúc project

```
IOT.server_lan/
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker services configuration
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── simple_server.py        # Main server application
├── qr.py                   # QR code generator
└── README.md              # This file
```

## 🔧 Troubleshooting

### Port đã được sử dụng
```bash
# Kiểm tra port đang được sử dụng
netstat -tulpn | grep :8080

# Thay đổi port trong docker-compose.yml
ports:
  - "8081:8080"  # Sử dụng port 8081 thay vì 8080
```

### Container không khởi động
```bash
# Xem logs chi tiết
docker-compose logs iot-server

# Rebuild container
docker-compose build --no-cache
docker-compose up -d
```
