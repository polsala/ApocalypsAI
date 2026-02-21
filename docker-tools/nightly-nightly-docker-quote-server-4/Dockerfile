# Build stage
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod .
COPY src/*.go .
RUN go build -o quote-server

# Runtime stage
FROM alpine:3.19
WORKDIR /app
COPY --from=builder /app/quote-server .
EXPOSE 8080
CMD ["./quote-server"]
