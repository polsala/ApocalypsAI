# syntax=docker/dockerfile:1
FROM golang:1.20-alpine AS builder
WORKDIR /app
COPY go.mod .
COPY go.sum .
RUN go mod download
COPY src/ ./src
RUN go build -o catfacts ./src/main.go

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/catfacts /app/catfacts
ENTRYPOINT ["./catfacts"]
