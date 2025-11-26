# Nightly Configuration Harmonizer of Chaotic Settings

## 🌌 Overview

The `nightly-config-harmonizer` is a whimsical yet essential utility designed to combat configuration drift and ensure consistency across your project's various environments. It acts as a digital librarian, comparing your active configuration files against a 'golden' standard, highlighting any discrepancies that might lead to unexpected behavior or apocalyptic outages.

Think of it as a vigilant guardian, ensuring all your settings are aligned, preventing the subtle chaos that can creep into complex systems.

## ✨ Features

*   **Golden Standard Comparison**: Define a single source of truth for your configurations.
*   **Detailed Discrepancy Reporting**: Pinpoint exactly where your target configurations deviate from the golden standard.
*   **Nested Structure Support**: Handles complex YAML structures with ease.
*   **Cross-Environment Consistency**: Ideal for ensuring dev, staging, and production environments share common, critical settings.

## 🚀 Usage

To use the harmonizer, you need a 'golden' configuration file (e.g., `config.golden.yaml`) and one or more 'target' configuration files (e.g., `config.dev.yaml`, `config.prod.yaml`).

```bash
python src/harmonizer.py \
  --golden-config path/to/config.golden.yaml \
  --target-configs path/to/config.dev.yaml path/to/config.prod.yaml
```

### Arguments

*   `--golden-config <path>`: **Required**. Path to the golden standard YAML configuration file.
*   `--target-configs <path> [<path> ...]`: **Required**. One or more paths to the target YAML configuration files to be compared against the golden standard.

### Exit Codes

*   `0`: All target configurations perfectly match the golden standard.
*   `1`: Discrepancies were found in one or more target configurations, or an error occurred (e.g., file not found, invalid YAML).

## 📝 Example Report

If `config.golden.yaml` contains:

```yaml
database:
  host: localhost
  port: 5432
  user: admin
logging:
  level: INFO
```

And `config.dev.yaml` contains:

```yaml
database:
  host: dev-db
  port: 5432
  user: dev_user
logging:
  level: DEBUG
  format: json
```

The harmonizer might output:

```
--- Comparing config.dev.yaml against config.golden.yaml ---

Difference found at 'database.host': Golden='localhost', Target='dev-db'
Difference found at 'database.user': Golden='admin', Target='dev_user'
Difference found at 'logging.level': Golden='INFO', Target='DEBUG'
Extra key in target at 'logging.format': 'json'

--- Comparison complete for config.dev.yaml ---

Found 4 discrepancies in config.dev.yaml.

--- Summary ---
Total discrepancies found across all target configurations: 4.
```
