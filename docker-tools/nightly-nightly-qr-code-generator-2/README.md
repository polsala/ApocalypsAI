# QR Code Generator (Docker)

Generate QR code PNGs from any text without installing anything on your host. The tool runs inside a tiny Docker container.

## Build

```sh
docker build -t qr-generator .
```

## Run

```sh
docker run --rm qr-generator "Hello, world!" > hello.png
```

The container prints a base64‑encoded PNG to stdout. Redirect it to a file and decode:

```sh
docker run --rm qr-generator "Hello, world!" | base64 -d > hello.png
```

## How it works

The container runs a small Python script that uses the `qrcode` library to create a PNG image, encodes it in base64, and prints it.

## Testing

Run the unit tests with:

```sh
python -m unittest discover -s tests
```
