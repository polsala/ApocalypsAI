import json
import sys
import os
import argparse

def validate_config(config_path: str) -> list[str]:
    """
    Validates a doomsday device configuration file.
    Returns a list of error messages, or an empty list if valid.
    """
    errors = []

    if not os.path.exists(config_path):
        errors.append(f"Error: Configuration file not found at '{config_path}'.")
        return errors

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Error: Invalid JSON format in '{config_path}': {e}")
        return errors
    except Exception as e:
        errors.append(f"Error reading '{config_path}': {e}")
        return errors

    # --- Validation Rules ---

    # 1. device_name: Must be a non-empty string.
    device_name = config.get('device_name')
    if not isinstance(device_name, str) or not device_name.strip():
        errors.append("Validation Error: 'device_name' must be a non-empty string.")

    # 2. activation_sequence: Must be a list of at least 3 integers.
    activation_sequence = config.get('activation_sequence')
    if not isinstance(activation_sequence, list):
        errors.append("Validation Error: 'activation_sequence' must be a list.")
    elif len(activation_sequence) < 3:
        errors.append("Validation Error: 'activation_sequence' must contain at least 3 elements.")
    elif not all(isinstance(item, int) for item in activation_sequence):
        errors.append("Validation Error: All elements in 'activation_sequence' must be integers.")

    # 3. target_coordinates: Must be a list/tuple of exactly 2 floats.
    target_coordinates = config.get('target_coordinates')
    if not isinstance(target_coordinates, (list, tuple)):
        errors.append("Validation Error: 'target_coordinates' must be a list or tuple.")
    elif len(target_coordinates) != 2:
        errors.append("Validation Error: 'target_coordinates' must contain exactly 2 elements.")
    elif not all(isinstance(item, (float, int)) for item in target_coordinates): # Allow int as float-compatible
        errors.append("Validation Error: Both elements in 'target_coordinates' must be numbers (float or int).")

    # 4. safety_override_code: Must be a non-empty string.
    safety_override_code = config.get('safety_override_code')
    if not isinstance(safety_override_code, str) or not safety_override_code.strip():
        errors.append("Validation Error: 'safety_override_code' must be a non-empty string.")

    # 5. power_level: Must be an integer between 1 and 10000 (inclusive).
    power_level = config.get('power_level')
    if not isinstance(power_level, int):
        errors.append("Validation Error: 'power_level' must be an integer.")
    elif not (1 <= power_level <= 10000):
        errors.append("Validation Error: 'power_level' must be between 1 and 10000.")

    # 6. status: Must be one of "standby", "armed", or "disarmed".
    status = config.get('status')
    allowed_statuses = ["standby", "armed", "disarmed"]
    if not isinstance(status, str) or status not in allowed_statuses:
        errors.append(f"Validation Error: 'status' must be one of {allowed_statuses}.")

    return errors

def main():
    parser = argparse.ArgumentParser(
        description="Validate a doomsday device configuration file."
    )
    parser.add_argument(
        "--config-path",
        type=str,
        required=True,
        help="Path to the JSON configuration file."
    )
    args = parser.parse_args()

    errors = validate_config(args.config_path)

    if errors:
        print("\nDoomsday Config Validation Failed! Detected issues:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1) # Exit with error code
    else:
        print("\nDoomsday Config Validation Successful! All systems nominal. Proceed with caution.")
        sys.exit(0) # Exit with success code

if __name__ == "__main__":
    main()
