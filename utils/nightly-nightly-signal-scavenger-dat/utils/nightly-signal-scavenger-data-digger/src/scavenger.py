import re
import argparse
import sys

def extract_patterns(text_content, pattern_type=None, custom_regex=None):
    """
    Extracts patterns from text content based on predefined types or a custom regex.
    """
    patterns = {
        "url": r"https?://[^\s/$.?#].[^\s]*",
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        # Add more common patterns if desired
    }

    if custom_regex:
        regex = custom_regex
    elif pattern_type and pattern_type in patterns:
        regex = patterns[pattern_type]
    else:
        raise ValueError(f"Invalid pattern type '{pattern_type}' or no custom regex provided.")

    return re.findall(regex, text_content)

def main():
    parser = argparse.ArgumentParser(
        description="Signal Scavenger's Data Digger: Extract specific data patterns from text files."
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="+",
        help="One or more text files to process."
    )
    parser.add_argument(
        "-t", "--type",
        choices=["url", "email"],
        help="Predefined pattern type to extract (e.g., 'url', 'email')."
    )
    parser.add_argument(
        "-r", "--regex",
        help="Custom regular expression to use for extraction. Overrides --type."
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file to write extracted data. If not specified, prints to stdout."
    )

    args = parser.parse_args()

    if not args.type and not args.regex:
        parser.error("Either --type or --regex must be specified.")

    all_extracted_data = []

    for file_path in args.files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            extracted = extract_patterns(content, args.type, args.regex)
            if extracted:
                all_extracted_data.extend(extracted)

        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error processing '{file_path}': {e}", file=sys.stderr)
            sys.exit(1)

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                for item in all_extracted_data:
                    f.write(item + '\n')
            print(f"Extracted data written to '{args.output}'")
        except Exception as e:
            print(f"Error writing to output file '{args.output}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        if all_extracted_data:
            for item in all_extracted_data:
                print(item)
        else:
            print("No patterns found across specified files.")

if __name__ == "__main__":
    main()
