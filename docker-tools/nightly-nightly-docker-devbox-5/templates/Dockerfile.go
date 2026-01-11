# Go 1.21 Development Environment
FROM golang:1.21-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV GOPATH=/go
ENV GO111MODULE=on
ENV CGO_ENABLED=0

# Install Go tools
RUN go install golang.org/x/tools/cmd/goimports@latest
RUN go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
RUN go install github.com/cosmtrek/air@latest

# Create source and data directories
RUN mkdir -p /app/src /app/data

# Set permissions
RUN useradd -m -s /bin/bash devuser && chown -R devuser:devuser /app
USER devuser

# Default command
CMD ["/bin/bash"]
