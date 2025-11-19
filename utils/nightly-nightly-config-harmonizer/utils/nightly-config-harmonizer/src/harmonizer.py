import argparse
import yaml
import os

def load_yaml(filepath):
    """Loads a YAML file from the given filepath."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def save_yaml(filepath, data):
    """Saves data to a YAML file."""
    with open(filepath, 'w') as f:
        yaml.safe_dump(data, f, default_flow_style=False)

def find_discrepancies(template_config, target_config, path=""):
    """Recursively finds discrepancies between template and target configurations."""
    discrepancies = {
        'missing_keys': [],
        'extra_keys': [],
        'value_mismatches': []
    }

    # Check for missing keys and value mismatches
    for key, template_value in template_config.items():
        current_path = f"{path}.{key}" if path else key
        if key not in target_config:
            discrepancies['missing_keys'].append((current_path, template_value))
        else:
            target_value = target_config[key]
            if isinstance(template_value, dict) and isinstance(target_value, dict):
                sub_discrepancies = find_discrepancies(template_value, target_value, current_path)
                for k, v in sub_discrepancies.items():
                    discrepancies[k].extend(v)
            elif template_value != target_value:
                discrepancies['value_mismatches'].append((current_path, target_value, template_value))

    # Check for extra keys in target (optional, but useful for reporting)
    for key in target_config.keys():
        current_path = f"{path}.{key}" if path else key
        if key not in template_config:
            discrepancies['extra_keys'].append(current_path)

    return discrepancies

def apply_defaults(template_config, target_config):
    """Recursively applies missing keys from template to target config."""
    for key, template_value in template_config.items():
        if key not in target_config:
            target_config[key] = template_value
        elif isinstance(template_value, dict) and isinstance(target_config[key], dict):
            apply_defaults(template_value, target_config[key])
    return target_config

def main():
    parser = argparse.ArgumentParser(
        description="Harmonize a target YAML configuration file with a template."
    )
    parser.add_argument('--template', required=True, help="Path to the golden template YAML file.")
    parser.add_argument('--target', required=True, help="Path to the target YAML file to be harmonized.")
    parser.add_argument('--apply', action='store_true', help="If present, apply missing defaults to the target file.")

    args = parser.parse_args()

    try:
        template_config = load_yaml(args.template)
        target_config = load_yaml(args.target)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        exit(1)

    discrepancies = find_discrepancies(template_config, target_config)

    if any(discrepancies.values()):
        print(f"Discrepancies found in {args.target}:")
        if discrepancies['missing_keys']:
            for key, default_val in discrepancies['missing_keys']:
                print(f"- Missing key: {key} (default: {default_val})")
        if discrepancies['extra_keys']:
            for key in discrepancies['extra_keys']:
                print(f"- Extra key: {key} (not in template)")
        if discrepancies['value_mismatches']:
            for key, target_val, template_val in discrepancies['value_mismatches']:
                print(f"- Value mismatch for {key}: target='{target_val}', template='{template_val}'")

        if args.apply:
            print(f"Applying missing defaults to {args.target}...")
            updated_target_config = apply_defaults(template_config, target_config)
            save_yaml(args.target, updated_target_config)
            print("Harmonization complete. Target file updated.")
        else:
            print("Run with --apply to update the target file with missing defaults.")
    else:
        print(f"No discrepancies found in {args.target}. Configuration is harmonized.")


if __name__ == '__main__':
    main()
