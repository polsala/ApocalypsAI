FROM \"golang:1.22-alpine\" AS builder
WORKDIR /app
COPY src/main.go .
RUN go build -o echo .

FROM alpine
WORKDIR /app
COPY --from=builder /app/echo .
EXPOSE 8080
CMD [\"./echo\"]

