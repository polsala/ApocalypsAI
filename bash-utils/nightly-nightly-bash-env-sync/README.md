# nightly-bash-env-sync

A whimsical yet useful bash script that synchronizes environment variables from a source file into your current shell session. Think of it as a tiny, personal time-travel device for your shell's memory!

## Purpose

In the chaotic aftermath of system reboots or context switches, your shell's environment variables can get jumbled. This utility helps you quickly restore a known good state by sourcing variables from a designated file.

## Usage

1.  **Create a source file**: This file should contain environment variable assignments, one per line, in the format `KEY=VALUE`.
    Example: `my_vars.env`
    ```bash
    export MY_API_KEY="supersecret123"
    export ANOTHER_VAR="some_value"
    ```

2.  **Run the script**: Execute the script, providing the path to your source file as an argument.
    ```bash
    ./nightly-bash-env-sync/src/sync_env.sh /path/to/your/my_vars.env
    ```

    The script will then export these variables into your current shell session.

## Installation

No installation required. Simply download the `sync_env.sh` script and make it executable:

```bash
chmod +x nightly-bash-env-sync/src/sync_env.sh
```

## Testing

Automated tests are included to ensure the script functions correctly. You can run them using `bash`.

```bash
cd nightly-bash-env-sync/tests
bash test_sync_env.sh
```
