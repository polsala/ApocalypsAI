# Gloom-Glimmer Log Analyzer

The world may be crumbling, but our systems still generate logs! The Gloom-Glimmer Log Analyzer is a vital utility for sifting through the digital detritus of the apocalypse, identifying critical errors (the "Gloom") and unexpected positive signs (the "Glimmers").

This tool helps you quickly get a summary of what's going wrong, what's just a warning, and where a tiny spark of hope might be hiding in your system's output.

## Usage

```bash
python src/analyzer.py <log_file_path> [--config <config_file_path>]
```

### Arguments:

*   `<log_file_path>`: The path to the log file you want to analyze.
*   `--config <config_file_path>`: (Optional) Path to a YAML configuration file. If not provided, a default configuration will be used.

## Configuration

The analyzer uses a YAML configuration file to define the patterns it searches for.
A default configuration is embedded, but you can override it.

**Example `config.yaml`:**

```yaml
patterns:
  gloom:
    - "ERROR"
    - "CRITICAL"
    - "FAILURE"
    - "EXCEPTION"
  warning:
    - "WARNING"
    - "DEPRECATED"
    - "TIMEOUT"
  glimmer:
    - "SUCCESS"
    - "OPTIMIZED"
    - "HEALED"
    - "RECOVERED"
    - "STABLE"
```

Each category (`gloom`, `warning`, `glimmer`) should contain a list of strings. The analyzer will perform case-insensitive substring matching.

## Output

The tool will print a summary report to the console, detailing the count of each pattern found, and listing the lines where "Gloom" or "Glimmer" patterns were detected.

```
--- Gloom-Glimmer Log Analysis Report ---
Log File: /path/to/your/log.log

Gloom (Errors/Critical): 3
  - Line 10: [ERROR] Disk full.
  - Line 25: [CRITICAL] Core meltdown imminent.
  - Line 50: [EXCEPTION] NullPointerException in main loop.

Warning (Warnings/Issues): 2
  - Line 15: [WARNING] Low memory.
  - Line 30: [DEPRECATED] Old API usage detected.

Glimmer (Success/Hope): 1
  - Line 40: [SUCCESS] Data backup complete.

Total Lines Analyzed: 50
--- End Report ---
```
