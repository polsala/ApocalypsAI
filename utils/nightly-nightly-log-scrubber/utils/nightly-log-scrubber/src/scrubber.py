import re
import argparse
import sys

def scrub_log_content(content: str, custom_patterns: list[tuple[str, str]]) -> str:
    """
    Scrubs sensitive information from the given log content.
    """
    # Redact IPv4 addresses
    # Regex for IPv4: Matches 4 sets of 1-3 digits separated by dots.
    content = re.sub(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', '[REDACTED_IP]', content)

    # Redact email addresses
    # Regex for email: Basic pattern for user@domain.tld
    content = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[REDACTED_EMAIL]', content)

    # Redact custom patterns
    for pattern, replacement in custom_patterns:
        content = re.sub(pattern, replacement, content)

    return content

def main():
    parser = argparse.ArgumentParser(
        description="Scrub sensitive information from log files."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the log file to be scrubbed."
    )
    parser.add_argument(
        "--output",
        help="Path to the file where the scrubbed logs will be written. If not provided, output is printed to stdout."
    )
    parser.add_argument(
        "--custom-pattern",
        action='append',
        metavar='REGEX_PATTERN',
        help="A regular expression pattern to search for and redact. Can be specified multiple times."
    )
    parser.add_argument(
        "--replacement",
        default="[REDACTED_CUSTOM]",
        help="The string to replace custom-pattern matches with. Applies to all custom patterns."
    )

    args = parser.parse_args()

    custom_patterns_with_replacements = []
    if args.custom_pattern:
        for pattern in args.custom_pattern:
            custom_patterns_with_replacements.append((pattern, args.replacement))

    try:
        with open(args.input, 'r', encoding='utf-8') as f_in:
            log_content = f_in.read()

        scrubbed_content = scrub_log_content(log_content, custom_patterns_with_replacements)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f_out:
                f_out.write(scrubbed_content)
            print(f"Scrubbed content written to '{args.output}'")
        else:
            sys.stdout.write(scrubbed_content)

    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
