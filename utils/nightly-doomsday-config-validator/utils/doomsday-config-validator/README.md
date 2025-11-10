# Doomsday Config Validator

## Overview

The `doomsday-config-validator` is a crucial utility for any aspiring supervillain or benevolent global guardian. It ensures that your hypothetical Doomsday Device's configuration file (YAML) is perfectly structured and contains all the necessary parameters for its intended operation – be it global annihilation, localized disruption, or even peaceful coexistence.

Misconfigured doomsday devices are a common cause of accidental world-saving or, worse, incomplete destruction. This validator helps prevent such embarrassing mishaps by checking for required fields, valid data types, acceptable ranges, and logical consistency.

## Configuration Structure

The validator expects a YAML file with the following structure:

```yaml
device_name: "Omega Protocol Initiator"
activation_code: "ALPHA-OMEGA-7" # Must match pattern AAAAA-BBBBB-C
target_mode: "global_annihilation" # or "localized_disruption", "peaceful_coexistence"
payload_yield: 1000 # kilotons, required for destructive modes, must be > 0
safety_protocols_active: true # Boolean
self_destruct_sequence:
  enabled: false # Boolean
  countdown_hours: 24 # required if enabled is true, must be > 0
```

## Usage

To validate a configuration file, run the `validator.py` script with the path to your YAML file:

```bash
python src/validator.py path/to/your/config.yaml
```

### Exit Codes

*   `0`: Configuration is valid.
*   `1`: Configuration is invalid or an error occurred (details printed to stderr).

## Example Valid Configuration (`valid_config.yaml`)

```yaml
device_name: "World-Ender 9000"
activation_code: "ZETA-GAMMA-3"
target_mode: "global_annihilation"
payload_yield: 5000
safety_protocols_active: false
```

## Example Invalid Configuration (`invalid_config.yaml`)

```yaml
device_name: "The Pacifier"
activation_code: "BAD-CODE-X" # Invalid format
target_mode: "peaceful_coexistence"
payload_yield: 100 # Payload yield not allowed for peaceful mode
safety_protocols_active: true
```
