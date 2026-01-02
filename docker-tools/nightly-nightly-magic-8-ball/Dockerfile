# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/main.go .
RUN go mod init magic8ball && go mod tidy && go build -o magic8ball

FROM alpine
WORKDIR /app
COPY --from=builder /app/magic8ball .
ENTRYPOINT ["./magic8ball"]
