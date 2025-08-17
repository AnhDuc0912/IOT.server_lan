#!/usr/bin/env python3
import socket

CHANNEL = 1  # khớp với sdptool add --channel=1 SP

srv = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
srv.bind(("", CHANNEL))
srv.listen(1)
print(f"🔵 Jetson SPP server listening on RFCOMM channel {CHANNEL}")

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
    client.close()
    srv.close()
    print("🛑 Closed RFCOMM.")
