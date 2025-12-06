# Temporal Anomaly Tracker

## 🌌 What is it?

The Temporal Anomaly Tracker is a whimsical-yet-useful command-line utility designed to help you detect unexpected changes in your file system. Think of it as a digital guardian for your directories, constantly vigilant against 'temporal anomalies' – files that have been added, removed, or modified since your last baseline scan.

Whether you're safeguarding critical configuration files, monitoring a deployment directory for unauthorized changes, or simply ensuring your project files haven't mysteriously shifted in the night, this tool provides a simple, self-contained way to keep an eye on things.

## ✨ Features

*   **Baseline Generation**: Create a snapshot (baseline) of a directory's file paths, sizes, and modification times.
*   **Anomaly Detection**: Compare the current state of a directory against a previously generated baseline to identify:
    *   **Added files**: New files that weren't in the baseline.
    *   **Removed files**: Files present in the baseline but now missing.
    *   **Modified files**: Files whose size or modification timestamp has changed.
*   **Self-contained**: Written in Python, with minimal dependencies, making it easy to run anywhere.

## 🚀 Installation

This utility is self-contained. Simply place the `temporal-anomaly-tracker` folder within your `utils/` directory. No special installation steps are required beyond having Python 3.6+ installed.

## 🛠️ Usage

The `tracker.py` script accepts two main actions: `baseline` and `check`.

### 1. Generate a Baseline

To create a new baseline for a directory, use the `baseline` action:

```bash
python3 utils/temporal-anomaly-tracker/src/tracker.py baseline /path/to/your/directory --output my_project_baseline.json
```

*   `/path/to/your/directory`: The directory you want to monitor.
*   `--output` (or `-o`): The name of the JSON file where the baseline will be saved. Defaults to `anomaly_baseline.json`.

### 2. Check for Anomalies

To compare the current state of a directory against an existing baseline, use the `check` action:

```bash
python3 utils/temporal-anomaly-tracker/src/tracker.py check /path/to/your/directory --output my_project_baseline.json
```

*   `/path/to/your/directory`: The directory to check for changes.
*   `--output` (or `-o`): The path to the baseline JSON file to compare against. Defaults to `anomaly_baseline.json`.

## 💡 Example Workflow

1.  **Initial Baseline**: After setting up your project or system, create a baseline:
    ```bash
    python3 utils/temporal-anomaly-tracker/src/tracker.py baseline ./my_critical_app -o my_app_v1.json
    ```

2.  **Scheduled Checks**: Run the `check` command periodically (e.g., via a cron job or GitHub Action) to detect any unexpected changes:
    ```bash
    python3 utils/temporal-anomaly-tracker/src/tracker.py check ./my_critical_app -o my_app_v1.json
    ```
    If anomalies are found, the script will print a detailed report to the console.

3.  **Update Baseline**: If legitimate changes occur and you want to accept them, simply generate a new baseline:
    ```bash
    python3 utils/temporal-anomaly-tracker/src/tracker.py baseline ./my_critical_app -o my_app_v1.json
    ```

## 🧪 Tests

To run the automated tests for this utility, navigate to the `utils/temporal-anomaly-tracker` directory and execute:

```bash
python3 -m unittest tests/test_tracker.py
```

The tests use `unittest.mock` to simulate file system operations, ensuring they are deterministic and do not interact with your actual file system.
