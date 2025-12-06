import argparse
import os
import sys

def get_keys_from_file(filepath: str) -> set[str]:
    """Reads a file and extracts keys (either from KEY=VALUE or just KEY lines)."""
    keys = set()
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Handle KEY=VALUE format
            if '=' in line:
                key = line.split('=', 1)[0].strip()
                keys.add(key)
            # Handle plain KEY format (for template files)
            else:
                keys.add(line)
    return keys

def calibrate_config(config_path: str, template_path: str) -> list[str]:
    """
    Compares a configuration file against a template to find missing keys.

    Args:
        config_path: Path to the configuration file (e.g., .env).
        template_path: Path to the template file listing required keys.

    Returns:
        A list of keys present in the template but missing from the config file.
    Raises:
        FileNotFoundError: If either config_path or template_path does not exist.
    """
    config_keys = get_keys_from_file(config_path)
    template_keys = get_keys_from_file(template_path)

    missing_keys = sorted(list(template_keys - config_keys))
    return missing_keys

def main():
    parser = argparse.ArgumentParser(
        description="Calibrate your configuration files against a template of required keys."
    )
    parser.add_argument(
        "-c", "--config",
        required=True,
        help="Path to the configuration file to calibrate (e.g., .env)."
    )
    parser.add_argument(
        "-t", "--template",
        required=True,
        help="Path to the template file containing required keys (one per line)."
    )

    args = parser.parse_args()

    try:
        missing = calibrate_config(args.config, args.template)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if missing:
        print(f"Missing required keys: {missing}")
        print("Configuration requires calibration!")
        sys.exit(1)
    else:
        print("Configuration calibrated successfully. All required keys are present.")
        sys.exit(0)

if __name__ == "__main__":
    main()
