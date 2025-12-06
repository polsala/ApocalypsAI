# Gloom-Glimmer Log Analyzer

## Overview
In the post-apocalyptic digital landscape, understanding the health of your systems is paramount. The Gloom-Glimmer Log Analyzer is a whimsical-yet-useful utility designed to scan your log files, identify potential issues (warnings, errors, critical failures), and distill the system's overall 'mood' into a single, easy-to-understand 'Gloom-Glimmer Score'. A high score means your system is shining bright; a low score suggests it's feeling a bit gloomy and might need some immediate attention.

## Features
- **Log Level Detection**: Automatically identifies DEBUG, INFO, WARNING, ERROR, and CRITICAL log entries.
- **Issue Summarization**: Provides counts for each log level.
- **Detailed Error Reporting**: Lists specific lines for warnings, errors, and critical messages.
- **Gloom-Glimmer Score**: A proprietary metric (0-100) indicating system health. 100 is pristine, 0 is catastrophic.
- **Whimsical Commentary**: Offers lighthearted advice based on the calculated score.

## How to Use

### Prerequisites
- Python 3.6+

### Running the Analyzer
1. Navigate to the `utils/nightly-gloom-glimmer-log-analyzer` directory.
2. Run the `analyzer.py` script with the path to your log file:

   ```bash
   python src/analyzer.py /path/to/your/logfile.log
   ```

### Example Output
```
--- Gloom-Glimmer Log Analysis Report ---
Total Lines: 100

Log Level Counts:
  INFO: 80
  WARNING: 15
  ERROR: 5

Error/Warning Details:
  WARNING (15 occurrences):
    - 2023-10-27 10:05:12 WARNING Disk space low on /var/log
    - 2023-10-27 10:10:01 WARNING API rate limit approaching
    - ... and 13 more.
  ERROR (5 occurrences):
    - 2023-10-27 10:15:30 ERROR Failed to connect to database
    - 2023-10-27 10:20:05 ERROR NullPointerException in main thread
    - ... and 3 more.

--- Gloom-Glimmer Score: 75.50/100 ---
System is holding steady, but some shadows linger. Keep an eye out!
```

## Gloom-Glimmer Score Explained
The score is calculated based on the presence and severity of non-informational log entries. Warnings, errors, and critical messages contribute 'gloom points' with increasing weight. The final score is 100 minus a percentage of total possible gloom. A higher score indicates fewer issues and a healthier system.

- **80-100**: System is shining bright! Minimal gloom detected.
- **50-79**: System is holding steady, but some shadows linger. Keep an eye out!
- **0-49**: System is feeling a bit gloomy. Time for some serious troubleshooting!

## Development

### Testing
To run the tests, navigate to the utility's root directory and execute:

```bash
python -m unittest tests/test_analyzer.py
```
