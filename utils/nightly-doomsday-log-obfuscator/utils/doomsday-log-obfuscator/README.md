# Doomsday Log Obfuscator

## Purpose
When your doomsday device inevitably encounters a minor hiccup (or a catastrophic meltdown), its debug logs can contain sensitive information. The `Doomsday Log Obfuscator` is a whimsical-yet-useful utility designed to sanitize these logs, replacing critical data like IP addresses, secret project names, and sensitive IDs with harmless, non-revealing placeholders. Perfect for sharing logs with junior apprentices or external contractors without revealing the true extent of your apocalyptic plans.

## How to Use
This utility is a Python script that takes an input log file and an output file path. It will read the input, apply a set of predefined obfuscation rules, and write the sanitized content to the output file.

### Prerequisites
* Python 3.6+

### Running the Obfuscator
1.  Navigate to the `src` directory:
    ```bash
    cd utils/doomsday-log-obfuscator/src
    ```
2.  Run the script, providing the input and output file paths:
    ```bash
    python obfuscator.py --input_file /path/to/your/doomsday.log --output_file /path/to/sanitized_doomsday.log
    ```

## Obfuscation Rules
The current version obfuscates the following:
*   **IPv4 Addresses**: Replaced with `[OBFUSCATED_IP]`
*   **Secret Project Names**: Specific keywords like 'Project Chimera', 'Operation Phoenix', 'Project Mjolnir' are replaced with `[CLASSIFIED_PROJECT]`
*   **Sensitive Numeric IDs**: Patterns like 'Agent ID: XXXXX' or 'Target: YYYYY' are replaced with `[REDACTED_ID]`

## Example
**Original Log Snippet:**
```
[2023-10-27 10:00:01] INFO: Initiating Project Chimera from 192.168.1.100
[2023-10-27 10:00:05] ERROR: Failed to contact Agent ID: 54321. Target: 98765. Critical system failure.
[2023-10-27 10:00:10] DEBUG: Operation Phoenix status: nominal.
```

**Obfuscated Log Snippet:**
```
[2023-10-27 10:00:01] INFO: Initiating [CLASSIFIED_PROJECT] from [OBFUSCATED_IP]
[2023-10-27 10:00:05] ERROR: Failed to contact [REDACTED_ID]. [REDACTED_ID]. Critical system failure.
[2023-10-27 10:00:10] DEBUG: [CLASSIFIED_PROJECT] status: nominal.
```
