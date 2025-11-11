# Doomsday Config Validator

## Overview
In the precarious world of ApocalypsAI, even a single misplaced comma in a configuration file can trigger a cascade of unforeseen 'doomsday' scenarios. The `doomsday-config-validator` is your first line of defense, a whimsical yet critical utility designed to meticulously check your YAML and JSON configuration files for syntax errors and basic structural integrity.

Ensure your 'Doomsday Device' (or any critical system) is configured flawlessly before deployment!

## Features
- Validates YAML files for syntax errors.
- Validates JSON files for syntax errors.
- Provides clear error messages for easy debugging.

## Installation
This utility is self-contained and requires Python 3.6+.

It depends on the `PyYAML` library for YAML parsing. Install it using pip:

```bash
cd utils/doomsday-config-validator
pip install pyyaml
```

## Usage
Run the validator from the command line, providing the path to your configuration file:

```bash
python src/validator.py <path_to_config_file>
```

### Examples

**Valid YAML:**
```yaml
# config.yaml
server:
  port: 8080
  host: 127.0.0.1
database:
  type: postgres
  credentials:
    user: admin
    password: secure_password
```

```bash
python src/validator.py config.yaml
# Output: config.yaml: OK - Syntax is pristine. The apocalypse can wait.
```

**Invalid JSON:**
```json
// bad_config.json
{
  "api_key": "super_secret",
  "endpoints": [
    {
      "name": "users",
      "url": "/api/v1/users"
    }
    // Missing comma here!
    {
      "name": "products",
      "url": "/api/v1/products"
    }
  ]
}
```

```bash
python src/validator.py bad_config.json
# Output: bad_config.json: ERROR - JSON syntax error: Expecting ',' delimiter: line 9 column 5 (char 145). Doomsday averted (for now).
```

## Development

### Running Tests
```bash
cd utils/doomsday-config-validator
pip install pyyaml # Ensure dependencies are met for tests
python -m unittest discover tests
```
