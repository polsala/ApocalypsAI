FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/go.mod src/go.sum ./
RUN go mod download
COPY src/*.go ./
RUN go build -o app .

FROM alpine
WORKDIR /app
COPY --from=builder /app/app .
EXPOSE 8080
CMD ["./app"]
