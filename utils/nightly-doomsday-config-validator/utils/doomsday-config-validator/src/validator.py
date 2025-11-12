import sys
import yaml
import json

def validate_config(config_data):
    errors = []

    # 1. Check for critical parameters
    if 'activation_code' not in config_data:
        errors.append("Missing critical parameter: 'activation_code'.")
    elif not isinstance(config_data['activation_code'], str):
        errors.append("'activation_code' must be a string.")

    if 'target_coordinates' not in config_data:
        errors.append("Missing critical parameter: 'target_coordinates'.")
    elif not (isinstance(config_data['target_coordinates'], list) and
              len(config_data['target_coordinates']) == 2 and
              all(isinstance(coord, (int, float)) for coord in config_data['target_coordinates'])):
        errors.append("'target_coordinates' must be a list of two numbers (latitude, longitude).")

    if 'power_source' not in config_data:
        errors.append("Missing critical parameter: 'power_source'.")
    elif config_data['power_source'] not in ['solar', 'fusion', 'dark_matter', 'antimatter']:
        errors.append(f"Invalid 'power_source': '{config_data['power_source']}'. Must be one of 'solar', 'fusion', 'dark_matter', 'antimatter'.")

    if 'countdown_timer_seconds' not in config_data:
        errors.append("Missing critical parameter: 'countdown_timer_seconds'.")
    elif not isinstance(config_data['countdown_timer_seconds'], int) or config_data['countdown_timer_seconds'] <= 0:
        errors.append("'countdown_timer_seconds' must be a positive integer.")

    # 2. Check for optional parameters and their types/conflicts
    if 'safety_override' in config_data and not isinstance(config_data['safety_override'], bool):
        errors.append("'safety_override' must be a boolean.")

    if 'self_destruct_on_failure' in config_data and not isinstance(config_data['self_destruct_on_failure'], bool):
        errors.append("'self_destruct_on_failure' must be a boolean.")

    # 3. Check for logical conflicts
    if config_data.get('safety_override') is True and config_data.get('self_destruct_on_failure') is True:
        errors.append("Conflicting settings: 'safety_override' and 'self_destruct_on_failure' cannot both be true. Choose your fate!")

    return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/validator.py <config_file.yaml|json>")
        sys.exit(1)

    config_file_path = sys.argv[1]
    config_data = {}

    try:
        with open(config_file_path, 'r') as f:
            if config_file_path.endswith(('.yaml', '.yml')):
                config_data = yaml.safe_load(f)
            elif config_file_path.endswith('.json'):
                config_data = json.load(f)
            else:
                print(f"Error: Unsupported file type for {config_file_path}. Must be .yaml, .yml, or .json.")
                sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at '{config_file_path}'.")
        sys.exit(1)
    except (yaml.YAMLError, json.JSONDecodeError) as e:
        print(f"Error parsing configuration file '{config_file_path}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

    if not isinstance(config_data, dict):
        print("Error: Configuration file must contain a dictionary/object at its root.")
        sys.exit(1)

    errors = validate_config(config_data)

    if errors:
        print(f"\nDoomsday Configuration for '{config_file_path}' is INVALID! Detected the following anomalies:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    else:
        print(f"\nDoomsday Configuration for '{config_file_path}' is VALID! Proceed with caution... or don't.")
        sys.exit(0)

if __name__ == '__main__':
    main()
