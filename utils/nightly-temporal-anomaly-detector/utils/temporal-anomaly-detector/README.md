# Temporal Anomaly Detector

## Unearthing Chronological Oddities in Your Filesystem

Welcome, fellow temporal cartographer! The ApocalypsAI Nightly Integrator proudly presents the `temporal-anomaly-detector`, a whimsical yet surprisingly practical utility designed to scan your filesystem for files whose modification timestamps defy the natural flow of time. Are some files from the future? Are others so ancient they predate your current project by eons? This tool will help you find them!

### Why would I need this?

*   **Future Files**: Often indicate build system misconfigurations, clock sync issues, or files copied from a system with a different timezone/time setting. These can cause build tools to skip recompilation or behave unexpectedly.
*   **Ancient Files**: Can highlight forgotten dependencies, unmaintained code, or artifacts that should have been cleaned up long ago. Useful for project hygiene and identifying potential technical debt.

### Features

*   Scans a specified directory recursively.
*   Identifies files with modification times in the future.
*   Identifies files with modification times older than a configurable threshold.
*   Provides clear output detailing detected anomalies.

### Installation

This utility is self-contained and written in Python 3.11. No special installation steps are required beyond having a compatible Python interpreter.

### Usage

Navigate to the `utils/temporal-anomaly-detector/src` directory and run the `detector.py` script.

```bash
python3 detector.py --path <directory_to_scan> [--ancient-threshold <years>]
```

*   `--path <directory_to_scan>`: The root directory to start scanning from. (Required)
*   `--ancient-threshold <years>`: Files older than this many years will be flagged as 'Ancient Anomalies'. Defaults to `5` years.

#### Examples

Scan the current directory for anomalies, flagging files older than 3 years:

```bash
python3 detector.py --path . --ancient-threshold 3
```

Scan your project's `build` directory, using the default 5-year ancient threshold:

```bash
python3 detector.py --path ./build
```

### Example Output

```
Scanning directory: /home/user/my_project

--- Temporal Anomaly Report ---

Future Anomalies:
  - /home/user/my_project/src/future_bug.py (Modified: 2024-11-01 09:00:00, Current: 2024-10-27 10:00:00)

Ancient Anomalies (threshold: 5 years):
  - /home/user/my_project/old_docs/legacy_spec.txt (Modified: 2018-01-01 00:00:00, Current: 2024-10-27 10:00:00)

No anomalies detected for: /home/user/my_project/src/main.py
No anomalies detected for: /home/user/my_project/data/config.json

--- Scan Complete ---
```

May your timestamps ever be in order, and your future remain unwritten by errant files!
