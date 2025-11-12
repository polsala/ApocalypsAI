# Doomsday Config Validator

## Purpose
This utility provides a whimsical-yet-useful way to validate hypothetical 'doomsday device' configuration files. It's designed to catch common logical flaws, missing critical parameters, and conflicting settings that might prevent your world-ending (or saving!) contraption from functioning as intended.

## Features
- **Critical Parameter Checks**: Ensures essential settings like `activation_code`, `target_coordinates`, `power_source`, and `countdown_timer_seconds` are present and correctly formatted.
- **Conflict Detection**: Identifies logical inconsistencies, such as a `safety_override` being active while `self_destruct_on_failure` is also enabled.
- **Schema Validation**: Verifies data types and acceptable values for various configuration fields.

## Usage
To validate a configuration file, run the `validator.py` script with the path to your YAML or JSON config:

```bash
python src/validator.py path/to/your_config.yaml
```

If the configuration is valid, it will print a success message. Otherwise, it will list all detected errors.

## Example Valid Configuration (`example_valid.yaml`)
```yaml
activation_code: "OMEGA-PROTOCOL-7"
target_coordinates: [34.0522, -118.2437] # Los Angeles
power_source: fusion
countdown_timer_seconds: 3600 # 1 hour
safety_override: false
self_destruct_on_failure: true
message_on_activation: "The end is nigh!"
```

## Example Invalid Configuration (`example_invalid.yaml`)
```yaml
activation_code: 12345 # Should be a string
target_coordinates: [34.0522] # Missing longitude
power_source: magic # Invalid source
# Missing countdown_timer_seconds
safety_override: true
self_destruct_on_failure: true # Conflict with safety_override
```
