# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/main.go .
RUN go build -o tips .

FROM alpine:3.18
COPY --from=builder /app/tips /usr/local/bin/tips
ENTRYPOINT ["tips"]
