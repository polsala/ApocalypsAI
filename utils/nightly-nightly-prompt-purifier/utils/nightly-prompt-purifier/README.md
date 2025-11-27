# Nightly Prompt Purifier

## Overview

The ApocalypsAI Nightly Prompt Purifier is a standalone utility designed to scrub sensitive information and unnecessary noise from text files. In a world where every prompt counts, ensuring your data is clean, concise, and free of accidental leaks is paramount. This tool helps you prepare your logs, documents, or any text-based data for safe use with Large Language Models (LLMs) or for public sharing, without revealing secrets.

## Features

-   **Sensitive Data Redaction**: Automatically identifies and redacts common patterns for API keys, email addresses, and IPv4 addresses.
-   **Whitespace Optimization**: Removes excessive blank lines and trims leading/trailing whitespace for cleaner input.
-   **Custom Keyword Replacement**: Allows for user-defined keywords to be replaced with a specified placeholder (e.g., `[REDACTED]`).

## Usage

```bash
python src/purifier.py --input <input_file_path> --output <output_file_path> [--keywords <key1=value1,key2=value2>] [--no-api-keys] [--no-emails] [--no-ips] [--no-whitespace]
```

### Arguments:

-   `--input <path>`: **Required**. Path to the input text file.
-   `--output <path>`: **Required**. Path where the purified output will be saved.
-   `--keywords <key1=value1,key2=value2>`: Optional. Comma-separated list of `original=replacement` pairs for custom redaction. Keywords are case-insensitive.
-   `--no-api-keys`: Optional. Disable API key redaction.
-   `--no-emails`: Optional. Disable email address redaction.
-   `--no-ips`: Optional. Disable IPv4 address redaction.
-   `--no-whitespace`: Optional. Disable whitespace optimization.

## Example

```bash
# Purify a log file, redacting API keys and a custom word, saving to a new file
python src/purifier.py --input my_sensitive_log.txt --output purified_log.txt --keywords "secret_project=PROJECT_X" --no-emails --no-ips

# Purify a document, only removing whitespace
python src/purifier.py --input messy_doc.md --output clean_doc.md --no-api-keys --no-emails --no-ips --keywords ""
```

## Development

To run tests:

```bash
python -m unittest tests/test_purifier.py
```
