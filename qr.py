import qrcode
import json

import qrcode
import json
import socket

def get_local_ip():
    """Tự động lấy IP local"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

# Lấy IP tự động
auto_ip = get_local_ip()
print(f"🌐 IP hiện tại: {auto_ip}")

# Nhập thông tin
ip_lan = input(f"📝 Nhập IP Server (Enter để dùng {auto_ip}): ").strip()
if not ip_lan:
    ip_lan = auto_ip

port = 8080
custom_port = input(f"📝 Nhập Port (Enter để dùng {port}): ").strip()
if custom_port and custom_port.isdigit():
    port = int(custom_port)

shelf_id = "SHELF001"
employee_id = "EMP123"

print(f"\n📋 Thông tin QR Code:")
print(f"🌐 IP: {ip_lan}")
print(f"🔌 Port: {port}")
print(f"📦 Shelf ID: {shelf_id}")
print(f"👨‍💼 Employee ID: {employee_id}")

# Tạo dữ liệu dạng JSON
data = {
    "ip": ip_lan,
    "port": port,
    "shelf_id": shelf_id,
    "employee_id": employee_id,
    "action": "connect_to_shelf"
}
json_data = json.dumps(data)

# Tạo mã QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(json_data)
qr.make(fit=True)

# Tạo ảnh QR
img = qr.make_image(fill_color="black", back_color="white")

# Lưu ảnh QR
img.save("shelf_qr.png")
print("✅ QR Code đã được lưu thành 'shelf_qr.png'")
