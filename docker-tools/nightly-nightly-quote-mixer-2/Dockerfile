# syntax=docker/dockerfile:1

# ---------- Builder stage ----------
FROM golang:1.22-alpine AS builder
WORKDIR /app

# Copy go.mod and source files
COPY src/go.mod ./
COPY src/main.go ./

# Build the binary
RUN CGO_ENABLED=0 GOOS=linux go build -o /quote-mixer

# ---------- Runtime stage ----------
FROM alpine:3.18
COPY --from=builder /quote-mixer /quote-mixer
EXPOSE 8080
ENTRYPOINT [\"/quote-mixer\"]

