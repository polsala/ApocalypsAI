# Doomsday Device Debugger

## Purpose

Ensuring the end of the world goes off without a hitch requires meticulous planning and flawless execution. The `Doomsday Device Debugger` is a whimsical-yet-critical utility designed to validate your doomsday device configuration files for logical consistency, missing components, and common operational flaws. It helps you identify potential issues before your grand finale fizzles.

## Usage

To debug a doomsday device configuration, simply run the Python script with the path to your JSON configuration file:

```bash
python src/debugger.py path/to/your_device_config.json
```

The script will output a report detailing any errors or warnings found in your configuration.

## Configuration Format Example (`example_device.json`)

```json
{
  "device_name": "Global Annihilation Engine v3.1",
  "activation_code": "OMEGA777",
  "target_population_percentage": 100,
  "power_source": "Dark Matter Reactor",
  "countdown_timer_seconds": 3600,
  "safety_protocols": [
    "Two-key activation",
    "Biometric override"
  ],
  "self_destruct_on_failure": true
}
```

## Validation Rules

The debugger checks for the following:

*   `device_name`: Required, string, non-empty.
*   `activation_code`: Required, string, alphanumeric, minimum 6 characters.
*   `target_population_percentage`: Required, integer, between 0 and 100 (inclusive).
*   `power_source`: Required, string, non-empty.
*   `countdown_timer_seconds`: Required, integer, positive.
*   `safety_protocols`: Optional, list of strings. Each string must be non-empty.
*   `self_destruct_on_failure`: Optional, boolean.

## Output

The script will print a summary of validation results, listing any errors or warnings. If no issues are found, it will declare the device configuration 'Flawless and ready for deployment!'.
