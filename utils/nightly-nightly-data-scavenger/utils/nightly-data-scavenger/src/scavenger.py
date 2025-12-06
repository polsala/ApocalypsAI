import argparse
import re
import json
import sys

def scavenge_logs(log_file_path: str, pattern: str, output_file_path: str = None):
    """
    Scavenges a log file for patterns and extracts named groups into JSON Lines.

    Args:
        log_file_path (str): Path to the input log file.
        pattern (str): Regular expression pattern with named capture groups.
        output_file_path (str, optional): Path to the output JSONL file.
                                          If None, output to stdout.
    """
    compiled_pattern = re.compile(pattern)
    output_stream = None

    try:
        if output_file_path:
            output_stream = open(output_file_path, 'w', encoding='utf-8')
        else:
            output_stream = sys.stdout

        with open(log_file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                match = compiled_pattern.match(line)
                if match:
                    extracted_data = match.groupdict()
                    json_line = json.dumps(extracted_data, ensure_ascii=False)
                    output_stream.write(json_line + '\n')
    except FileNotFoundError:
        print(f"Error: Log file not found at '{log_file_path}'", file=sys.stderr)
        sys.exit(1)
    except re.error as e:
        print(f"Error: Invalid regex pattern '{pattern}': {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if output_file_path and output_stream:
            output_stream.close()

def main():
    parser = argparse.ArgumentParser(
        description="Scavenge log files for patterns and extract structured data."
    )
    parser.add_argument(
        "--log-file",
        required=True,
        help="Path to the input log file."
    )
    parser.add_argument(
        "--pattern",
        required=True,
        help="Regular expression pattern with named capture groups (e.g., '(?P<name>...)')."
    )
    parser.add_argument(
        "--output-file",
        help="Optional path to the output JSONL file. If not provided, output to stdout."
    )

    args = parser.parse_args()

    scavenge_logs(args.log_file, args.pattern, args.output_file)

if __name__ == "__main__":
    main()
