# Nightly Config Sentinel

The ApocalypsAI Nightly Config Sentinel is a vigilant utility designed to scan your `.env` configuration files for common pitfalls that could lead to security vulnerabilities or unexpected behavior in production environments. It's like a tiny, digital watch-dog for your secrets, ensuring they're not accidentally left exposed or misconfigured.

## Features

*   **Debug Mode Detection**: Warns if `DEBUG=True` is found, which is often undesirable in production.
*   **Empty Sensitive Variable Check**: Identifies environment variables that appear to be sensitive (e.g., `API_KEY`, `SECRET_KEY`, `PASSWORD`, `DB_HOST`, `DB_USER`, `DB_PASS`) but have an empty or whitespace-only value, indicating a potential misconfiguration or oversight.

## Usage

1.  **Navigate to the utility directory**:
    ```bash
    cd utils/nightly-config-sentinel/src
    ```
2.  **Run the sentinel against your `.env` file**:
    ```bash
    python sentinel.py --file /path/to/your/.env
    ```
    Replace `/path/to/your/.env` with the actual path to the configuration file you want to check.

## Example Output

```
Checking configuration file: /path/to/your/.env

--- Sentinel Report ---
[WARNING] Found 'DEBUG=True'. This is often unsafe for production environments.
[WARNING] Sensitive variable 'API_KEY' has an empty or whitespace-only value.
[INFO] No critical issues found.
--- End Report ---
```
