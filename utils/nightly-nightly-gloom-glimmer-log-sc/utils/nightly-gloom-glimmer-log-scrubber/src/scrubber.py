import argparse
import json
import sys

def load_config(config_path):
    """Loads configuration from a JSON file."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return {
            'keywords_to_highlight': [k.lower() for k in config.get('keywords_to_highlight', [])],
            'keywords_to_ignore': [k.lower() for k in config.get('keywords_to_ignore', [])]
        }
    except FileNotFoundError:
        print(f"Error: Config file not found at '{config_path}'", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in config file '{config_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while loading config: {e}", file=sys.stderr)
        sys.exit(1)

def scrub_log(log_file_path, config):
    """Reads a log file, filters and highlights lines based on config."""
    keywords_to_highlight = config.get('keywords_to_highlight', [])
    keywords_to_ignore = config.get('keywords_to_ignore', [])

    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                line_lower = line.lower().strip()
                
                # Check if line should be ignored (ignore takes precedence)
                if any(keyword in line_lower for keyword in keywords_to_ignore):
                    continue
                
                # Check if line should be highlighted (printed)
                if any(keyword in line_lower for keyword in keywords_to_highlight):
                    print(line.strip())

    except FileNotFoundError:
        print(f"Error: Log file not found at '{log_file_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while scrubbing log: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Gloom-Glimmer Log Scrubber: Filter and highlight critical information from log files."
    )
    parser.add_argument('--log-file', required=True, help='Path to the log file to scrub.')
    parser.add_argument('--config-file', required=True, help='Path to the JSON configuration file.')
    
    args = parser.parse_args()

    config = load_config(args.config_file)
    scrub_log(args.log_file, config)

if __name__ == '__main__':
    main()
