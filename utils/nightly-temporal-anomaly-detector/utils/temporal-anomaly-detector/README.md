# Temporal Anomaly Detector

## Overview

The Temporal Anomaly Detector is a whimsical-yet-useful utility designed to scan a specified directory for files exhibiting unusual modification timestamps. It helps identify potential issues such as:

*   **Future Timestamps**: Files whose modification date is set in the future, often indicating build system misconfigurations, clock synchronization problems, or corrupted file transfers.
*   **Excessively Old Timestamps**: Files with modification dates far in the past, which might point to forgotten artifacts, incorrect restorations, or system clock resets.

While its name suggests cosmic mischief, its purpose is grounded in practical system hygiene, ensuring your project files reflect a coherent timeline.

## Usage

```bash
python src/detector.py <path_to_directory> [--max-age-years <int>]
```

*   `<path_to_directory>`: The root directory to scan.
*   `--max-age-years`: (Optional) Defines what constitutes an "excessively old" file. Defaults to 10 years.

### Example

```bash
python src/detector.py ./my_project --max-age-years 5
```

This will scan `my_project` and its subdirectories, reporting any files modified in the future or older than 5 years.

## Output

The utility prints a report to standard output, listing detected anomalies with their paths and the nature of the anomaly.

```
Temporal Anomaly Report for: /path/to/my_project

[FUTURE] /path/to/my_project/build/future_artifact.log (Modified: 2025-01-01 10:00:00)
[ANCIENT] /path/to/my_project/old_docs/legacy.txt (Modified: 2005-03-15 14:30:00)

Scan complete. 2 anomalies found.
```

## Development

The detector is written in Python 3.11 and is self-contained. No external dependencies are required beyond the standard library.

## Tests

To run the tests, navigate to the `utils/temporal-anomaly-detector` directory and execute:

```bash
python -m unittest tests/test_detector.py
```
