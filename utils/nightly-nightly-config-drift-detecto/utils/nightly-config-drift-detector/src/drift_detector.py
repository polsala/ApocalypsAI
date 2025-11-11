import argparse
import os
from typing import Set, List, Tuple

def parse_env_file(filepath: str) -> Set[str]:
    """Parses a .env-style file and returns a set of keys found."""
    keys = set()
    if not os.path.exists(filepath):
        return keys

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Handle key=value or key="value" or key='value'
            # Split only on the first '=' to preserve '=' in values
            parts = line.split('=', 1)
            if len(parts) > 0:
                key = parts[0].strip()
                if key:
                    keys.add(key)
    return keys

def detect_drift(template_keys: Set[str], target_keys: Set[str]) -> Tuple[Set[str], Set[str]]:
    """Compares template keys against target keys to find missing and extra keys."""
    missing_keys = template_keys - target_keys
    extra_keys = target_keys - template_keys
    return missing_keys, extra_keys

def main():
    parser = argparse.ArgumentParser(
        description="Detects configuration drift between a template and target .env-style files."
    )
    parser.add_argument(
        '--template', 
        type=str, 
        required=True, 
        help="Path to the reference configuration file (e.g., .env.example)."
    )
    parser.add_argument(
        '--target', 
        type=str, 
        nargs='+', 
        required=True, 
        help="One or more paths to the configuration files to check."
    )

    args = parser.parse_args()

    if not os.path.exists(args.template):
        print(f"Error: Template file '{args.template}' not found.")
        exit(1)

    template_keys = parse_env_file(args.template)

    for target_filepath in args.target:
        print(f"\n--- Checking '{target_filepath}' against '{args.template}' ---")
        target_keys = parse_env_file(target_filepath)

        missing, extra = detect_drift(template_keys, target_keys)

        if not missing and not extra:
            print(f"  ✅ '{target_filepath}' is perfectly aligned with the template.")
        else:
            if missing:
                print(f"  ⚠️  Missing Keys in '{target_filepath}': {', '.join(sorted(list(missing)))}")
            if extra:
                print(f"  🚨 Extra Keys in '{target_filepath}': {', '.join(sorted(list(extra)))}")

if __name__ == '__main__':
    main()
