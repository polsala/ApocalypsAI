# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/ ./
RUN go build -o quote-server .

FROM alpine:3.19
WORKDIR /app
COPY --from=builder /app/quote-server .
EXPOSE 8080
ENTRYPOINT ["./quote-server"]
