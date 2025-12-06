import re
import argparse
import sys

def scrub_log_content(content: str, custom_patterns: list[str] = None) -> str:
    """
    Anonymizes sensitive information in a given log content string.

    Args:
        content: The string content of the log file.
        custom_patterns: A list of additional regex patterns to scrub.

    Returns:
        The scrubbed log content string.
    """
    # Default patterns for common sensitive data
    # Order matters: more specific patterns first if they might overlap with generic ones.
    default_scrub_rules = [
        (r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', '[SCRUBBED_IP]'),  # IPv4 addresses
        (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[SCRUBBED_EMAIL]'), # Email addresses
        # Generic long alphanumeric strings (potential API keys, tokens, UUIDs)
        # Avoids scrubbing common words, targets strings typically 20-64 chars long.
        (r'\b[A-Za-z0-9]{20,64}\b', '[SCRUBBED_SECRET]')
    ]

    # Apply custom patterns first, if provided, to allow user override or specific targeting
    if custom_patterns:
        for i, pattern_str in enumerate(custom_patterns):
            try:
                # Use a generic placeholder for custom patterns unless specified otherwise
                # For simplicity, we'll use a numbered placeholder for custom patterns
                content = re.sub(pattern_str, f'[SCRUBBED_CUSTOM_{i+1}]', content)
            except re.error as e:
                print(f"Error: Invalid custom regex pattern '{pattern_str}': {e}", file=sys.stderr)
                # Continue with other patterns even if one is invalid

    # Apply default scrubbing rules
    for pattern, replacement in default_scrub_rules:
        content = re.sub(pattern, replacement, content)

    return content

def main():
    parser = argparse.ArgumentParser(
        description="Anonymize sensitive information in log files."
    )
    parser.add_argument(
        "input_file",
        help="Path to the input log file."
    )
    parser.add_argument(
        "output_file",
        help="Path to the output scrubbed log file."
    )
    parser.add_argument(
        "--patterns",
        nargs='*', # 0 or more arguments
        default=[],
        help="One or more custom regex patterns to apply for scrubbing."
    )

    args = parser.parse_args()

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f_in:
            log_content = f_in.read()
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file '{args.input_file}': {e}", file=sys.stderr)
        sys.exit(1)

    scrubbed_content = scrub_log_content(log_content, args.patterns)

    try:
        with open(args.output_file, 'w', encoding='utf-8') as f_out:
            f_out.write(scrubbed_content)
        print(f"Log file '{args.input_file}' successfully scrubbed to '{args.output_file}'.")
    except Exception as e:
        print(f"Error writing to output file '{args.output_file}': {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
