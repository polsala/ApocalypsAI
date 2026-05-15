# Nightly Chrono-Courier

A whimsical-yet-useful Go-based time-delayed message relay service. Send messages now, have them delivered later! Perfect for future reminders, simulating asynchronous communications, or sending "post-apocalyptic" messages that arrive when the dust settles.

## Features

*   **Time-Delayed Delivery**: Messages are held and delivered only after a specified delay.
*   **Recipient-Based**: Messages are addressed to specific recipients.
*   **Simple HTTP API**: Easy to integrate with other tools or scripts.
*   **Concurrent**: Built with Go's concurrency features for efficient message processing.

## How to Run

1.  **Prerequisites**: Ensure you have Go (version 1.16 or higher) installed.
2.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/go-utils/nightly-chrono-courier
    ```
3.  **Build the service**:
    ```bash
    go build -o chrono-courier src/main.go
    ```
4.  **Run the service**:
    ```bash
    ./chrono-courier
    ```
    The service will start on `http://localhost:8080`.

## Usage

The Chrono-Courier exposes two main HTTP endpoints:

### 1. Send a Time-Delayed Message (`POST /send`)

Send a message to a recipient with a specified delay in seconds.

**Request:**

```http
POST http://localhost:8080/send
Content-Type: application/json

{
    "recipient": "survivor-alpha",
    "content": "Remember to check the water purifier by next Tuesday!",
    "delay_seconds": 604800
}
```

*   `recipient` (string, required): The identifier for the message recipient.
*   `content` (string, required): The message content.
*   `delay_seconds` (integer, required): The delay in seconds before the message is delivered.

**Response (Status 202 Accepted):**

```json
{
    "id": "msg-1",
    "recipient": "survivor-alpha",
    "content": "Remember to check the water purifier by next Tuesday!",
    "delivery_time": "2024-07-20T10:00:00Z",
    "sent_time": "2024-07-13T10:00:00Z"
}
```

### 2. Receive Delivered Messages (`GET /receive`)

Retrieve all messages that have been delivered for a specific recipient.

**Request:**

```http
GET http://localhost:8080/receive?recipient=survivor-alpha
```

*   `recipient` (string, required): The identifier of the recipient whose messages you want to retrieve.

**Response (Status 200 OK):**

```json
[
    {
        "id": "msg-1",
        "recipient": "survivor-alpha",
        "content": "Remember to check the water purifier by next Tuesday!",
        "delivery_time": "2024-07-20T10:00:00Z",
        "sent_time": "2024-07-13T10:00:00Z"
    },
    {
        "id": "msg-2",
        "recipient": "survivor-alpha",
        "content": "The secret stash is under the old oak tree.",
        "delivery_time": "2024-07-14T12:30:00Z",
        "sent_time": "2024-07-14T12:29:00Z"
    }
]
```
If no messages are delivered for the recipient, an empty JSON array `[]` will be returned.

## Development

### Running Tests

To run the automated tests for the Chrono-Courier:

```bash
go test ./tests/...
```

The tests are designed to be deterministic and do not require an active network connection or external dependencies. They use `httptest` for mocking HTTP requests and manually control time-related aspects to ensure consistent results.
