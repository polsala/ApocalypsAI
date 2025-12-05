import os
import argparse
from typing import List

def get_env_vars(prefix: str = "") -> dict:
    """
    Retrieves environment variables, optionally filtered by a prefix.
    """
    env_vars = {}
    for key, value in os.environ.items():
        if key.startswith(prefix):
            env_vars[key] = value
    return env_vars

def identify_sensitive_vars(env_vars: dict, sensitive_keywords: List[str]) -> dict:
    """
    Identifies potentially sensitive environment variables based on keywords.
    Returns a dictionary where keys are env var names and values are boolean (is_sensitive).
    """
    sensitive_status = {}
    for key in env_vars:
        is_sensitive = any(keyword.lower() in key.lower() for keyword in sensitive_keywords)
        sensitive_status[key] = is_sensitive
    return sensitive_status

def main():
    parser = argparse.ArgumentParser(
        description="A gentle utility to reveal and categorize your environment variables."
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default="",
        help="Only show environment variables starting with this prefix."
    )
    parser.add_argument(
        "--sensitive-keywords",
        type=str,
        default="KEY,TOKEN,PASSWORD,SECRET,API_KEY,AUTH",
        help="Comma-separated keywords to identify potentially sensitive variables."
    )
    args = parser.parse_args()

    sensitive_keywords_list = [k.strip() for k in args.sensitive_keywords.split(',') if k.strip()]

    print("🌌 Nightly Env-Var Whisperer 🌌\n")
    print(f"Whispering environment variables (prefix: '{args.prefix}', sensitive keywords: {sensitive_keywords_list}):\n")

    env_vars = get_env_vars(args.prefix)
    sensitive_status = identify_sensitive_vars(env_vars, sensitive_keywords_list)

    if not env_vars:
        print("No environment variables found matching the criteria.")
        return

    for key in sorted(env_vars.keys()):
        status = " (Sensitive? ✨)" if sensitive_status[key] else ""
        # Mask sensitive values for display, but not for internal logic
        display_value = "***REDACTED***" if sensitive_status[key] else env_vars[key]
        print(f"  - {key}: {display_value}{status}")

if __name__ == "__main__":
    main()
