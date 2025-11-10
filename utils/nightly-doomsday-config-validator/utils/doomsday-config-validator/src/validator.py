import yaml
import sys
import re

def validate_config(config_data):
    errors = []

    # 1. device_name: Required, string, not empty.
    if 'device_name' not in config_data:
        errors.append("Missing required field: 'device_name'.")
    elif not isinstance(config_data['device_name'], str) or not config_data['device_name'].strip():
        errors.append("'device_name' must be a non-empty string.")

    # 2. activation_code: Required, string, matches pattern [A-Z]{5}-[A-Z]{5}-\d{1}.
    if 'activation_code' not in config_data:
        errors.append("Missing required field: 'activation_code'.")
    elif not isinstance(config_data['activation_code'], str) or not re.fullmatch(r'[A-Z]{5}-[A-Z]{5}-\d{1}', config_data['activation_code']):
        errors.append("'activation_code' must be a string matching pattern 'AAAAA-BBBBB-C'.")

    # 3. target_mode: Required, one of 'global_annihilation', 'localized_disruption', 'peaceful_coexistence'.
    valid_modes = ['global_annihilation', 'localized_disruption', 'peaceful_coexistence']
    if 'target_mode' not in config_data:
        errors.append("Missing required field: 'target_mode'.")
    elif config_data['target_mode'] not in valid_modes:
        errors.append(f"'target_mode' must be one of {', '.join(valid_modes)}.")

    # 4. payload_yield: Required for destructive modes, must be int > 0. Not allowed for peaceful_coexistence.
    target_mode = config_data.get('target_mode')
    if target_mode in ['global_annihilation', 'localized_disruption']:
        if 'payload_yield' not in config_data:
            errors.append(f"'payload_yield' is required for '{target_mode}' mode.")
        elif not isinstance(config_data['payload_yield'], int) or config_data['payload_yield'] <= 0:
            errors.append("'payload_yield' must be an integer greater than 0.")
    elif target_mode == 'peaceful_coexistence':
        if 'payload_yield' in config_data:
            errors.append("'payload_yield' is not allowed for 'peaceful_coexistence' mode.")

    # 5. safety_protocols_active: Required, boolean.
    if 'safety_protocols_active' not in config_data:
        errors.append("Missing required field: 'safety_protocols_active'.")
    elif not isinstance(config_data['safety_protocols_active'], bool):
        errors.append("'safety_protocols_active' must be a boolean.")

    # 6. self_destruct_sequence: Optional. If present, validate sub-fields.
    if 'self_destruct_sequence' in config_data:
        sd_sequence = config_data['self_destruct_sequence']
        if not isinstance(sd_sequence, dict):
            errors.append("'self_destruct_sequence' must be a dictionary.")
        else:
            if 'enabled' not in sd_sequence:
                errors.append("Missing required field in 'self_destruct_sequence': 'enabled'.")
            elif not isinstance(sd_sequence['enabled'], bool):
                errors.append("'self_destruct_sequence.enabled' must be a boolean.")

            if sd_sequence.get('enabled', False):
                if 'countdown_hours' not in sd_sequence:
                    errors.append("Missing required field in 'self_destruct_sequence': 'countdown_hours' when enabled is true.")
                elif not isinstance(sd_sequence['countdown_hours'], int) or sd_sequence['countdown_hours'] <= 0:
                    errors.append("'self_destruct_sequence.countdown_hours' must be an integer greater than 0 when enabled is true.")

    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: python validator.py <config_file.yaml>", file=sys.stderr)
        sys.exit(1)

    config_file_path = sys.argv[1]

    try:
        with open(config_file_path, 'r') as f:
            config_data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at '{config_file_path}'.", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(config_data, dict):
        print("Error: YAML content must be a dictionary.", file=sys.stderr)
        sys.exit(1)

    errors = validate_config(config_data)

    if errors:
        print("Configuration is INVALID:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        sys.exit(1)
    else:
        print("Configuration is VALID.")
        sys.exit(0)


if __name__ == '__main__':
    main()
