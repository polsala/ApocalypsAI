import re
import argparse
import sys

# Regex patterns for common sensitive data
IP_PATTERN = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
# Basic credit card pattern (not exhaustive, but covers common formats)
# Visa: 4[0-9]{12}(?:[0-9]{3})?
# MasterCard: 5[1-5][0-9]{14}
# Amex: 3[47][0-9]{13}
# Discover: 6(?:011|5[0-9]{2})[0-9]{12}
CREDIT_CARD_PATTERN = re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b')

def anonymize_line(line: str) -> str:
    """Anonymizes sensitive patterns in a single line."""
    line = IP_PATTERN.sub('[ANONYMIZED_IP]', line)
    line = EMAIL_PATTERN.sub('[REDACTED_EMAIL]', line)
    line = CREDIT_CARD_PATTERN.sub('[HIDDEN_CARD]', line)
    return line

def scrub_log(input_stream, output_stream, keywords=None, anonymize=True):
    """
    Reads from input_stream, processes lines, and writes to output_stream.
    :param input_stream: A file-like object for reading (e.g., open('file.log', 'r'), io.StringIO).
    :param output_stream: A file-like object for writing (e.g., open('output.log', 'w'), io.StringIO).
    :param keywords: A list of strings. Only lines containing any of these keywords will be processed.
                     If None or empty, all lines are processed. Case-insensitive.
    :param anonymize: Boolean. If True, sensitive data will be anonymized.
    """
    if keywords:
        keywords = [k.lower() for k in keywords]

    for line in input_stream:
        original_line = line.strip()
        
        # Apply keyword filtering
        if keywords:
            if not any(k in original_line.lower() for k in keywords):
                continue # Skip line if no keyword found

        processed_line = original_line
        if anonymize:
            processed_line = anonymize_line(processed_line)
        
        output_stream.write(processed_line + '\n')

def main():
    parser = argparse.ArgumentParser(
        description="Chronicle Keeper's Log Scrubber: Anonymize and filter log files."
    )
    parser.add_argument(
        'input_file',
        type=str,
        help="Path to the input log file."
    )
    parser.add_argument(
        'output_file',
        type=str,
        help="Path to the output scrubbed log file."
    )
    parser.add_argument(
        '--keywords',
        nargs='*',
        help="Optional. List of keywords to filter log entries. Only lines containing any of these keywords will be processed. Case-insensitive."
    )
    parser.add_argument(
        '--no-anonymize',
        action='store_true',
        help="Do not anonymize sensitive data. Only filter if keywords are provided."
    )

    args = parser.parse_args()

    try:
        with open(args.input_file, 'r', encoding='utf-8') as infile, \
             open(args.output_file, 'w', encoding='utf-8') as outfile:
            scrub_log(infile, outfile, args.keywords, not args.no_anonymize)
        print(f"Log scrubbed successfully from '{args.input_file}' to '{args.output_file}'.")
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
