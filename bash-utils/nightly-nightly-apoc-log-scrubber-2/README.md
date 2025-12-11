## Apoc Log Scrubber

A whimsical yet practical bash utility designed to help you clean up your log files by intelligently scrubbing sensitive information. In the post-apocalyptic world, keeping your data secure is paramount, even from your own logs!

### Features

*   **Pattern-based scrubbing**: Uses regular expressions to identify and remove common sensitive data like IP addresses, email addresses, and API keys.
*   **Customizable patterns**: Easily extendable to include your own specific sensitive data patterns.
*   **Dry-run mode**: Preview the changes before applying them.
*   **In-place modification**: Option to modify log files directly.

### Usage

```bash
./src/scrub_log.sh [OPTIONS] <log_file>
```

### Options

*   `-d`, `--dry-run`: Perform a dry run, showing what would be scrubbed without modifying the file.
*   `-i`, `--in-place`: Modify the log file in place. Use with caution!
*   `-p <pattern_file>`, `--pattern-file <pattern_file>`: Specify a custom file containing additional regex patterns to scrub.
*   `-h`, `--help`: Display this help message.

### Examples

**Dry run on a log file:**
```bash
./src/scrub_log.sh --dry-run /var/log/apoc_system.log
```

**In-place scrubbing:**
```bash
./src/scrub_log.sh -i /var/log/apoc_system.log
```

**Scrubbing with custom patterns:**
```bash
./src/scrub_log.sh -p custom_patterns.txt /var/log/apoc_system.log
```

### Custom Patterns File Format

The custom patterns file should contain one regular expression per line. Lines starting with `#` are treated as comments.

Example `custom_patterns.txt`:

```
# Custom patterns for Apoc Log Scrubber

# Scrub specific user IDs
USER_ID_[0-9]+

# Scrub internal server names
SERVER-[A-Z]{3}-[0-9]{2}
```

### Testing

This utility includes a set of automated tests. To run them, navigate to the `tests` directory and execute:

```bash
./run_tests.sh
```
