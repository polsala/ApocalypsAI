import argparse
import yaml
import sys
import os

def compare_configs(golden_config, target_config, path="", differences=None):
    """Recursively compares two dictionaries (configs) and records differences."""
    if differences is None:
        differences = []

    # Compare keys present in golden_config
    for key, golden_value in golden_config.items():
        current_path = f"{path}.{key}" if path else key
        if key not in target_config:
            differences.append(f"Missing key in target at '{current_path}'")
        else:
            target_value = target_config[key]
            if isinstance(golden_value, dict) and isinstance(target_value, dict):
                compare_configs(golden_value, target_value, current_path, differences)
            elif golden_value != target_value:
                differences.append(f"Difference found at '{current_path}': Golden='{golden_value}', Target='{target_value}'")

    # Check for extra keys in target_config
    for key, target_value in target_config.items():
        current_path = f"{path}.{key}" if path else key
        if key not in golden_config:
            differences.append(f"Extra key in target at '{current_path}': '{target_value}'")

    return differences

def main():
    parser = argparse.ArgumentParser(
        description="Compares target YAML configuration files against a golden standard."
    )
    parser.add_argument(
        "--golden-config",
        required=True,
        help="Path to the golden standard YAML configuration file."
    )
    parser.add_argument(
        "--target-configs",
        nargs='+',
        required=True,
        help="One or more paths to the target YAML configuration files."
    )

    args = parser.parse_args()

    total_discrepancies = 0

    try:
        with open(args.golden_config, 'r') as f:
            golden_data = yaml.safe_load(f)
        if not isinstance(golden_data, dict):
            print(f"Error: Golden config '{args.golden_config}' is not a valid YAML dictionary.", file=sys.stderr)
            sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Golden config file not found at '{args.golden_config}'.", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing golden config '{args.golden_config}': {e}", file=sys.stderr)
        sys.exit(1)

    for target_path in args.target_configs:
        print(f"\n--- Comparing {os.path.basename(target_path)} against {os.path.basename(args.golden_config)} ---")
        try:
            with open(target_path, 'r') as f:
                target_data = yaml.safe_load(f)
            if not isinstance(target_data, dict):
                print(f"Error: Target config '{target_path}' is not a valid YAML dictionary. Skipping.", file=sys.stderr)
                total_discrepancies += 1 # Count as a discrepancy for non-dict format
                continue
        except FileNotFoundError:
            print(f"Error: Target config file not found at '{target_path}'. Skipping.", file=sys.stderr)
            total_discrepancies += 1
            continue
        except yaml.YAMLError as e:
            print(f"Error parsing target config '{target_path}': {e}. Skipping.", file=sys.stderr)
            total_discrepancies += 1
            continue

        differences = compare_configs(golden_data, target_data)

        if differences:
            for diff in differences:
                print(diff)
            print(f"\n--- Comparison complete for {os.path.basename(target_path)} ---")
            print(f"Found {len(differences)} discrepancies in {os.path.basename(target_path)}.")
            total_discrepancies += len(differences)
        else:
            print(f"No discrepancies found in {os.path.basename(target_path)}.")
            print(f"\n--- Comparison complete for {os.path.basename(target_path)} ---")

    print("\n--- Summary ---")
    if total_discrepancies == 0:
        print("All target configurations perfectly match the golden standard.")
        sys.exit(0)
    else:
        print(f"Total discrepancies found across all target configurations: {total_discrepancies}.")
        sys.exit(1)

if __name__ == "__main__":
    main()
