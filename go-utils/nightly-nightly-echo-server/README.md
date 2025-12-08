Nightly Echo Server

A lightweight concurrent HTTP server that echoes back request details.
Useful for debugging HTTP clients and inspecting traffic.

Usage:
  go run src/main.go
  # Server listens on :8080

  curl -X POST http://localhost:8080 -d "hello world"

Response:
  {
    "method":"POST",
    "url":"/",
    "headers":{...},
    "body":"hello world"
  }
