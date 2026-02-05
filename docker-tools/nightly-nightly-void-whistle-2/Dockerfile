FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY src/main.go .
RUN go build -o void-whistle main.go

FROM alpine:latest

RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/void-whistle .

ENTRYPOINT ["./void-whistle"]
