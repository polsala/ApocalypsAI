import json
import sys
import os

def validate_config(config_data):
    errors = []
    warnings = []

    # Rule 1: device_name
    if 'device_name' not in config_data:
        errors.append("Missing required field: 'device_name'.")
    elif not isinstance(config_data['device_name'], str) or not config_data['device_name'].strip():
        errors.append("'device_name' must be a non-empty string.")

    # Rule 2: activation_code
    if 'activation_code' not in config_data:
        errors.append("Missing required field: 'activation_code'.")
    elif not isinstance(config_data['activation_code'], str) or not config_data['activation_code'].isalnum() or len(config_data['activation_code']) < 6:
        errors.append("'activation_code' must be an alphanumeric string of at least 6 characters.")

    # Rule 3: target_population_percentage
    if 'target_population_percentage' not in config_data:
        errors.append("Missing required field: 'target_population_percentage'.")
    elif not isinstance(config_data['target_population_percentage'], int) or not (0 <= config_data['target_population_percentage'] <= 100):
        errors.append("'target_population_percentage' must be an integer between 0 and 100.")

    # Rule 4: power_source
    if 'power_source' not in config_data:
        errors.append("Missing required field: 'power_source'.")
    elif not isinstance(config_data['power_source'], str) or not config_data['power_source'].strip():
        errors.append("'power_source' must be a non-empty string.")

    # Rule 5: countdown_timer_seconds
    if 'countdown_timer_seconds' not in config_data:
        errors.append("Missing required field: 'countdown_timer_seconds'.")
    elif not isinstance(config_data['countdown_timer_seconds'], int) or config_data['countdown_timer_seconds'] <= 0:
        errors.append("'countdown_timer_seconds' must be a positive integer.")

    # Rule 6: safety_protocols (optional)
    if 'safety_protocols' in config_data:
        if not isinstance(config_data['safety_protocols'], list):
            errors.append("'safety_protocols' must be a list of strings.")
        else:
            for i, protocol in enumerate(config_data['safety_protocols']):
                if not isinstance(protocol, str) or not protocol.strip():
                    errors.append(f"'safety_protocols' item {i} must be a non-empty string.")

    # Rule 7: self_destruct_on_failure (optional)
    if 'self_destruct_on_failure' in config_data and not isinstance(config_data['self_destruct_on_failure'], bool):
        errors.append("'self_destruct_on_failure' must be a boolean.")

    return errors, warnings

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/debugger.py <config_file.json>")
        sys.exit(1)

    config_path = sys.argv[1]

    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found at '{config_path}'")
        sys.exit(1)

    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{config_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{config_path}': {e}")
        sys.exit(1)

    errors, warnings = validate_config(config_data)

    if errors or warnings:
        print("\n--- Doomsday Device Debug Report ---")
        if errors:
            print("\nErrors found (critical flaws!):")
            for error in errors:
                print(f"  - {error}")
        if warnings:
            print("\nWarnings found (potential glitches):")
            for warning in warnings:
                print(f"  - {warning}")
        print("\nStatus: Device configuration requires immediate attention!")
        sys.exit(1) # Exit with error code if issues found
    else:
        print("\n--- Doomsday Device Debug Report ---")
        print("\nStatus: Flawless and ready for deployment! The end is nigh (and well-configured).")
        sys.exit(0)

if __name__ == '__main__':
    main()
