# Sử dụng Python 3.11 slim làm base image
FROM python:3.11-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các gói hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file trước để tận dụng Docker layer caching
COPY requirements.txt .

# Cài đặt Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

# Tạo thư mục cho QR codes nếu cần
RUN mkdir -p /app/qr_codes

# Expose port 8080 (port mặc định của server)
EXPOSE 8080

# Thiết lập biến môi trường
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8080

# Command mặc định để chạy server
CMD ["python", "simple_server.py"]
