import argparse
import sys
import re

def remove_empty_lines(lines):
    """Removes lines that are entirely empty or contain only whitespace."""
    return [line for line in lines if line.strip()]

def trim_whitespace(lines):
    """Removes leading/trailing whitespace from each line."""
    return [line.strip() for line in lines]

def remove_duplicate_lines(lines):
    """Removes duplicate lines, preserving the order of first appearance."""
    seen = set()
    result = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            result.append(line)
    return result

def remove_lines_by_pattern(lines, pattern):
    """Removes lines that match a given regex pattern."""
    if not pattern:
        return lines
    compiled_pattern = re.compile(pattern)
    return [line for line in lines if not compiled_pattern.search(line)]

def convert_to_case(lines, case_type):
    """Converts lines to a specified case (lower, upper, title)."""
    if case_type == 'lower':
        return [line.lower() for line in lines]
    elif case_type == 'upper':
        return [line.upper() for line in lines]
    elif case_type == 'title':
        return [line.title() for line in lines]
    return lines # No change if case_type is None or invalid

def decruft_data(input_data, trim=True, empty_lines=True, duplicates=True,
                 pattern=None, case=None):
    """
    Performs a series of data cleaning operations on a list of lines.
    """
    lines = input_data.splitlines()

    if trim:
        lines = trim_whitespace(lines)
    if empty_lines:
        lines = remove_empty_lines(lines)
    if duplicates:
        lines = remove_duplicate_lines(lines)
    if pattern:
        lines = remove_lines_by_pattern(lines, pattern)
    if case:
        lines = convert_to_case(lines, case)

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Data De-Crufter: Purge digital detritus and streamline textual data."
    )
    parser.add_argument(
        "input_file", nargs="?", type=str,
        help="Path to the input file. If omitted, reads from stdin."
    )
    parser.add_argument(
        "-o", "--output-file", type=str,
        help="Path to the output file. If omitted, writes to stdout."
    )
    parser.add_argument(
        "--no-trim", action="store_false", dest="trim",
        help="Do not remove leading/trailing whitespace from lines."
    )
    parser.add_argument(
        "--no-empty-lines", action="store_false", dest="empty_lines",
        help="Do not remove empty lines."
    )
    parser.add_argument(
        "--no-duplicates", action="store_false", dest="duplicates",
        help="Do not remove duplicate lines."
    )
    parser.add_argument(
        "-p", "--pattern", type=str,
        help="Regex pattern to remove lines matching it."
    )
    parser.add_argument(
        "-c", "--case", choices=['lower', 'upper', 'title'],
        help="Convert text to specified case (lower, upper, title)."
    )

    args = parser.parse_args()

    input_data = ""
    if args.input_file:
        try:
            with open(args.input_file, 'r', encoding='utf-8') as f:
                input_data = f.read()
        except FileNotFoundError:
            print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading input file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        input_data = sys.stdin.read()

    output_data = decruft_data(
        input_data,
        trim=args.trim,
        empty_lines=args.empty_lines,
        duplicates=args.duplicates,
        pattern=args.pattern,
        case=args.case
    )

    if args.output_file:
        try:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(output_data)
        except Exception as e:
            print(f"Error writing to output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        sys.stdout.write(output_data)

if __name__ == "__main__":
    main()
