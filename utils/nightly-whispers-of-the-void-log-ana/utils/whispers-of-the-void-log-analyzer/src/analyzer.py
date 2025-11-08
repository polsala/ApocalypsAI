import argparse
import json
import re
import sys

# Default premonitions if no config file is provided
DEFAULT_PREMONITIONS = {
    "keywords": [
        "error", "fail", "critical", "denied", "exception",
        "timeout", "unauthorized", "corrupt", "malformed",
        "segfault", "panic", "deadlock", "resource exhaustion"
    ],
    "regexes": [
        r"^(CRITICAL|EMERGENCY|ALERT):.*",
        r"connection (refused|reset|timed out)",
        r"out of memory",
        r"disk (full|space low)",
        r"permission denied",
        r"failed to (connect|start|load|authenticate)",
        r"unhandled exception"
    ]
}

def load_config(config_path):
    """Loads premonitions from a JSON configuration file."""
    if config_path:
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            # Ensure keywords and regexes are lists, provide defaults if missing
            config['keywords'] = [k.lower() for k in config.get('keywords', [])]
            config['regexes'] = config.get('regexes', [])
            return config
        except FileNotFoundError:
            print(f"Error: Configuration file not found at '{config_path}'", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in configuration file '{config_path}'", file=sys.stderr)
            sys.exit(1)
    return DEFAULT_PREMONITIONS

def analyze_log(log_path, config_path=None):
    """
    Scans a log file for predefined keywords and regex patterns (premonitions).
    Prints any detected premonitions with their line numbers.
    """
    premonitions = load_config(config_path)
    keywords = premonitions['keywords']
    regexes = [re.compile(r, re.IGNORECASE) for r in premonitions['regexes']]

    found_premonitions = False

    try:
        with open(log_path, 'r') as log_file:
            for line_num, line in enumerate(log_file, 1):
                line_lower = line.lower()

                # Check for keywords
                for keyword in keywords:
                    if keyword in line_lower:
                        print(f"[LINE {line_num}] Premonition: '{keyword}' found in '{line.strip()}'")
                        found_premonitions = True
                        break # Only report one keyword match per line

                # Check for regex patterns
                for regex in regexes:
                    if regex.search(line):
                        print(f"[LINE {line_num}] Premonition: Regex '{regex.pattern}' matched in '{line.strip()}'")
                        found_premonitions = True
                        break # Only report one regex match per line

    except FileNotFoundError:
        print(f"Error: Log file not found at '{log_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

    if not found_premonitions:
        print("No whispers of the void detected. All clear... for now.")
        sys.exit(0) # Indicate success, but no premonitions found
    else:
        sys.exit(0) # Indicate success, premonitions found

def main():
    parser = argparse.ArgumentParser(
        description="Whispers of the Void Log Analyzer: Detects early signs of impending doom in log files."
    )
    parser.add_argument(
        "log_file",
        help="Path to the log file to analyze."
    )
    parser.add_argument(
        "--config",
        help="Path to a JSON configuration file for custom premonitions (keywords and regexes)."
    )
    args = parser.parse_args()

    analyze_log(args.log_file, args.config)

if __name__ == "__main__":
    main()
