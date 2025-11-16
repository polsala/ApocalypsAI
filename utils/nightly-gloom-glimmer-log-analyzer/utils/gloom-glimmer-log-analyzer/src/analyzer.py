import argparse
import yaml
import sys
from collections import defaultdict

DEFAULT_CONFIG = {
    'patterns': {
        'gloom': [
            "ERROR",
            "CRITICAL",
            "FAILURE",
            "EXCEPTION",
            "FATAL",
            "DENIED"
        ],
        'warning': [
            "WARNING",
            "DEPRECATED",
            "TIMEOUT",
            "UNAUTHORIZED",
            "SLOW"
        ],
        'glimmer': [
            "SUCCESS",
            "OPTIMIZED",
            "HEALED",
            "RECOVERED",
            "STABLE",
            "RESTORED",
            "ONLINE"
        ]
    }
}

def load_config(config_path=None):
    """Loads configuration from a YAML file or returns the default."""
    if config_path:
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file not found at '{config_path}'. Using default config.", file=sys.stderr)
        except yaml.YAMLError as e:
            print(f"Error: Invalid YAML in config file '{config_path}': {e}. Using default config.", file=sys.stderr)
    return DEFAULT_CONFIG

def analyze_log(log_file_path, config):
    """
    Analyzes a log file for predefined patterns and returns a summary.
    """
    results = {
        'gloom': [],
        'warning': [],
        'glimmer': [],
        'counts': defaultdict(int),
        'total_lines': 0
    }

    patterns = {
        category: [p.lower() for p in config['patterns'].get(category, [])]
        for category in ['gloom', 'warning', 'glimmer']
    }

    try:
        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                results['total_lines'] += 1
                lower_line = line.lower()

                for category, category_patterns in patterns.items():
                    for pattern in category_patterns:
                        if pattern in lower_line:
                            results['counts'][category] += 1
                            if category in ['gloom', 'glimmer']: # Store specific lines for these categories
                                results[category].append(f"  - Line {line_num}: {line.strip()}")
                            # No break here, continue checking other patterns within the same category
                            # and other categories for the same line. This allows a line to match multiple categories.

    except FileNotFoundError:
        print(f"Error: Log file not found at '{log_file_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading the log file: {e}", file=sys.stderr)
        sys.exit(1)

    return results

def print_report(log_file_path, analysis_results):
    """Prints the formatted analysis report."""
    print("\n--- Gloom-Glimmer Log Analysis Report ---")
    print(f"Log File: {log_file_path}\n")

    print(f"Gloom (Errors/Critical): {analysis_results['counts']['gloom']}")
    if analysis_results['gloom']:
        for line in analysis_results['gloom']:
            print(line)
    print()

    print(f"Warning (Warnings/Issues): {analysis_results['counts']['warning']}")
    # We don't print individual warning lines by default to keep report concise
    print()

    print(f"Glimmer (Success/Hope): {analysis_results['counts']['glimmer']}")
    if analysis_results['glimmer']:
        for line in analysis_results['glimmer']:
            print(line)
    print()

    print(f"Total Lines Analyzed: {analysis_results['total_lines']}")
    print("--- End Report ---")

def main():
    parser = argparse.ArgumentParser(
        description="Analyze log files for 'Gloom' (errors), 'Warning', and 'Glimmer' (success) patterns."
    )
    parser.add_argument("log_file_path", help="Path to the log file to analyze.")
    parser.add_argument("--config", help="Path to a YAML configuration file.", default=None)

    args = parser.parse_args()

    config = load_config(args.config)
    results = analyze_log(args.log_file_path, config)
    print_report(args.log_file_path, results)

if __name__ == "__main__":
    main()
