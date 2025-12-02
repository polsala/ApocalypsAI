# Nightly Chaos Calibrator Config Checker

## Overview
In the chaotic aftermath, ensuring your systems are perfectly calibrated is paramount. The `Nightly Chaos Calibrator Config Checker` is a whimsical-yet-critical utility designed to validate your configuration files (YAML or JSON) against a set of predefined rules. It helps you catch common misconfigurations before they lead to catastrophic system failures or unexpected 'temporal tears'.

This tool checks for:
- **Missing Required Keys**: Ensures all essential configuration parameters are present.
- **Incorrect Data Types**: Verifies that values match their expected types (e.g., integer, boolean, string).
- **Invalid Values**: Checks if values fall within specified ranges or are part of an allowed enumeration list.

Keep your doomsday devices, automated defenses, and resource allocators running smoothly with perfectly calibrated configs!

## Usage

1.  **Navigate to the utility directory**:
    ```bash
    cd utils/nightly-chaos-calibrator-config-checker
    ```

2.  **Run the checker**:
    ```bash
    python3 src/config_checker.py <path_to_your_config_file> [--rules-file <path_to_your_rules_file>]
    ```

    -   `<path_to_your_config_file>`: The YAML or JSON configuration file you want to validate.
    -   `--rules-file <path_to_your_rules_file>`: (Optional) A YAML or JSON file containing the validation rules. If omitted, only basic file parsing will be checked.

### Example

Let's say you have a configuration file `my_apocalypse_device.yaml`:

```yaml
# my_apocalypse_device.yaml
system:
  name: "Omega Protocol"
  version: 1.0
  status: "active"
settings:
  enabled: true
  power_level: 75
  mode: "production"
```

And a rules file `apocalypse_rules.yaml`:

```yaml
# apocalypse_rules.yaml
required_keys:
  system:
    name: {}
    version: {}
    status: {}
  settings:
    enabled: {}
    power_level: {}
    mode: {}
type_rules:
  system:
    name: string
    version: integer
    status: string
  settings:
    enabled: boolean
    power_level: integer
    mode: string
value_rules:
  system:
    version:
      min: 1
      max: 5
    status:
      enum: ["active", "standby", "offline"]
  settings:
    power_level:
      min: 0
      max: 100
    mode:
      enum: ["production", "staging", "development"]
```

To validate `my_apocalypse_device.yaml` against `apocalypse_rules.yaml`:

```bash
python3 src/config_checker.py my_apocalypse_device.yaml --rules-file apocalypse_rules.yaml
```

If everything is correct, you'll see:
`Configuration for my_apocalypse_device.yaml is perfectly calibrated. All systems nominal!`

If there are errors (e.g., `power_level` is 150, or `mode` is `"debug"`), it will report them:

```
Configuration check failed for my_apocalypse_device.yaml:
- Value for 'settings.power_level' is too high: 150 (max: 100)
- Invalid value for 'settings.mode': 'debug' not in allowed list ['production', 'staging', 'development']
```

## Development

### Dependencies
- `PyYAML` (for YAML parsing)

### Running Tests

```bash
python3 -m unittest tests/test_config_checker.py
```
