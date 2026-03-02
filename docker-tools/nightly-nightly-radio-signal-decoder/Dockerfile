FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/main.go .
RUN go build -o decoder .

FROM alpine:latest
COPY --from=builder /app/decoder /usr/local/bin/decoder
ENTRYPOINT ["decoder"]
