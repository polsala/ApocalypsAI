# Nightly Cryptic Cipher Station

A containerized web service designed to encode and decode messages using a selection of whimsical, post-apocalyptic ciphers. Perfect for clandestine communications in the wasteland or just for fun!

## Ciphers Available

*   **Whisperwind Shift**: A simple Caesar-like shift cipher, where each letter is shifted by a fixed number of positions. The 'shift' value is determined by the first letter of the message (A=1, B=2, etc., wrapping around).
*   **Void Glyph Scramble**: A basic substitution cipher using a predefined, fixed mapping of common characters to 'void glyphs'.

## How to Build and Run

This utility is provided as a Docker container for easy deployment.

1.  **Build the Docker Image**:

    Navigate to the `nightly-cryptic-cipher-station` directory and run:

    ```bash
    docker build -t cryptic-cipher-station .
    ```

2.  **Run the Docker Container**:

    This will start the web service on port 8000 (mapped to your host's port 8000):

    ```bash
    docker run -p 8000:8000 --name cipher-station-instance cryptic-cipher-station
    ```

    The service will be accessible at `http://localhost:8000`.

## API Endpoints

The service exposes two primary endpoints:

### 1. `/encode` (POST)

Encodes a given message using a specified cipher.

*   **Method**: `POST`
*   **Headers**: `Content-Type: application/json`
*   **Body**: JSON object with `message` (string) and `cipher_type` (string).
    *   `cipher_type` can be `whisperwind` or `void_glyph`.

**Example Request (Whisperwind Shift)**:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"message": "Hello, survivor!", "cipher_type": "whisperwind"}' \
     http://localhost:8000/encode
```

**Example Response**:

```json
{
  "original_message": "Hello, survivor!",
  "cipher_type": "whisperwind",
  "encoded_message": "Ifmmp, tvswjwps!"
}
```

### 2. `/decode` (POST)

Decodes a given message using a specified cipher.

*   **Method**: `POST`
*   **Headers**: `Content-Type: application/json`
*   **Body**: JSON object with `message` (string) and `cipher_type` (string).
    *   `cipher_type` can be `whisperwind` or `void_glyph`.

**Example Request (Whisperwind Shift)**:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"message": "Ifmmp, tvswjwps!", "cipher_type": "whisperwind"}' \
     http://localhost:8000/decode
```

**Example Response**:

```json
{
  "original_message": "Ifmmp, tvswjwps!",
  "cipher_type": "whisperwind",
  "decoded_message": "Hello, survivor!"
}
}
```

## Error Handling

*   Missing `message` or `cipher_type` in request body will result in a `400 Bad Request`.
*   An unknown `cipher_type` will result in a `400 Bad Request`.

## Stopping the Container

```bash
docker stop cipher-station-instance
docker rm cipher-station-instance
```
