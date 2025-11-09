# Temporal Echo Chamber

## 🕰️ Bury Your Thoughts, Retrieve Your Past 🕰️

The Temporal Echo Chamber is a whimsical yet powerful utility designed to help you preserve the context of your work, document crucial decisions, or simply leave a future note for yourself. It allows you to create timestamped, self-contained archives (we call them "echoes") of files or entire directories. Think of it as a digital time capsule for your code and thoughts.

### Why use it?

*   **Context Preservation**: Archive the state of a file or directory at a critical decision point.
*   **Future Self-Reminders**: Leave notes or code snippets for your future self to discover.
*   **Whimsical Documentation**: Add a touch of magic to your project's history.
*   **Lightweight Snapshots**: A simple way to take point-in-time backups without full version control overhead for specific items.

### Usage

The `echo_chamber.py` script provides commands to create, list, and retrieve echoes.

#### Prerequisites

*   Python 3.6+ (standard library only)

#### Commands

1.  **Create an Echo**: Archive a file or directory.
    ```bash
    python src/echo_chamber.py create <path_to_item> [--message "Your message here"] [--output-dir <directory>]
    ```
    *   `<path_to_item>`: The file or directory you want to archive.
    *   `--message`: (Optional) A short message to include inside the echo archive.
    *   `--output-dir`: (Optional) The directory where echoes will be stored. Defaults to `./echoes`.

    _Example:_
    ```bash
    python src/echo_chamber.py create my_important_file.py --message "Refactored the core logic, this is the 'before' state."
    python src/echo_chamber.py create my_feature_branch/ --output-dir project_echoes
    ```

2.  **List Echoes**: See all echoes stored in a directory.
    ```bash
    python src/echo_chamber.py list [--output-dir <directory>]
    ```
    *   `--output-dir`: (Optional) The directory to list echoes from. Defaults to `./echoes`.

    _Example:_
    ```bash
    python src/echo_chamber.py list
    ```

3.  **Retrieve an Echo**: Extract the contents of a specific echo.
    ```bash
    python src/echo_chamber.py retrieve <echo_archive_path> [--extract-dir <directory>]
    ```
    *   `<echo_archive_path>`: The full path to the `.zip` echo file.
    *   `--extract-dir`: (Optional) The directory where the echo will be extracted. Defaults to a new folder named after the echo in the current directory.

    _Example:_
    ```bash
    python src/echo_chamber.py retrieve echoes/echo-20231027-143000-my_important_file.zip --extract-dir retrieved_states
    ```

### Echo Structure

Each echo is a `.zip` file named `echo-YYYYMMDD-HHMMSS-<original_item_name>.zip`.
Inside, you'll find:
*   The archived file(s) or directory.
*   (If a message was provided) `message.txt` containing your note.

### Development

To run tests:
```bash
python -m unittest tests/test_echo_chamber.py
```
