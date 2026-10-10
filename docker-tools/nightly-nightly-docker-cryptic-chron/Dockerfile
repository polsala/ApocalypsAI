# Build stage
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/main.go .
RUN go build -o chronicle .

# Runtime stage
FROM alpine:3.18
WORKDIR /app
COPY --from=builder /app/chronicle /usr/local/bin/chronicle
EXPOSE 8080
ENTRYPOINT ["chronicle"]
