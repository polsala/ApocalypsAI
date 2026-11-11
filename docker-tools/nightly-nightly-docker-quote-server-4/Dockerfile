# Build stage
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/ ./
RUN go build -o quote-server .

# Run stage
FROM alpine:3.19
WORKDIR /app
COPY --from=builder /app/quote-server .
EXPOSE 8080
ENTRYPOINT ["./quote-server"]
