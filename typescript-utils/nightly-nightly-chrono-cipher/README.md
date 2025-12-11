# Nightly Chrono Cipher

A whimsical-yet-useful TypeScript CLI tool that encrypts messages with time-based keys, creating messages that can only be decrypted at specific future timestamps.

## Features

- **Time-Locked Encryption**: Encrypt messages that can only be decrypted at a specific future time
- **Time Window Decryption**: Allow decryption within a specified time window
- **Cross-Platform**: Works on any system with Node.js
- **Zero Dependencies**: Pure TypeScript implementation

## Installation

```bash
npm install -g nightly-chrono-cipher
```

Or use directly with npx:

```bash
npx nightly-chrono-cipher --help
```

## Usage

### Encrypt a message for a specific time

```bash
# Encrypt for decryption at exactly 3:30 PM on December 25, 2024
npx nightly-chrono-cipher encrypt --message "Secret Santa plans" --time "2024-12-25T15:30:00"
```

### Encrypt with a time window

```bash
# Allow decryption between 9 AM and 5 PM on January 1, 2025
npx nightly-chrono-cipher encrypt --message "New Year's resolution" --start "2025-01-01T09:00:00" --end "2025-01-01T17:00:00"
```

### Decrypt a message

```bash
# Try to decrypt (will only work if current time is within the allowed window)
npx nightly-chrono-cipher decrypt --message "encrypted_message_here"
```

### Generate a time capsule

```bash
# Create a message that can only be opened on your birthday next year
npx nightly-chrono-cipher encrypt --message "Reflections from this year" --time "2025-06-15T00:00:00"
```

## Message Format

Encrypted messages are base64-encoded JSON with the following structure:

```json
{
  "version": "1.0",
  "startTime": "2024-12-25T15:30:00.000Z",
  "endTime": "2024-12-25T15:30:00.000Z",
  "encryptedData": "base64_encoded_encrypted_message"
}
```

## Use Cases

- **Time Capsules**: Store messages for future you
- **Event Coordination**: Share secrets that unlock at event start
- **Birthday Surprises**: Schedule reveals for special occasions
- **Project Milestones**: Encrypt release notes until go-live
- **Educational Tools**: Create time-gated learning materials

## Security Notes

- This tool uses time-based keys derived from the target timestamp
- Messages cannot be decrypted before the allowed time window
- Clock synchronization between encryption and decryption is critical
- For production use, consider additional authentication mechanisms

## Examples

```bash
# Secret team announcement
npx nightly-chrono-cipher encrypt \
  --message "We're launching Project Phoenix tomorrow!" \
  --time "2024-12-02T09:00:00"

# Holiday gift clue
npx nightly-chrono-cipher encrypt \
  --message "Check under the Christmas tree" \
  --start "2024-12-25T06:00:00" \
  --end "2024-12-25T12:00:00"

# Personal goal reminder
npx nightly-chrono-cipher encrypt \
  --message "Remember to meditate daily" \
  --time "2025-01-01T08:00:00"
```

## License

MIT
