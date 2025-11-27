# Gloom-Glimmer Log Analyzer

A whimsical-yet-useful utility for scanning log files to identify both "gloom" (errors, warnings) and "glimmer" (successes, healthy states), providing a balanced report on your system's "vibe" in a post-apocalyptic world.

## Purpose

In the chaotic aftermath, understanding the state of your systems is paramount. The Gloom-Glimmer Log Analyzer helps you quickly assess the health of your applications and infrastructure by highlighting critical issues while also celebrating moments of success and stability. It's not just about finding problems; it's about finding hope in the logs!

## Features

*   **Dual-Spectrum Analysis**: Scans for both negative (gloom) and positive (glimmer) keywords.
*   **File & Directory Support**: Analyze individual log files or entire directories recursively.
*   **Customizable Keywords**: Define your own gloom and glimmer terms to suit specific log formats.
*   **Summary Report**: Provides overall counts and a "System Vibe" assessment.
*   **Line-Level Detail**: Option to display the exact lines where keywords were found.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are strictly required beyond the standard library.

1.  Navigate to the `utils/gloom-glimmer-log-analyzer` directory.
2.  Run directly using `python3 src/analyzer.py`.

## Usage

```bash
python3 src/analyzer.py <path_to_log_file_or_directory> [path2 ...] [--gloom-keywords KEYWORD [KEYWORD ...]] [--glimmer-keywords KEYWORD [KEYWORD ...]] [--show-lines]
```

### Arguments:

*   `<path_to_log_file_or_directory>`: One or more paths to log files or directories containing log files.
*   `--gloom-keywords KEYWORD [KEYWORD ...]`: Custom keywords to identify "gloom" events. Overrides default gloom keywords.
*   `--glimmer-keywords KEYWORD [KEYWORD ...]`: Custom keywords to identify "glimmer" events. Overrides default glimmer keywords.
*   `--show-lines`: Display the specific lines where gloom or glimmer keywords were found.

### Examples:

1.  **Analyze a single log file with default keywords:**
    ```bash
    python3 src/analyzer.py /var/log/syslog
    ```

2.  **Analyze a directory of logs and show specific lines:**
    ```bash
    python3 src/analyzer.py /app/logs --show-lines
    ```

3.  **Analyze with custom keywords:**
    ```bash
    python3 src/analyzer.py my_app.log --gloom-keywords "CRITICAL" "FAILURE" --glimmer-keywords "INIT_COMPLETE" "HEALTH_CHECK_OK"
    ```

4.  **Analyze multiple paths:**
    ```bash
    python3 src/analyzer.py /var/log/auth.log /var/log/kern.log /var/log/nginx/error.log
    ```

## Example Output

```
--- Gloom-Glimmer Log Analysis Report ---
-----------------------------------------

File: /var/log/syslog
  Gloom Count: 5
  Glimmer Count: 2
  Gloom Lines:
    Line 10: ERROR: Failed to connect to database.
    Line 25: WARNING: Disk space low.
    Line 50: CRITICAL: Service 'web' stopped unexpectedly.
  Glimmer Lines:
    Line 15: INFO: Database connection established.
    Line 30: INFO: System health check passed.

File: /app/logs/worker.log
  Gloom Count: 1
  Glimmer Count: 3
  Gloom Lines:
    Line 120: EXCEPTION: Worker process crashed.
  Glimmer Lines:
    Line 10: Worker started successfully.
    Line 50: Task 'process_data' completed.
    Line 100: All workers are healthy.

--- Overall System Vibe ---
Total Gloom Events: 6
Total Glimmer Events: 5
Balanced: Gloom and glimmer are in equilibrium. A stable state.
-----------------------------------------
```
