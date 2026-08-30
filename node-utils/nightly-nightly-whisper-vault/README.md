# Nightly Whisper Vault

## Overview

The `nightly-whisper-vault` is a command-line utility designed for the discreet storage and retrieval of ephemeral text snippets. Think of it as a secure, temporary notepad for those fleeting thoughts, sensitive notes, or temporary secrets that you don't want lingering forever. Each "whisper" can optionally be set with a Time-To-Live (TTL), after which it will automatically self-destruct.

It uses AES-256-CBC encryption to protect your whispers, requiring an encryption key to access the vault.

## Features

*   **Add Whispers**: Store new text snippets with an optional expiry time.
*   **List Whispers**: View a summary of all active whispers.
*   **Reveal Whispers**: Decrypt and display the full content of a specific whisper.
*   **Purge Expired**: Manually clean up whispers that have passed their expiry.
*   **Secure**: Whispers are encrypted at rest using AES-256-CBC.

## Installation

1.  **Node.js**: Ensure you have Node.js (v14 or higher) installed.
2.  **Clone**: Clone the `polsala/ApocalypsAI` repository.
3.  **Navigate**: Go to the `node-utils/nightly-whisper-vault` directory.

    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-whisper-vault
    ```

## Usage

All commands require an encryption key, which can be provided via the `WHISPER_KEY` environment variable or the `--key` flag. **It is highly recommended to use an environment variable for security.**

### Environment Variable (Recommended)

```bash
export WHISPER_KEY="YourSuperSecretKey1234567890123456"
node src/cli.js <command> [options]
```

### Command-line Flag (Less Secure for persistent use)

```bash
node src/cli.js <command> --key "YourSuperSecretKey1234567890123456" [options]
```

**Note**: The encryption key must be 32 bytes (256 bits) long. If you provide a shorter or longer key, it will be hashed to 32 bytes using SHA256 for consistency.

### Commands

#### 1. Add a new whisper

```bash
node src/cli.js add "This is a secret message for the future." [--ttl <hours>]
```

*   `--ttl <hours>`: Optional. The number of hours until the whisper expires and is automatically purged. If omitted, the whisper will not expire.

    Example with TTL:
    ```bash
    node src/cli.js add "Remember to check the temporal anomaly detector." --ttl 24
    ```

#### 2. List all active whispers

```bash
node src/cli.js list
```

This will show a summary (ID, creation time, expiry) of all whispers that haven't expired yet.

#### 3. Reveal a specific whisper

```bash
node src/cli.js reveal <whisper_id>
```

Replace `<whisper_id>` with the ID obtained from the `list` command. This will decrypt and display the full content of the whisper.

#### 4. Purge expired whispers

```bash
node src/cli.js purge
```

This command will scan the vault and permanently remove all whispers that have passed their `expiresAt` timestamp.

## Storage Location

Whispers are stored in a JSON file named `.whisper_vault.json`.

By default, this file is created in the directory where `cli.js` is executed. For more permanent storage, you might consider modifying `src/whisperVault.js` to use `os.homedir()` for the vault file path.

## Development & Testing

To run tests:

```bash
node tests/test_whisperVault.js
```
