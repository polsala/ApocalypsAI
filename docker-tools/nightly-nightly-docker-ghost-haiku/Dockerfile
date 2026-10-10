# Build stage
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/main.go .
RUN go build -o ghost-haiku .

# Runtime stage
FROM alpine:3.18
COPY --from=builder /app/ghost-haiku /usr/local/bin/ghost-haiku
ENTRYPOINT ["ghost-haiku"]
