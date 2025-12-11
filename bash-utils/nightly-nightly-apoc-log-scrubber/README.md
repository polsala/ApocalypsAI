# Apoc-Log-Scrubber

This utility is designed to help you clean up your log files in the post-apocalyptic world. It intelligently removes sensitive information, leaving behind only the essential, non-sensitive data for analysis or archival.

## Features

*   **Pattern-based scrubbing**: Uses regular expressions to identify and remove common sensitive data patterns (e.g., IP addresses, timestamps, specific keywords).
*   **Configurable**: Easily customize the patterns to be scrubbed via a configuration file.
*   **Preserves context**: Aims to keep the surrounding log message intact for better understanding.

## Usage

```bash
./src/main.sh <input_log_file> <output_log_file> [config_file]
```

*   `<input_log_file>`: The path to the log file you want to scrub.
*   `<output_log_file>`: The path where the scrubbed log file will be saved.
*   `[config_file]` (optional): The path to a custom configuration file. If not provided, a default configuration will be used.

## Example

```bash
./src/main.sh /var/log/system.log /var/log/system.scrubbed.log
```

## Configuration File Format

The configuration file is a simple text file where each line represents a regular expression pattern to be scrubbed. Lines starting with `#` are treated as comments.

```
# Default patterns to scrub
^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*\s+INFO\s+User\s+\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+logged in
^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*\s+DEBUG\s+Session ID: [a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}
```

## Testing

To run the tests, navigate to the `tests` directory and execute the `test_main.sh` script.

```bash
cd tests
./test_main.sh
```
