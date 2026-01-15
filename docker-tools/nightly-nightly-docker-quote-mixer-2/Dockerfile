FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY src/ ./src/
COPY quotes/ ./quotes/
RUN go build -o /quote-mixer ./src/main.go

FROM alpine:3.18
COPY --from=builder /quote-mixer /usr/local/bin/quote-mixer
COPY quotes/ /app/quotes/
WORKDIR /app
ENTRYPOINT ["quote-mixer"]
