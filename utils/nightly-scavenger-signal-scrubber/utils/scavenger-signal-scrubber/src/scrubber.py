import argparse
import re
import os

def scrub_file(
    input_filepath: str,
    output_filepath: str,
    remove_duplicates: bool = True,
    remove_empty_lines: bool = True,
    strip_whitespace: bool = True,
    custom_patterns_to_remove: list[str] | None = None
) -> None:
    """
    Cleans a text file by removing empty lines, duplicate lines,
    stripping whitespace, and removing lines matching custom regex patterns.

    Args:
        input_filepath: Path to the input file.
        output_filepath: Path to the output file where cleaned content will be written.
        remove_duplicates: If True, remove duplicate lines.
        remove_empty_lines: If True, remove lines that are empty or contain only whitespace.
        strip_whitespace: If True, strip leading/trailing whitespace and normalize
                          internal whitespace (multiple spaces to single space).
        custom_patterns_to_remove: A list of regex patterns (strings) to remove.
                                   Any line matching any of these patterns will be removed.
    """
    if not os.path.exists(input_filepath):
        raise FileNotFoundError(f"Input file not found: {input_filepath}")

    cleaned_lines = []
    seen_lines = set()
    compiled_patterns = [re.compile(p) for p in (custom_patterns_to_remove or [])]

    with open(input_filepath, 'r', encoding='utf-8') as infile:
        for line in infile:
            original_line = line.strip() # for pattern matching before full strip

            # Check for custom patterns first
            if any(pattern.search(original_line) for pattern in compiled_patterns):
                continue

            processed_line = line

            if strip_whitespace:
                processed_line = processed_line.strip()
                # Normalize internal whitespace: replace multiple spaces/tabs with a single space
                processed_line = re.sub(r'\s+', ' ', processed_line)

            if remove_empty_lines and not processed_line:
                continue

            if remove_duplicates:
                if processed_line in seen_lines:
                    continue
                seen_lines.add(processed_line)

            cleaned_lines.append(processed_line)

    with open(output_filepath, 'w', encoding='utf-8') as outfile:
        for line in cleaned_lines:
            outfile.write(line + '\n')

def main():
    parser = argparse.ArgumentParser(
        description="Scavenger's Satellite Signal Scrubber: Clean up text files."
    )
    parser.add_argument("input_file", help="Path to the input file.")
    parser.add_argument("output_file", help="Path to the output file.")
    parser.add_argument(
        "-d", "--no-duplicates", action="store_false", dest="remove_duplicates",
        help="Do not remove duplicate lines."
    )
    parser.add_argument(
        "-e", "--no-empty", action="store_false", dest="remove_empty_lines",
        help="Do not remove empty lines."
    )
    parser.add_argument(
        "-s", "--no-strip", action="store_false", dest="strip_whitespace",
        help="Do not strip leading/trailing whitespace or normalize internal whitespace."
    )
    parser.add_argument(
        "-p", "--pattern", action="append", dest="custom_patterns",
        help="Add a custom regex pattern to remove lines matching it. Can be specified multiple times."
    )

    args = parser.parse_args()

    try:
        scrub_file(
            args.input_file,
            args.output_file,
            remove_duplicates=args.remove_duplicates,
            remove_empty_lines=args.remove_empty_lines,
            strip_whitespace=args.strip_whitespace,
            custom_patterns_to_remove=args.custom_patterns
        )
        print(f"File '{args.input_file}' successfully scrubbed to '{args.output_file}'.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
