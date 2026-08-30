FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/ .
RUN go build -o server .

FROM alpine
COPY --from=builder /app/server /server
EXPOSE 8080
ENTRYPOINT ["/server"]
