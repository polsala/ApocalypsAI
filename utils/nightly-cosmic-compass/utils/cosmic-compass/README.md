# Cosmic Compass: Your GitHub Linkifier

Navigate the vast cosmos of your GitHub repository with ease! The Cosmic Compass is a whimsical-yet-useful utility that automatically transforms plain text references to GitHub issues and pull requests into clickable Markdown links. Perfect for enhancing commit messages, PR descriptions, comments, or any documentation.

## Features

*   **Auto-linking**: Converts `#ISSUE_NUMBER` (e.g., `#123`) into `[#123](https://github.com/OWNER/REPO/issues/ISSUE_NUMBER)`.
*   **Cross-repository linking**: Converts `OWNER/REPO#ISSUE_NUMBER` (e.g., `octocat/Spoon-Knife#42`) into `[octocat/Spoon-Knife#42](https://github.com/octocat/Spoon-Knife/issues/42)`.
*   **Flexible input**: Reads from standard input or a specified file.
*   **Configurable default repository**: Specify the current repository for local issue references.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are strictly required beyond standard library modules.

1.  Navigate to the `utils/cosmic-compass` directory.
2.  Ensure you have Python 3.11 or newer installed.

## Usage

```bash
python src/linkifier.py --repo <owner/repo> [OPTIONS]
```

### Arguments

*   `--repo <owner/repo>` (Required): The default GitHub repository (e.g., `polsala/ApocalypsAI`) to use for resolving local issue references (e.g., `#123`). This can also be set via the `GITHUB_REPOSITORY` environment variable.
*   `--file <path>` (Optional): Path to a text file to process. If not provided, the utility reads from standard input.
*   `--output <path>` (Optional): Path to a file where the linked output will be written. If not provided, output goes to standard output.

### Examples

1.  **Process text from standard input:**

    ```bash
    echo "Fixes #123 and addresses polsala/ApocalypsAI#456. Also, check out issue #789." | python src/linkifier.py --repo polsala/ApocalypsAI
    ```

    Output:
    ```
    Fixes [#123](https://github.com/polsala/ApocalypsAI/issues/123) and addresses [polsala/ApocalypsAI#456](https://github.com/polsala/ApocalypsAI/issues/456). Also, check out issue [#789](https://github.com/polsala/ApocalypsAI/issues/789).
    ```

2.  **Process a file and save to another file:**

    ```bash
    # content of my_notes.txt:
    # This is a note about issue #1.
    # We also need to consider other_org/other_repo#2.

    python src/linkifier.py --repo polsala/ApocalypsAI --file my_notes.txt --output linked_notes.txt
    ```

    `linked_notes.txt` will contain:
    ```
    This is a note about issue [#1](https://github.com/polsala/ApocalypsAI/issues/1).
    We also need to consider [other_org/other_repo#2](https://github.com/other_org/other_repo/issues/2).
    ```

3.  **Using `GITHUB_REPOSITORY` environment variable:**

    ```bash
    export GITHUB_REPOSITORY="polsala/ApocalypsAI"
    echo "This fixes #100." | python src/linkifier.py
    ```

    Output:
    ```
    This fixes [#100](https://github.com/polsala/ApocalypsAI/issues/100).
    ```
