# Nightly Configuration Harmonizer of Chaotic Settings

## Overview
The `nightly-config-harmonizer` is a whimsical-yet-useful utility designed to bring order to your configuration files. In the chaotic aftermath, ensuring all systems run with consistent and complete settings is paramount. This tool compares a target configuration file against a 'golden' template, reporting any missing keys, extra keys, or value discrepancies. Optionally, it can apply missing default settings from the template to the target file.

## Features
- **Configuration Validation**: Quickly identify if a configuration file deviates from a desired template.
- **Discrepancy Reporting**: Clearly lists missing keys, extra keys, and value mismatches.
- **Automated Harmonization**: Option to automatically add missing keys with their default values from the template.
- **YAML Support**: Designed for YAML configuration files, a common format for modern applications.

## Usage

```bash
python src/harmonizer.py --template <path_to_template.yaml> --target <path_to_target.yaml> [--apply]
```

### Arguments:
- `--template <path>`: Path to the 'golden' template YAML file.
- `--target <path>`: Path to the target YAML file to be harmonized.
- `--apply`: (Optional) If present, the utility will write changes to the target file, adding missing keys from the template with their default values. If omitted, it will only report discrepancies.

### Example:

Given `template.yaml`:
```yaml
api_key: "default_api_key"
log_level: "INFO"
database:
  host: "localhost"
  port: 5432
  user: "admin"
server:
  port: 8080
  timeout: 30
```

And `target.yaml`:
```yaml
api_key: "my_secret_key"
database:
  host: "db.example.com"
  port: 5432
```

Running `python src/harmonizer.py --template template.yaml --target target.yaml` would report:

```
Discrepancies found in target.yaml:
- Missing key: log_level (default: INFO)
- Missing key: database.user (default: admin)
- Missing key: server.port (default: 8080)
- Missing key: server.timeout (default: 30)
- Value mismatch for api_key: target='my_secret_key', template='default_api_key'
Run with --apply to update the target file with missing defaults.
```

Running `python src/harmonizer.py --template template.yaml --target target.yaml --apply` would update `target.yaml` to:

```yaml
api_key: "my_secret_key"
log_level: "INFO"
database:
  host: "db.example.com"
  port: 5432
  user: "admin"
server:
  port: 8080
  timeout: 30
```
