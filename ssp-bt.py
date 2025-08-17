#!/usr/bin/env python3
import socket, subprocess, re

CHANNEL = 1
ADAPTER_MAC = "A0:C5:89:E8:E1:1B"   # <-- dùng MAC thật của Jetson (bluetoothctl show)

def ensure_adapter_up():
    # Đảm bảo adapter bật (không bắt buộc nếu bạn đã bật rồi)
    try:
        out = subprocess.check_output(["bluetoothctl", "show"], text=True)
        if "Powered: no" in out:
            subprocess.run(["bluetoothctl", "power", "on"], check=False)
    except Exception:
        pass

def main():
    ensure_adapter_up()

    srv = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

    # Một số hệ không nhận "" (BDADDR_ANY). Hãy bind bằng MAC của adapter.
    srv.bind((ADAPTER_MAC, CHANNEL))   # trước đây là ("", CHANNEL)
    srv.listen(1)
    print(f"🔵 SPP server listening on {ADAPTER_MAC}, RFCOMM channel {CHANNEL}")

    client, addr = srv.accept()
    print("✅ Connected from:", addr)
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            msg = data.decode("utf-8", errors="replace")
            print("📱 RX:", msg)
            reply = f"Jetson received: {msg}"
            client.sendall(reply.encode("utf-8"))
            print("🖥️ TX:", reply)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("❌ Error:", e)
    finally:
        try: client.close()
        except: pass
        srv.close()
        print("🛑 Closed RFCOMM.")

if __name__ == "__main__":
    main()
