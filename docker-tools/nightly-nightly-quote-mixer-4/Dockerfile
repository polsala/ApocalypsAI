# Build stage
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/*.go .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o quote-mixer .

# Runtime stage
FROM alpine:3.18
WORKDIR /app
COPY --from=builder /app/quote-mixer .
EXPOSE 8080
ENTRYPOINT ["./quote-mixer"]
