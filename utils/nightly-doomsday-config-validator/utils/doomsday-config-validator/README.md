# Doomsday Config Validator

Ensuring your critical systems are correctly configured is paramount, especially when the apocalypse looms. The `doomsday-config-validator` is a whimsical yet essential utility designed to scrutinize your YAML and JSON configuration files against a set of predefined structural rules. It helps you catch common misconfigurations before they trigger an unforeseen 'temporal anomaly' or 'catastrophic system cascade'.

## Features

- **YAML & JSON Support**: Validates both common configuration formats.
- **Customizable Schemas**: Define your expected structure, required keys, and basic type checks.
- **Themed Error Messages**: Get clear, apocalypse-themed feedback on what went wrong.
- **Self-Contained**: No external dependencies beyond standard Python libraries and `PyYAML` (which is already allowed).

## Installation

This utility is self-contained. Ensure you have Python 3.11+ and `PyYAML` installed.

```bash
pip install PyYAML
```

## Usage

To validate a configuration file, you need two things:
1.  The configuration file itself (e.g., `my_doomsday_device.yaml`).
2.  A schema definition file (e.g., `device_schema.yaml`) that specifies the expected structure.

```bash
python src/validator.py --config-file path/to/your/config.yaml --schema-file path/to/your/schema.yaml
```

### Example Schema (`device_schema.yaml`)

```yaml
required_keys:
  - device_name
  - activation_sequence
  - power_source
optional_keys:
  - debug_mode
key_types:
  device_name: str
  activation_sequence: list
  power_source: str
  debug_mode: bool
list_item_types:
  activation_sequence: str # All items in activation_sequence must be strings
```

### Example Config (`my_doomsday_device.yaml`)

```yaml
device_name: "Chronos Disruptor"
activation_sequence:
  - "Initiate temporal flux capacitor"
  - "Calibrate quantum entanglement field"
  - "Engage reality anchor"
power_source: "Dark Matter Reactor"
debug_mode: false
```

### Validation Output

- **Success**: `[INTEGRATOR] Doomsday device configuration 'my_doomsday_device.yaml' is structurally sound. The end is nigh, but at least it's configured correctly.`
- **Failure**: `[INTEGRATOR] ERROR: Doomsday device configuration 'my_doomsday_device.yaml' has critical structural anomalies! (Missing key: 'power_source')`

## Development

To run tests from the `utils/doomsday-config-validator/` directory:

```bash
python -m pytest tests/
```
