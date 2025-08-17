#!/usr/bin/env python3
import bluetooth

SPP_UUID = "00001101-0000-1000-8000-00805f9b34fb"

def main():
    # Tạo socket RFCOMM
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)
    port = server_sock.getsockname()[1]

    # Quảng cáo dịch vụ SPP để Android tìm thấy
    bluetooth.advertise_service(
        server_sock,
        "JetsonSPPServer",
        service_id=SPP_UUID,
        service_classes=[SPP_UUID, bluetooth.SERIAL_PORT_CLASS],
        profiles=[bluetooth.SERIAL_PORT_PROFILE]
    )

    print(f"🔵 Jetson Nano Bluetooth RFCOMM server đang chờ kết nối trên channel {port}")
    print(f"🆔 UUID: {SPP_UUID}")

    try:
        client_sock, client_info = server_sock.accept()
        print(f"✅ Đã nhận kết nối từ: {client_info}")

        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            text = data.decode("utf-8")
            print(f"📱 Nhận từ điện thoại: {text}")
            # Phản hồi lại
            response = f"Jetson nhận: {text}"
            client_sock.send(response.encode("utf-8"))
            print(f"🖥️ Đã gửi lại: {response}")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        client_sock.close()
        server_sock.close()
        print("🛑 Đã đóng kết nối Bluetooth.")

if __name__ == "__main__":
    main()