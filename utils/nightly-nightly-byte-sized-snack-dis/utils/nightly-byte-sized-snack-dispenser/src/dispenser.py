import argparse
import collections
import random
import re
import sys

def get_first_n_lines(file_path: str, n: int):
    """Yields the first N lines from a file."""
    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            if i >= n:
                break
            yield line

def get_last_n_lines(file_path: str, n: int):
    """Yields the last N lines from a file."""
    # Use a deque for efficient storage of the last N lines
    last_lines = collections.deque(maxlen=n)
    with open(file_path, 'r') as f:
        for line in f:
            last_lines.append(line)
    yield from last_lines

def get_random_n_lines(file_path: str, n: int):
    """Yields N random lines from a file."""
    all_lines = []
    with open(file_path, 'r') as f:
        for line in f:
            all_lines.append(line)
    
    if not all_lines:
        return # No lines to sample

    # Ensure n does not exceed the total number of lines
    actual_n = min(n, len(all_lines))
    
    # Mock rationale: random.sample is deterministic for testing if seed is set,
    # but for true randomness, we don't set a seed here.
    # Tests will mock random.sample directly.
    sampled_lines = random.sample(all_lines, actual_n)
    yield from sampled_lines

def get_grep_lines(file_path: str, pattern: str):
    """Yields lines from a file that match a given pattern."""
    compiled_pattern = re.compile(pattern)
    with open(file_path, 'r') as f:
        for line in f:
            if compiled_pattern.search(line):
                yield line

def main():
    parser = argparse.ArgumentParser(
        description="Extracts a 'snack-sized' sample from large text files."
    )
    parser.add_argument("file_path", help="Path to the input file.")
    parser.add_argument(
        "--method",
        choices=["first", "last", "random", "grep"],
        required=True,
        help="The sampling method to use."
    )
    parser.add_argument(
        "--count",
        type=int,
        help="(Required for first, last, random methods) The number of lines to extract."
    )
    parser.add_argument(
        "--pattern",
        help="(Required for grep method) The string or regex pattern to search for."
    )
    parser.add_argument(
        "--output",
        help="Path to save the extracted lines. If not provided, output goes to stdout."
    )

    args = parser.parse_args()

    if args.method in ["first", "last", "random"] and args.count is None:
        parser.error(f"--count is required for method '{args.method}'.")
    if args.method == "grep" and args.pattern is None:
        parser.error("--pattern is required for method 'grep'.")
    if args.method not in ["first", "last", "random"] and args.count is not None:
        parser.error(f"--count is only applicable for 'first', 'last', 'random' methods.")
    if args.method != "grep" and args.pattern is not None:
        parser.error(f"--pattern is only applicable for 'grep' method.")

    lines_to_output = []
    try:
        if args.method == "first":
            lines_to_output = list(get_first_n_lines(args.file_path, args.count))
        elif args.method == "last":
            lines_to_output = list(get_last_n_lines(args.file_path, args.count))
        elif args.method == "random":
            lines_to_output = list(get_random_n_lines(args.file_path, args.count))
        elif args.method == "grep":
            lines_to_output = list(get_grep_lines(args.file_path, args.pattern))
    except FileNotFoundError:
        print(f"Error: File not found at '{args.file_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        try:
            with open(args.output, 'w') as outfile:
                for line in lines_to_output:
                    outfile.write(line)
            print(f"Extracted lines saved to '{args.output}'")
        except IOError as e:
            print(f"Error writing to output file '{args.output}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        for line in lines_to_output:
            sys.stdout.write(line)

if __name__ == "__main__":
    main()
