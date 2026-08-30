# nightly-digital-bottle-message

A whimsical-yet-useful CLI tool for the ApocalypsAI community to "bottle" and "uncork" digital messages. Preserve your thoughts, notes, or important data snippets in a uniquely identifiable and timestamped "digital bottle" for future retrieval. Think of it as sending a message across the digital wasteland, hoping it reaches its destination (or your future self!).

## Features

*   **Bottle Messages**: Encodes any text message into a Base64 string, assigns a unique ID, records a timestamp, and saves it as a JSON file.
*   **Uncork Messages**: Decodes and displays the original message from a specified bottle ID or file path.
*   **Self-Contained**: All bottles are stored locally in a `bottles/` directory relative to where the command is run.

## Installation

1.  **Ensure Node.js is installed**: This utility requires Node.js (v14 or higher recommended).
    You can download it from [nodejs.org](https://nodejs.org/).

2.  **Clone the repository (or copy the utility folder)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-digital-bottle-message
    ```

3.  **Install dependencies**:
    ```bash
    npm install
    ```

4.  **Make the CLI tool executable (optional, for global access)**:
    You can link it globally for easier access from any directory:
    ```bash
    npm link
    ```
    Now you can run `bottle-message` from anywhere. If you don't `npm link`, you'll need to run it via `node src/index.js bottle ...` or `npx bottle-message bottle ...` from within the utility's directory.

## Usage

### 1. Bottle a Message

To bottle a message, use the `bottle` command followed by your message. Wrap your message in quotes if it contains spaces.

```bash
bottle-message bottle "Remember to check the temporal anomaly detector daily."
# Output:
# Message bottled! ID: <unique-id>
# File: /path/to/your/bottles/bottle-<unique-id>.json
```

This will create a new JSON file in the `bottles/` directory (e.g., `bottles/bottle-a1b2c3d4-e5f6-7890-1234-567890abcdef.json`) containing the encoded message and metadata.

### 2. Uncork a Message

To retrieve a message, use the `uncork` command with either the bottle's unique ID or its full file path.

**Using the Bottle ID:**

```bash
bottle-message uncork <unique-id>
# Example:
# bottle-message uncork a1b2c3d4-e5f6-7890-1234-567890abcdef
# Output:
# --- Uncorked Message ---
# ID: a1b2c3d4-e5f6-7890-1234-567890abcdef
# Timestamp: 2023-10-27T10:00:00.000Z
# Original Length: 50
# Encoding: base64
# ------------------------
# Remember to check the temporal anomaly detector daily.
# ------------------------
```

**Using the Full File Path:**

```bash
bottle-message uncork ./bottles/bottle-a1b2c3d4-e5f6-7890-1234-567890abcdef.json
# (Output will be the same as above)
```

## Development & Testing

To run the automated tests:

```bash
npm test
```

Tests are deterministic and use mocks for file system operations and UUID generation to ensure reliability and prevent side effects.

## License

This project is licensed under the MIT License.
