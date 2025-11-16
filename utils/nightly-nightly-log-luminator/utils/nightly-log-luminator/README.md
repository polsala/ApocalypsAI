# Nightly Log Luminator

## 🔦 Illuminating the Digital Shadows 🔦

The Nightly Log Luminator is your trusty guide through the often-murky depths of system logs. Instead of sifting through endless lines of text, this utility helps you quickly spot critical errors, exceptions, and warnings, providing a concise, illuminated summary report. It's like having a wise old owl perched on your shoulder, pointing out the important bits in the digital wilderness.

### ✨ Features

*   **Pattern-Based Scanning**: Define custom regex patterns to identify specific error types, warnings, or critical events.
*   **Concise Summaries**: Generates a clear report detailing error counts, unique messages, and their occurrences.
*   **Directory & File Support**: Scan individual log files or entire directories for a comprehensive overview.
*   **Offline & Self-Contained**: Runs without external network dependencies, perfect for secure and isolated environments.

### 🚀 Usage

```bash
python src/luminator.py --path /var/log/my_app.log
# Or scan a directory
python src/luminator.py --path /var/log/my_app_logs/ --output-file report.md
```

#### Arguments:

*   `--path <file_or_dir>`: Required. Path to a log file or a directory containing log files.
*   `--output-file <filename>`: Optional. Path to save the summary report. If not provided, prints to stdout.
*   `--patterns <pattern1> <pattern2> ...`: Optional. List of regex patterns to search for. Defaults to common error patterns if not provided.

### 🛠️ Development

The Luminator is written in Python 3.11 and uses standard library modules.

#### Running Tests:

```bash
python -m pytest tests/
```

### 📜 License

This utility is released under the MIT License. See `LICENSE` for more details.
