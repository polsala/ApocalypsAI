# Nightly Ephemeral Message Board

A simple, local, file-based command-line utility for posting and managing ephemeral messages. Messages can be configured to automatically delete after a certain time-to-live (TTL) or a maximum number of views, making it perfect for temporary announcements or quick notes in a shared, resource-constrained environment.

## Features

*   **Ephemeral Messages**: Set messages to expire after a specified duration or view count.
*   **Local Storage**: All messages are stored in a local JSON file (`data/messages.json`).
*   **CLI Interface**: Easy to use from the command line.
*   **Cross-Platform**: Built with Node.js, runs on any system with Node.js installed.

## Installation

1.  **Ensure Node.js is installed**: You need Node.js (v14 or higher) to run this utility.
    You can download it from [nodejs.org](https://nodejs.org/).

2.  **Clone the repository (or copy the utility)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-ephemeral-msg-board
    ```

3.  **Install dependencies**: `jest` is a dev dependency for testing.
    ```bash
    npm install
    ```

## Usage

Run the utility using `node src/index.js` followed by commands.

### Post a new message

```bash
node src/index.js post "Remember to check the water purifier by sundown." --ttl 60
node src/index.js post "Ration distribution at Sector 7 tomorrow." --max-views 3
node src/index.js post "Urgent: Anomaly detected near old factory." --ttl 10 --max-views 1
```

*   `post <message>`: The message content (wrap in quotes if it contains spaces).
*   `--ttl <minutes>`: (Optional) Time-to-live in minutes. Message expires after this duration.
*   `--max-views <count>`: (Optional) Maximum number of times the message can be viewed before expiring.

### List all active messages

```bash
node src/index.js list
```

This command will display all messages that have not yet expired. Each time a message is listed, its view count is incremented. Expired messages are automatically removed during this operation.

### Manually clean up expired messages

```bash
node src/index.js clean
```

This command will remove any messages that have expired based on their `ttl` or `max-views` settings, without displaying them.

## Development & Testing

To run tests:

```bash
npm test
```

## Project Structure

```
.
├── README.md
├── package.json        # Node.js project manifest
├── src/
│   └── index.js        # Main application logic
└── tests/
    └── index.test.js   # Jest tests
```
