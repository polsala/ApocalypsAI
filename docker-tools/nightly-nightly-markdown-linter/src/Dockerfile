FROM golang:1.20-alpine AS builder
WORKDIR /app
COPY go.mod .
COPY go.sum .
RUN go mod download
COPY . .
RUN go build -o markdown-linter .

FROM alpine
WORKDIR /app
COPY --from=builder /app/markdown-linter .
ENTRYPOINT ["./markdown-linter"]
