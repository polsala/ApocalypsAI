FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/go.mod src/go.sum ./
RUN go mod download
COPY src/*.go ./
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o tipserver main.go

FROM alpine:3.19
WORKDIR /app
COPY --from=builder /app/tipserver .
EXPOSE 8080
ENTRYPOINT ["./tipserver"]
