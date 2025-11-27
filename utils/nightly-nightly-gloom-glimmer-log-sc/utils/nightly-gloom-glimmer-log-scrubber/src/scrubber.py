import argparse
import sys

def scrub_log_content(log_content: str, glimmers: list[str], glooms: list[str]) -> list[str]:
    """
    Processes log content, filtering out 'gloom' lines and highlighting 'glimmer' lines.

    Args:
        log_content: The entire log content as a single string.
        glimmers: A list of keywords/phrases to highlight.
        glooms: A list of keywords/phrases to filter out.

    Returns:
        A list of processed log lines.
    """
    processed_lines = []
    for line in log_content.splitlines():
        # Check for gloom first (filter out entirely)
        if any(gloom_keyword in line for gloom_keyword in glooms):
            continue

        # Check for glimmers (highlight)
        if any(glimmer_keyword in line for glimmer_keyword in glimmers):
            processed_lines.append(f"[GLIMMER] {line}")
        else:
            processed_lines.append(line)

    return processed_lines

def main():
    parser = argparse.ArgumentParser(
        description="Gloom-Glimmer Log Scrubber: Filter and highlight log entries."
    )
    parser.add_argument(
        "input_log_file",
        type=str,
        help="Path to the log file to scrub."
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to the file where the scrubbed log will be written. If not provided, output goes to stdout."
    )
    parser.add_argument(
        "--glimmers",
        nargs='*', # 0 or more arguments
        default=[],
        help="Space-separated list of keywords to highlight. Lines containing any will be prefixed with [GLIMMER]."
    )
    parser.add_argument(
        "--glooms",
        nargs='*', # 0 or more arguments
        default=[],
        help="Space-separated list of keywords to filter out. Lines containing any will be removed."
    )

    args = parser.parse_args()

    try:
        with open(args.input_log_file, 'r') as f:
            log_content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_log_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)

    processed_lines = scrub_log_content(log_content, args.glimmers, args.glooms)

    if args.output:
        try:
            with open(args.output, 'w') as f:
                for line in processed_lines:
                    f.write(line + '\n')
            print(f"Scrubbed log written to '{args.output}'.")
        except Exception as e:
            print(f"Error writing to output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        for line in processed_lines:
            print(line)

if __name__ == "__main__":
    main()
