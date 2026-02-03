####################
# Stage 1: Build frontend assets
####################
FROM node:20-alpine AS frontend-builder

WORKDIR /code

# Copy only package files for better layer caching
COPY ./static/package*.json /code/static/

# Install npm dependencies
RUN cd /code/static && npm ci --only=production

####################
# Stage 2: Build Python dependencies
####################
FROM ubuntu:24.04 AS python-builder

# Build arguments
ARG UV_VERSION="0.8.18"
ARG UV_HASH="e7e78475c6d6cfeac5cb96b01ac50e22df5af97dc1e0d5a5e75ce682b3e4a54b"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CMAKE_POLICY_VERSION_MINIMUM=3.5 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /code

# Install build dependencies for compilation
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        gcc \
        g++ \
        python3-dev \
        git \
        libre2-dev \
        build-essential \
        pkg-config \
        cmake \
        ninja-build \
        clang \
        postgresql-client \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster Python package management
RUN curl -sSL "https://github.com/astral-sh/uv/releases/download/${UV_VERSION}/uv-x86_64-unknown-linux-gnu.tar.gz" > uv.tar.gz && \
    echo "${UV_HASH}  uv.tar.gz" | sha256sum -c - && \
    tar xf uv.tar.gz -C /tmp/ && \
    mv /tmp/uv-x86_64-unknown-linux-gnu/uv /usr/local/bin/uv && \
    mv /tmp/uv-x86_64-unknown-linux-gnu/uvx /usr/local/bin/uvx && \
    rm -rf /tmp/uv* uv.tar.gz

# Copy dependency files
COPY pyproject.toml uv.lock .python-version ./

# Install Python and dependencies using uv
RUN uv python install $(cat .python-version) && \
    uv sync --locked --no-dev

####################
# Stage 3: Production runtime
####################
FROM ubuntu:24.04 AS production

# Metadata labels
LABEL maintainer="SimpleLogin <dev@simplelogin.io>" \
      description="SimpleLogin - Open source email alias solution" \
      version="latest"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/code/.venv/bin:$PATH" \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /code

# Install only runtime dependencies (no build tools)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        libre2-11 \
        libpq5 \
        postgresql-client \
        bash \
        wget \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -g 1000 simplelogin && \
    useradd -r -u 1000 -g simplelogin -s /bin/bash simplelogin

# Copy Python environment from builder
COPY --from=python-builder --chown=simplelogin:simplelogin /code/.venv /code/.venv

# Copy application code
COPY --chown=simplelogin:simplelogin . .

# Copy frontend assets from frontend builder
COPY --from=frontend-builder --chown=simplelogin:simplelogin /code/static/node_modules /code/static/node_modules

# Create necessary directories with proper permissions
RUN mkdir -p /code/static/upload && \
    chown -R simplelogin:simplelogin /code

# Switch to non-root user
USER simplelogin

# Expose application port
EXPOSE 7777

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:7777/health || exit 1

# Default command to run the application
CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:7777", "-w", "2", "--timeout", "15", "--log-level", "INFO"]

