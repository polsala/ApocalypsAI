# nightly-env-var-sanitizer

**Purpose**: Quickly scrub a ```.env``` style file of secrets before you paste it into logs, tickets, or public repositories.

## Features
- Detects common secret key patterns (e.g., ``*_KEY``, ``*_SECRET``, ``PASSWORD``)
- Leaves non‑secret lines untouched
- Works with any line‑ending style (Unix or Windows)
- Outputs to **stdout** by default; optional ``-o`` flag writes to a file

## Installation
```bash
# Clone the repository (or copy the script into your bin)
git clone https://github.com/polsala/ApocalypsAI.git
cp utils/bash-utils/nightly-env-var-sanitizer/src/sanitize_env.sh /usr/local/bin/sanitize_env
chmod +x /usr/local/bin/sanitize_env
```

## Usage
```bash
# Sanitize a file and print to terminal
sanitize_env path/to/.env

# Write sanitized output to a new file
sanitize_env -o sanitized.env path/to/.env
```

## How it works
The script reads each line, checks the variable name against a built‑in list of patterns, and replaces the value with ``***REDACTED***`` when a match is found.

## Testing
Run the bundled test suite with:
```bash
cd utils/bash-utils/nightly-env-var-sanitizer/tests
bash test_sanitize_env.sh
```
All tests should pass.
