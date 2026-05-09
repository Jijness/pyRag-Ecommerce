FROM python:3.10-slim

WORKDIR /app

# Install system dependencies cho mysqlclient và matplotlib
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8007

# Chạy Django với uvicorn ASGI (có thể dùng daphne nếu muốn, nhưng uvicorn thông dụng)
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8007"]
