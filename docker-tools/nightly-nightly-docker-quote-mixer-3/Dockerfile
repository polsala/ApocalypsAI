FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/ .
RUN go build -o quote-mixer .

FROM alpine:3.18
WORKDIR /app
COPY --from=builder /app/quote-mixer .
EXPOSE 8080
ENTRYPOINT ["./quote-mixer"]
