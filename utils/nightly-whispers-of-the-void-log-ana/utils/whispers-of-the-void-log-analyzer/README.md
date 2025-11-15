# Whispers of the Void Log Analyzer

## 🌌 Uncover Hidden Omens in Your Logs 🌌

The ApocalypsAI Nightly Integrator presents a whimsical-yet-useful utility designed to help you detect subtle, recurring patterns or unusual events in your log files that might indicate impending system instability or hidden issues. We call these "whispers of the void" – the faint, often overlooked signals that precede a major system meltdown.

Don't wait for the apocalypse; listen to the whispers!

## ✨ Features

*   **Pattern-Based Detection**: Scans log files for predefined or custom regular expression patterns.
*   **Anomaly Thresholding**: Identifies patterns that occur above a specified frequency, highlighting potential "whispers."
*   **Customizable**: Use default patterns for common errors/warnings or provide your own specific regexes.
*   **Simple CLI**: Easy to integrate into your existing monitoring scripts or run ad-hoc.
*   **Self-Contained**: A single Python script with no external dependencies beyond the standard library.

## 🚀 How to Use

### Prerequisites

*   Python 3.6+ (tested with 3.11)

### Installation

This utility is self-contained. Simply navigate to its directory:

```bash
cd utils/whispers-of-the-void-log-analyzer/
```

### Running the Analyzer

You can run the analyzer directly from the command line:

```bash
python src/analyzer.py <path_to_your_log_file> [options]
```

**Example 1: Analyze a log file with default patterns**

```bash
python src/analyzer.py /var/log/syslog
```

**Example 2: Analyze with a higher anomaly threshold**

This will only report patterns that appear 5 or more times.

```bash
python src/analyzer.py /var/log/nginx/access.log --threshold 5
```

**Example 3: Analyze with custom patterns**

This will override the default patterns and only look for "database connection failed" or "out of memory" messages.

```bash
python src/analyzer.py /var/log/app.log --patterns "database connection failed" "out of memory"
```

### Command-line Arguments

*   `<log_file>` (required): Path to the log file you want to analyze.
*   `--threshold <int>` (optional): The minimum number of occurrences for a pattern to be considered an "anomaly" (default: `3`).
*   `--patterns <pattern1> <pattern2> ...` (optional): Space-separated list of custom regex patterns to search for. If provided, these will override the default patterns.

## 📊 Example Output

```
--- Analysis of '/var/log/app.log' ---
Status: Anomalies Detected
Summary: Detected 2 potential 'whispers of the void' in 1245 lines.

Detected Whispers (Pattern: Count):
- 'error': 15
- 'timeout': 7
-----------------------------------
```

```
--- Analysis of '/var/log/clean.log' ---
Status: Clean
Summary: No significant 'whispers of the void' detected above threshold in 500 lines.
-----------------------------------
```

```
--- Analysis of '/var/log/empty.log' ---
Status: Empty Log
Summary: The log file is empty. No whispers detected.
-----------------------------------
```

## 🧪 Testing

To run the automated tests for this utility:

```bash
cd utils/whispers-of-the-void-log-analyzer/
python -m unittest tests/test_analyzer.py
```

All tests are self-contained and use mocks to ensure determinism and offline execution.
