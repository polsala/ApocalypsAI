FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/main.go .
RUN go build -o tip-server .

FROM alpine:3.19
COPY --from=builder /app/tip-server /tip-server
EXPOSE 8080
ENTRYPOINT ["/tip-server"]
