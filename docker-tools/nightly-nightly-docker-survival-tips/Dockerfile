FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/main.go .
RUN go build -o tipgen .

FROM alpine:3.19
COPY --from=builder /app/tipgen /tipgen
ENTRYPOINT ["/tipgen"]
