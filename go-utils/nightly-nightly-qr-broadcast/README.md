# QR Broadcast Service

A tiny Go HTTP service that receives a JSON payload with a `message` field and returns a PNG QR code representing that message. Perfect for secret post‑apocalypse communications.

## Build

```sh
go build -o qr-broadcast ./src
```

## Run

```sh
./qr-broadcast
```

The server listens on `localhost:8080`.

## API

`POST /qr`

Payload:

```json
{ "message": "Your secret text" }
```

Response: `image/png` containing the QR code.

## Example

```sh
curl -X POST -d '{"message":"Hello"}' -H "Content-Type: application/json" http://localhost:8080/qr --output hello.png
```
