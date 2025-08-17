#!/bin/bash
set -e

echo "Initializing Bluetooth services..."

# Khởi động dbus nếu chưa chạy
if ! pgrep -x "dbus-daemon" > /dev/null; then
    echo "Starting dbus..."
    dbus-daemon --system --fork
fi

# Khởi động bluetooth service
echo "Starting bluetooth service..."
service bluetooth start

# Đợi bluetooth service khởi động
sleep 3

# Kiểm tra bluetooth adapter
echo "Checking Bluetooth adapter..."
if hciconfig -a | grep -q "UP RUNNING"; then
    echo "Bluetooth adapter is ready"
else
    echo "Warning: No Bluetooth adapter found or not ready"
    echo "Available adapters:"
    hciconfig -a || echo "No adapters found"
fi

echo "Starting RFCOMM server..."
python3 /opt/rfcomm_server.py