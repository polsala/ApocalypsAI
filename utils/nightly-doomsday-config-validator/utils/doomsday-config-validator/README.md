# Doomsday Config Validator

## Overview

The 'Doomsday Config Validator' is a whimsical yet crucial utility designed to prevent accidental apocalypses by meticulously checking your critical JSON configuration files. Think of it as a pre-flight checklist for your most sensitive systems, ensuring that no misplaced comma or incorrect value leads to unforeseen global consequences.

It's built to be self-contained and easy to integrate into any pre-deployment or CI/CD pipeline.

## Features

*   **JSON Syntax Validation**: Ensures your config is valid JSON.
*   **Critical Key Presence**: Verifies that essential configuration keys are not missing.
*   **Data Type Enforcement**: Checks if values for critical keys are of the expected type (e.g., string, integer, list).
*   **Value Constraints**: Validates specific ranges or allowed values for sensitive parameters.

## Installation

This utility is self-contained. Simply place the `doomsday-config-validator` folder within your `utils/` directory.

## Usage

To validate a configuration file, run the `validator.py` script with the path to your JSON file:

```bash
python3 utils/doomsday-config-validator/src/validator.py --config-path /path/to/your/doomsday_device.json
```

If the configuration is valid, the script will exit silently (or print a success message). If errors are found, it will print a list of detected issues and exit with a non-zero status code.

### Example Valid Configuration (`doomsday_device.json`)

```json
{
  "device_name": "Omega Protocol Initiator",
  "activation_sequence": [1, 3, 5, 7, 9],
  "target_coordinates": [40.7128, -74.0060],
  "safety_override_code": "ALPHA-OMEGA-7",
  "power_level": 9000,
  "status": "standby"
}
```

## Validation Rules

The validator checks for the following:

*   `device_name`: Must be a non-empty string.
*   `activation_sequence`: Must be a list of at least 3 integers.
*   `target_coordinates`: Must be a list/tuple of exactly 2 numbers (float or integer).
*   `safety_override_code`: Must be a non-empty string.
*   `power_level`: Must be an integer between 1 and 10000 (inclusive).
*   `status`: Must be one of `"standby"`, `"armed"`, or `"disarmed"`.

## Development & Testing

To run the tests, navigate to the `doomsday-config-validator` directory and execute:

```bash
python3 -m unittest tests/test_validator.py
```
