FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/. ./
RUN go build -ldflags "-s -w" -o /cryptic-quote .

FROM alpine:3.19
COPY --from=builder /cryptic-quote /cryptic-quote
ENTRYPOINT ["/cryptic-quote"]
