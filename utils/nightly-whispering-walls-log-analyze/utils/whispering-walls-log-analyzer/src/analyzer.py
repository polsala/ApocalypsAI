import argparse
import re
import json
import sys

# Default patterns and their whimsical narratives
DEFAULT_PATTERNS = [
    {"regex": r"ERROR", "narrative": "A faint echo of despair: {match} found!"},
    {"regex": r"WARNING|WARN", "narrative": "The walls murmur a caution: {match} detected."},
    {"regex": r"FATAL", "narrative": "A strange ripple in the data stream: {match} observed."},
    {"regex": r"EXCEPTION", "narrative": "A sudden tremor in the fabric of reality: {match} occurred."},
    {"regex": r"CRITICAL", "narrative": "The very foundations groan: {match} event."},
]

def load_patterns(config_file=None):
    """Loads patterns from a configuration file, merging with default patterns."""
    patterns = list(DEFAULT_PATTERNS) # Start with a copy of default patterns
    if config_file:
        try:
            with open(config_file, 'r') as f:
                custom_config = json.load(f)
                if 'patterns' in custom_config and isinstance(custom_config['patterns'], list):
                    # For simplicity, custom patterns are appended.
                    # A more complex system might allow overriding defaults by regex.
                    patterns.extend(custom_config['patterns'])
        except FileNotFoundError:
            print(f"Error: Configuration file '{config_file}' not found.", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in configuration file '{config_file}'.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error loading configuration: {e}", file=sys.stderr)
            sys.exit(1)
    return patterns

def analyze_log(log_file_path, config_file=None):
    """
    Analyzes a log file for predefined patterns and prints whimsical narratives.
    """
    patterns = load_patterns(config_file)
    found_whispers = []

    print("Listening to the digital whispers...\n")

    try:
        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for pattern_def in patterns:
                    regex = pattern_def.get("regex")
                    narrative_template = pattern_def.get("narrative")

                    if not regex or not narrative_template:
                        print(f"Warning: Malformed pattern definition skipped: {pattern_def}", file=sys.stderr)
                        continue

                    match = re.search(regex, line)
                    if match:
                        # Use the full matched string for the narrative
                        whisper = narrative_template.format(match=match.group(0).strip())
                        found_whispers.append(f"[Line {line_num}] {whisper}")
                        break # Only report the first matching pattern per line
    except FileNotFoundError:
        print(f"Error: Log file '{log_file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading log file: {e}", file=sys.stderr)
        sys.exit(1)

    if found_whispers:
        for whisper in found_whispers:
            print(whisper)
    else:
        print("The walls are silent. No significant whispers detected.")

    print("\nAnalysis complete. The walls have spoken.")

def main():
    parser = argparse.ArgumentParser(
        description="Whispering Walls Log Analyzer: Sifts through log files for anomalies."
    )
    parser.add_argument(
        "--log-file",
        required=True,
        help="Path to the log file to analyze."
    )
    parser.add_argument(
        "--config-file",
        help="Optional path to a JSON configuration file for custom patterns."
    )
    args = parser.parse_args()

    analyze_log(args.log_file, args.config_file)

if __name__ == "__main__":
    main()
