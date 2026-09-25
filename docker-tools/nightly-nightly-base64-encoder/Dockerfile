# ---- Build stage ----
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod .
COPY src/main.go ./main.go
RUN go build -o encoder main.go

# ---- Runtime stage ----
FROM alpine:3.18
COPY --from=builder /app/encoder /usr/local/bin/encoder
ENTRYPOINT ["encoder"]
