# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod .
COPY src/*.go .
RUN go build -o quote-mixer .

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/quote-mixer .
EXPOSE 8080
ENTRYPOINT ["./quote-mixer"]
