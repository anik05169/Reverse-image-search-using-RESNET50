# docker/Dockerfile

# Update to 3.11-slim for better performance
FROM python:3.11-slim

# Install system dependencies (Required for Postgres and Image libraries)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install CPU-only PyTorch
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Keep the container alive
CMD ["tail", "-f", "/dev/null"]