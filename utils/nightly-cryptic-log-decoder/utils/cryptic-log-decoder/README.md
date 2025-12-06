# Cryptic Log Decoder

## Unveiling the Whispers of the Ancients in Your Logs

Are your logs filled with arcane symbols and technical jargon that only a forgotten deity could decipher? Fear not, mortal! The Cryptic Log Decoder is here to translate the ominous murmurs of your system's inner workings into warnings and insights even a novice can comprehend.

This utility takes your raw, cryptic log messages and rephrases them into more dramatic, human-readable, and sometimes slightly whimsical interpretations, helping you quickly identify the nature and severity of underlying issues.

### Features

*   **Pattern-Based Translation**: Recognizes common error patterns and translates them into evocative warnings.
*   **Severity Indication**: Hints at the urgency of the message through its ancient phrasing.
*   **Whimsical Insights**: Adds a touch of the mystical to mundane system failures.

### Usage

The `decoder.py` script provides a single function, `decode_log`, which takes a log string and returns its ancient interpretation.

#### Example

```python
from src.decoder import decode_log

log_message_1 = "ERROR: Connection refused by remote host 192.168.1.100:8080"
log_message_2 = "WARN: Disk usage on /var/log is at 95%"
log_message_3 = "INFO: User 'admin' logged in from 10.0.0.5"
log_message_4 = "DEBUG: Processing request with ID 12345"
log_message_5 = "CRITICAL: System integrity compromised, core meltdown imminent!"
log_message_6 = "Unknown error code 0xDEADBEEF"

print(f"Original: {log_message_1}\nDecoded: {decode_log(log_message_1)}\n")
print(f"Original: {log_message_2}\nDecoded: {decode_log(log_message_2)}\n")
print(f"Original: {log_message_3}\nDecoded: {decode_log(log_message_3)}\n")
print(f"Original: {log_message_4}\nDecoded: {decode_log(log_message_4)}\n")
print(f"Original: {log_message_5}\nDecoded: {decode_log(log_message_5)}\n")
print(f"Original: {log_message_6}\nDecoded: {decode_log(log_message_6)}\n")
```

### Installation

Simply place the `src/decoder.py` file within your project and import the `decode_log` function. No external dependencies are required.
