import socket
import threading
import json
import sys
from datetime import datetime

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

class SimpleIOTServer:
    def __init__(self, host=None, port=8080):
        self.host = host if host else get_local_ip()
        self.port = port
        self.server_socket = None
        self.running = False
        
    def start_server(self):
        """Khởi động server đơn giản"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Thử bind với IP cụ thể, nếu không được thì dùng 0.0.0.0
            try:
                self.server_socket.bind((self.host, self.port))
                print(f"🚀 Server đang chạy tại: {self.host}:{self.port}")
            except Exception as e:
                print(f"❌ Không thể bind với {self.host}:{self.port}")
                print(f"🔄 Thử bind với 0.0.0.0:{self.port}")
                self.server_socket.bind(('0.0.0.0', self.port))
                print(f"🚀 Server đang chạy tại: 0.0.0.0:{self.port}")
                print(f"📱 Có thể truy cập qua: {self.host}:{self.port}")
            
            self.server_socket.listen(5)
            self.running = True
            
            print(f"📋 Shelf ID: SHELF001")
            print(f"👨‍💼 Employee ID: EMP123")
            print("-" * 60)
            print("🔍 Đang chờ kết nối từ Android app...")
            print("💡 Nhấn Ctrl+C để dừng server")
            print("-" * 60)
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"\n📲 KẾT NỐI MỚI từ: {client_address}")
                    
                    # Tạo thread để xử lý client
                    client_thread = threading.Thread(
                        target=self.handle_client, 
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except Exception as e:
                    if self.running:
                        print(f"❌ Lỗi accept connection: {e}")
                    
        except Exception as e:
            print(f"❌ Lỗi khởi động server: {e}")
            print(f"💡 Kiểm tra:")
            print(f"   - Port {self.port} có bị chiếm không?")
            print(f"   - Firewall có chặn không?")
            print(f"   - IP {self.host} có đúng không?")
            
    def handle_client(self, client_socket, client_address):
        """Xử lý client kết nối"""
        try:
            # Set timeout cho socket
            client_socket.settimeout(30)
            
            print(f"🔗 Đang xử lý client: {client_address}")
            
            # Nhận dữ liệu
            data = client_socket.recv(4096).decode('utf-8')
            
            if data:
                print(f"📨 NHẬN DỮ LIỆU:")
                print(f"   Từ: {client_address}")
                print(f"   Nội dung: {data}")
                
                try:
                    # Parse JSON
                    json_data = json.loads(data)
                    self.display_connection_info(json_data, client_address)
                    
                    # Tạo response
                    response = {
                        "status": "success",
                        "message": "Kết nối thành công với IOT Server!",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "server_info": {
                            "shelf_id": "SHELF001",
                            "employee_id": "EMP123",
                            "server_ip": self.host,
                            "server_port": self.port
                        }
                    }
                    
                    response_json = json.dumps(response, ensure_ascii=False)
                    client_socket.send(response_json.encode('utf-8'))
                    print(f"✅ Đã gửi response về client")
                    
                except json.JSONDecodeError:
                    # Nếu không phải JSON
                    print(f"📝 Text message: {data}")
                    response = "Message received successfully"
                    client_socket.send(response.encode('utf-8'))
                    
            else:
                print(f"❌ Không nhận được dữ liệu từ {client_address}")
                
        except socket.timeout:
            print(f"⏰ Timeout với client {client_address}")
        except Exception as e:
            print(f"❌ Lỗi xử lý client {client_address}: {e}")
        finally:
            try:
                client_socket.close()
                print(f"🔌 Đã đóng kết nối với {client_address}")
            except:
                pass
            print("-" * 40)
            
    def display_connection_info(self, json_data, client_address):
        """Hiển thị thông tin kết nối"""
        print(f"\n{'='*50}")
        print(f"📋 THÔNG TIN KẾT NỐI IOT")
        print(f"{'='*50}")
        print(f"🕒 Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📱 Địa chỉ client: {client_address[0]}:{client_address[1]}")
        
        if "action" in json_data:
            print(f"🎯 Hành động: {json_data['action']}")
            
        if "qr_data" in json_data:
            qr_info = json_data["qr_data"]
            print(f"📦 Shelf ID: {qr_info.get('shelf_id', 'N/A')}")
            print(f"👨‍💼 Employee ID: {qr_info.get('employee_id', 'N/A')}")
            print(f"🌐 Target IP: {qr_info.get('ip', 'N/A')}")
            print(f"🔌 Target Port: {qr_info.get('port', 'N/A')}")
            
        if "device_info" in json_data:
            device = json_data["device_info"]
            print(f"📲 Thiết bị: {device.get('model', 'N/A')}")
            print(f"🤖 Android: {device.get('android_version', 'N/A')}")
            print(f"📱 App: {device.get('app_name', 'N/A')}")
            
        print(f"{'='*50}")
        
    def stop_server(self):
        """Dừng server"""
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
                print("\n🛑 Server đã dừng")
            except:
                pass

def main():
    print("="*60)
    print("        🚀 IOT PYTHON SERVER - SIMPLE VERSION")
    print("="*60)
    
    # Lấy IP tự động
    local_ip = get_local_ip()
    print(f"🌐 IP hiện tại: {local_ip}")
    
    # Cho phép user nhập IP khác nếu muốn
    custom_ip = input(f"📝 Nhập IP khác (Enter để dùng {local_ip}): ").strip()
    if custom_ip:
        local_ip = custom_ip
        
    port = 8080
    custom_port = input(f"📝 Nhập Port khác (Enter để dùng {port}): ").strip()
    if custom_port and custom_port.isdigit():
        port = int(custom_port)
    
    print(f"\n🎯 Sẽ khởi động server tại: {local_ip}:{port}")
    print(f"📱 QR Code cần chứa IP này: {local_ip}")
    
    server = SimpleIOTServer(local_ip, port)
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n⏹️  Đang dừng server...")
        server.stop_server()
        print("👋 Tạm biệt!")

if __name__ == "__main__":
    main()
