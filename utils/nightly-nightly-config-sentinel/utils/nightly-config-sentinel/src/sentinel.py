import os
import argparse
from typing import List, Dict

def parse_env_file(filepath: str) -> Dict[str, str]:
    """Parses a .env file into a dictionary."""
    config = {}
    if not os.path.exists(filepath):
        return config
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config

def check_config(filepath: str) -> List[str]:
    """
    Checks a .env file for common configuration issues.

    Args:
        filepath: The path to the .env file.

    Returns:
        A list of warning messages.
    """
    warnings = []
    config = parse_env_file(filepath)

    if not os.path.exists(filepath):
        warnings.append(f"[ERROR] Configuration file '{filepath}' not found.")
        return warnings
    
    if not config:
        warnings.append(f"[INFO] No key-value pairs found in '{filepath}'.")

    # Check for DEBUG=True
    if config.get('DEBUG', '').lower() == 'true':
        warnings.append("[WARNING] Found 'DEBUG=True'. This is often unsafe for production environments.")

    # Check for empty sensitive variables
    sensitive_keys_patterns = ['_KEY', '_SECRET', '_TOKEN', '_PASSWORD', 'DB_HOST', 'DB_USER', 'DB_PASS']
    for key, value in config.items():
        if any(pattern in key.upper() for pattern in sensitive_keys_patterns) and not value:
            warnings.append(f"[WARNING] Sensitive variable '{key}' has an empty or whitespace-only value.")

    return warnings

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Config Sentinel: Checks .env files for common issues."
    )
    parser.add_argument(
        '--file',
        type=str,
        required=True,
        help="Path to the .env configuration file to check."
    )
    args = parser.parse_args()

    print(f"Checking configuration file: {args.file}\n")
    print("--- Sentinel Report ---")
    issues = check_config(args.file)
    if issues:
        for issue in issues:
            print(issue)
    else:
        print("[INFO] No issues found. Configuration looks good!")
    print("--- End Report ---")

if __name__ == "__main__":
    main()
