# Log Lullaby Summarizer

## 🎶 Soothe Your Logs to Sleep 🎶

The Log Lullaby Summarizer is a whimsical yet practical utility designed to bring peace to your chaotic log files. Instead of sifting through endless lines of noise, let this tool sing your logs a lullaby, summarizing critical errors and warnings into a concise, digestible report. It identifies unique problematic patterns and counts their occurrences, helping you quickly pinpoint the most pressing issues.

## Features

*   **Error & Warning Detection**: Scans for common log levels like `ERROR`, `WARNING`, and `CRITICAL`.
*   **Pattern Summarization**: Groups identical or similar error/warning messages to provide a clean overview.
*   **Frequency Counting**: Shows how many times each unique problematic pattern appeared.
*   **Whimsical Output**: Presents the summary in a soothing, easy-to-read format.

## Usage

To use the Log Lullaby Summarizer, simply run the Python script with the path to your log file:

```bash
python src/lullaby_summarizer.py <path_to_your_log_file>
```

### Example

Given a `my_application.log` file like this:

```
2023-10-27 10:00:01 INFO Starting application...
2023-10-27 10:00:05 WARNING Deprecated feature 'X' used in module 'Y'.
2023-10-27 10:00:10 ERROR Failed to connect to database 'mydb'. Retrying...
2023-10-27 10:00:11 INFO User 'admin' logged in.
2023-10-27 10:00:15 ERROR Failed to connect to database 'mydb'. Retrying...
2023-10-27 10:00:20 CRITICAL Out of memory error in process 'Z'.
2023-10-27 10:00:25 WARNING Deprecated feature 'X' used in module 'Y'.
2023-10-27 10:00:30 INFO Processing complete.
```

Running `python src/lullaby_summarizer.py my_application.log` would produce a summary similar to:

```
🎶 Log Lullaby Summary 🎶
--------------------------

After a thorough scan, here are the unique patterns that might need your attention:

[ERROR] Failed to connect to database 'mydb'. Retrying... (2 times)
[WARNING] Deprecated feature 'X' used in module 'Y'. (2 times)
[CRITICAL] Out of memory error in process 'Z'. (1 time)

All other logs seem to be resting peacefully. Sweet dreams!
```
