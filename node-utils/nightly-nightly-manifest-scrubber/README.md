# Nightly Manifest Scrubber

A Node.js CLI tool to clean configuration files by removing comments, empty lines, and optionally redacting sensitive patterns. Ideal for preparing config files for sharing, deployment, or version control by stripping out transient or sensitive information.

## Features

*   **Comment Removal**: Automatically removes lines starting with `#` (for INI/YAML/Shell) or `//` (for JSON/JS-like configs).
*   **Empty Line Removal**: Cleans up whitespace by removing blank lines.
*   **Pattern Redaction**: Redact sensitive information (e.g., API keys, passwords) using regular expressions, replacing them with a configurable placeholder.
*   **Input/Output Flexibility**: Read from a specified file and either print to stdout or write to a new output file.

## Installation

1.  **Prerequisites**: Ensure you have Node.js (v14 or higher) and npm installed.
2.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-manifest-scrubber
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    ```
4.  **Make it executable (optional, for direct use)**:
    ```bash
    chmod +x src/cli.js
    ```
    Or, you can use `npx` or `npm exec` to run it without global installation.

## Usage

```bash
nightly-manifest-scrubber <file> [options]
```

### Arguments

*   `<file>`: Path to the input file you want to scrub.

### Options

*   `-o, --output <file>`: Path to the output file. If not provided, the scrubbed content will be printed to `stdout`.
*   `-c, --no-comments`: Do not remove lines starting with `#` or `//`. By default, comments are removed.
*   `-e, --no-empty-lines`: Do not remove empty lines. By default, empty lines are removed.
*   `-r, --redact <patterns...>`: Space-separated list of regular expression patterns (as strings) to redact. Any text matching these patterns will be replaced.
    *   **Example**: `--redact "API_KEY=.*" "PASSWORD=.*"`
*   `-p, --placeholder <text>`: Custom placeholder text for redacted content. Default is `[REDACTED]`.

### Examples

1.  **Basic scrubbing (remove comments and empty lines) to stdout**:
    ```bash
    nightly-manifest-scrubber my_config.ini
    ```

2.  **Scrubbing and saving to a new file**:
    ```bash
    nightly-manifest-scrubber my_config.ini -o my_config.clean.ini
    ```

3.  **Scrubbing without removing comments**:
    ```bash
    nightly-manifest-scrubber my_config.js -c
    ```

4.  **Redacting sensitive information**:
    ```bash
    nightly-manifest-scrubber .env -o .env.scrubbed --redact "API_KEY=.*" "DB_PASS=.*"
    ```

5.  **Redacting with a custom placeholder**:
    ```bash
    nightly-manifest-scrubber secrets.yml --redact "token: .*" -p "---SECRET---"
    ```

6.  **Combining options**:
    ```bash
    nightly-manifest-scrubber complex_settings.conf -o clean_settings.conf --no-empty-lines --redact "USER_ID=\\d+" -p "[USER_ID_OMITTED]"
    ```
    *Note: When using regex patterns in bash, you might need to escape special characters like `\`.* 

## Development

To run tests:

```bash
npm test
```

## License

This project is licensed under the MIT License.
