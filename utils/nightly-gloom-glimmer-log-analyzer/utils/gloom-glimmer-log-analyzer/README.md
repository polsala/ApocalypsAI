# Gloom-Glimmer Log Analyzer

## Overview

In the desolate landscape of the post-apocalypse, system logs can be a beacon of hope or a harbinger of despair. The **Gloom-Glimmer Log Analyzer** is a whimsical-yet-useful utility designed to help you quickly assess the "mood" of your systems by scanning log files for predefined "gloom" (errors, warnings) and "glimmer" (successes, connections) keywords. It calculates a "Glimmer Ratio" – a simple metric to tell you if things are looking up, or if it's time to prepare for the worst.

Keep your spirits up, even when the logs are grim!

## Features

*   Scans single log files or all `.log` files within a directory.
*   Counts occurrences of "gloom" and "glimmer" keywords.
*   Calculates a "Glimmer Ratio" (Glimmers / Total Relevant Entries).
*   Configurable keywords for custom analysis.

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are needed.

1.  Navigate to the `utils/gloom-glimmer-log-analyzer` directory.
2.  Run directly.

## Usage

```bash
python src/analyzer.py --path <log_file_or_directory>
```

### Examples

**Analyze a single log file:**

```bash
python src/analyzer.py --path my_system.log
```

**Analyze all `.log` files in a directory:**

```bash
python src/analyzer.py --path /var/log/apocalypse_systems/
```

**With custom keywords (comma-separated):**

```bash
python src/analyzer.py --path my_system.log \
    --gloom-keywords "ERROR,FAILURE,CRITICAL" \
    --glimmer-keywords "SUCCESS,CONNECTED,ONLINE"
```

## Output

The analyzer will print a summary report to the console, including:

*   Total files scanned.
*   Total lines processed.
*   Total "Gloom" entries.
*   Total "Glimmer" entries.
*   The calculated "Glimmer Ratio".

A higher Glimmer Ratio indicates a healthier, more hopeful system!
