# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/ .
RUN go build -o quote-mixer .

FROM alpine:3.18
COPY --from=builder /app/quote-mixer /usr/local/bin/quote-mixer
ENTRYPOINT ["quote-mixer"]
