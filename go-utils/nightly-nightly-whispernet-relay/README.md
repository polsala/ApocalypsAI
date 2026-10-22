# nightly-whispernet-relay

A lightweight, concurrent Go service designed to facilitate secure, ephemeral message relay between two parties. Think of it as a digital "dead drop" for sensitive whispers that vanish after being read or after a short time.

## Features

*   **Ephemeral Messages**: Whispers are deleted immediately after being retrieved by a client.
*   **Time-to-Live (TTL)**: Whispers automatically expire after a configurable duration if not retrieved.
*   **Channel-based Relay**: Messages are posted to and retrieved from unique, user-defined channel IDs.
*   **Content Agnostic**: The relay service does not inspect or store message content in plaintext; clients are responsible for encryption.
*   **Concurrent**: Built with Go's concurrency primitives for efficient handling of multiple requests.

## How it works

1.  **Sender**: Encrypts a message (e.g., using AES-GCM with a shared secret key) and `POST`s it to `/whisper/{channel_id}`.
2.  **Receiver**: `GET`s the message from the same `/whisper/{channel_id}`.
3.  **Deletion**: Upon successful `GET`, the whisper is immediately removed from the relay.
4.  **Expiration**: If a whisper is not retrieved within its TTL, it is automatically purged.

## Usage

### Running the Server

```bash
# Build the executable
go build -o whispernet-relay src/main.go

# Run the server (default port 8080, default TTL 5 minutes)
./whispernet-relay

# Or specify port and TTL
./whispernet-relay -port 8081 -ttl 10m # 10 minutes
```

### API Endpoints

*   **POST /whisper/{channel_id}**
    *   **Description**: Posts a new whisper to the specified channel.
    *   **Method**: `POST`
    *   **URL Path**: `/whisper/{channel_id}` (e.g., `/whisper/my-secret-channel-123`)
    *   **Headers**: `Content-Type: application/octet-stream` (or `text/plain` if preferred)
    *   **Body**: The raw (preferably encrypted) message content.
    *   **Response**: `201 Created` on success. `409 Conflict` if a whisper already exists for that channel.

*   **GET /whisper/{channel_id}**
    *   **Description**: Retrieves and immediately deletes a whisper from the specified channel.
    *   **Method**: `GET`
    *   **URL Path**: `/whisper/{channel_id}`
    *   **Response**: `200 OK` with the whisper content in the body on success. `404 Not Found` if no whisper exists or it has expired.

### Example (using `curl`)

**1. Sender posts a whisper (encrypted content is just illustrative here):**

```bash
# Assuming 'my-secret-key' is used for encryption client-side
ENCRYPTED_MESSAGE="<base64_encoded_encrypted_data>"
curl -X POST -H "Content-Type: application/octet-stream" \
     --data "$ENCRYPTED_MESSAGE" \
     http://localhost:8080/whisper/project-alpha-creds
```

**2. Receiver retrieves the whisper:**

```bash
curl -X GET http://localhost:8080/whisper/project-alpha-creds
# Output: <base64_encoded_encrypted_data>
# The whisper is now deleted from the relay.
```

**3. Attempting to retrieve again (will fail):**

```bash
curl -X GET http://localhost:8080/whisper/project-alpha-creds
# Output: 404 Not Found
```

## Development

### Prerequisites

*   Go 1.16+

### Build

```bash
go build -o whispernet-relay src/main.go
```

### Run Tests

```bash
go test ./tests/...
```
