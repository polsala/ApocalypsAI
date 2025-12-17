# nightly-echo-echo

A lightweight concurrent HTTP echo server that returns request details for debugging purposes.

## Usage

```bash
go run src/main.go
```

The server listens on port `8080` by default. You can change the port by setting the `PORT` environment variable.

```bash
PORT=9090 go run src/main.go
```

## Example

```bash
curl -X POST http://localhost:8080/test -d 'hello world' -H 'X-Custom: 123'
```

Response:

```json
{
  "method": "POST",
  "url": "/test",
  "headers": {
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Custom": "123"
  },
  "body": "hello world"
}
```

## Testing

Run the tests with:

```bash
go test ./...
```
