FROM python:3.11-slim

# Cài đặt thư viện hệ thống cho OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt uv từ image chính thức
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy các file cấu hình của uv vào container
COPY pyproject.toml uv.lock ./

# Cài đặt các gói phụ thuộc (dependencies) dựa trên uv.lock
# --frozen đảm bảo không cập nhật lại phiên bản mới, giữ đúng như ở local
RUN uv sync --frozen --no-cache

# Copy mã nguồn còn lại
COPY . .

EXPOSE 8000

# Chạy app thông qua uv
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]