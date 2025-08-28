# Build stage - compile dependencies
FROM python:3.12-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install build dependencies for compiling Python packages
RUN apk add --no-cache \
    gcc g++ musl-dev linux-headers \
    libffi-dev openssl-dev \
    rust cargo

# Install Python deps (will compile from source)
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage - clean minimal image
FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH

WORKDIR /app

# Install only runtime dependencies
RUN apk add --no-cache curl ca-certificates

# Copy compiled packages from builder stage
COPY --from=builder /root/.local /root/.local

# Copy source (compose will mount a volume over this in dev)
COPY . .

# Default command is overridden per-service in docker-compose.yml
CMD ["python","-V"]