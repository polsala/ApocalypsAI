# Nightly Config Drift Detector

## Purpose

In the ever-shifting digital landscape, configuration files can subtly diverge from their intended blueprints, leading to unforeseen anomalies and operational glitches. The `Nightly Config Drift Detector` acts as a vigilant sentinel, comparing your project's vital configuration files (like `.env` or similar key-value pairs) against a designated 'source of truth' template. It identifies missing essential variables and flags unexpected additions, ensuring your project's settings remain aligned with the sacred prophecy.

Prevent silent failures and maintain configuration integrity with this essential nightly check.

## Usage

```bash
python src/drift_detector.py --template <path/to/template.env> --target <path/to/actual.env> [path/to/another/actual.env ...]
```

- `--template`: Path to the reference configuration file (e.g., `.env.example`).
- `--target`: One or more paths to the configuration files you want to check against the template.

### Example

```bash
# Check your local .env against the example template
python src/drift_detector.py --template .env.example --target .env

# Check multiple environment configs
python src/drift_detector.py --template .env.example --target .env.dev .env.prod
```

## Output

The utility will print a clear report for each target file, detailing:

- **Missing Keys**: Variables present in the template but absent in the target file.
- **Extra Keys**: Variables present in the target file but not defined in the template.

If no drift is detected, it will report that the target file is 'aligned with the template'.

## Installation

This utility is self-contained and requires Python 3.6+ (tested with 3.11). No external dependencies are needed beyond the standard library.
