# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/go.mod src/go.sum ./
RUN go mod download
COPY src/*.go ./
RUN CGO_ENABLED=0 GOOS=linux go build -o /emoji-mood

FROM alpine:3.18
WORKDIR /app
COPY --from=builder /emoji-mood .
EXPOSE 8080
ENTRYPOINT ["./emoji-mood"]
