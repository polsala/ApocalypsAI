# Nightly Cryptic QR Encoder

A tiny Go command‑line utility that pretends to generate a QR‑code PNG from any input string.  It writes a minimal PNG header followed by the raw text – a placeholder useful for demos, testing pipelines, or just for fun.

## Usage
```bash
# Build and run directly
go run ./src/main.go "Hello, world!" output.png
```

The program expects exactly two arguments:
1. The text to encode (treated as opaque data).
2. The path of the PNG file to create.

On success it prints a short confirmation message and creates `output.png`.

## Why a placeholder?
Generating a real QR code would require an external library.  To keep the utility self‑contained and offline‑friendly, we embed only the PNG signature bytes and append the raw text.  The resulting file is a valid PNG file (it starts with the proper header) and can be opened by image viewers, which will show a tiny corrupted image – perfect for whimsical demos.

## Testing
Run the test suite with:
```bash
go test ./tests/...
```

The test checks that the program creates a file larger than the PNG header.
