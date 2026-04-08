# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/main.go .
RUN go build -o tipserver .

FROM alpine:3.18
COPY --from=builder /app/tipserver /usr/local/bin/tipserver
EXPOSE 8080
ENTRYPOINT ["tipserver"]
