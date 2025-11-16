import argparse
import re
from typing import Optional, List

def clean_text(text_content: str, 
               remove_empty_lines: bool = True, 
               trim_whitespace: bool = True, 
               collapse_spaces: bool = False, 
               remove_pattern: Optional[str] = None) -> str:
    """
    Cleans a given text string based on specified options.

    Args:
        text_content: The input text as a single string.
        remove_empty_lines: If True, removes lines that are empty after trimming.
        trim_whitespace: If True, removes leading/trailing whitespace from each line.
        collapse_spaces: If True, replaces multiple internal spaces with a single space.
        remove_pattern: A regex string. Lines fully matching this pattern will be removed.

    Returns:
        The cleaned text as a single string.
    """
    lines = text_content.splitlines()
    cleaned_lines: List[str] = []

    compiled_pattern = re.compile(remove_pattern) if remove_pattern else None

    for line in lines:
        original_line = line # Store original line for pattern matching

        if trim_whitespace:
            line = line.strip()
        
        if collapse_spaces:
            line = re.sub(r'\s+', ' ', line).strip() # strip again in case collapse created new leading/trailing space

        if remove_empty_lines and not line:
            continue

        if compiled_pattern and compiled_pattern.fullmatch(original_line):
            continue

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Scrub messy text files to purify signals."
    )
    parser.add_argument("input_file", help="Path to the input text file.")
    parser.add_argument("output_file", nargs="?", help="Optional path to the output text file. If not provided, output to stdout.")
    parser.add_argument("--no-empty-lines", action="store_true", help="Do not remove empty lines.")
    parser.add_argument("--no-trim-whitespace", action="store_true", help="Do not trim leading/trailing whitespace.")
    parser.add_argument("--collapse-spaces", action="store_true", help="Replace multiple internal spaces with a single space.")
    parser.add_argument("--remove-pattern", type=str, help="Regex pattern to remove lines that fully match it.")

    args = parser.parse_args()

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
        exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}")
        exit(1)

    cleaned_content = clean_text(
        content,
        remove_empty_lines=not args.no_empty_lines,
        trim_whitespace=not args.no_trim_whitespace,
        collapse_spaces=args.collapse_spaces,
        remove_pattern=args.remove_pattern
    )

    if args.output_file:
        try:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            print(f"Scrubbed content written to '{args.output_file}'.")
        except Exception as e:
            print(f"Error writing output file: {e}")
            exit(1)
    else:
        print(cleaned_content)

if __name__ == "__main__":
    main()
