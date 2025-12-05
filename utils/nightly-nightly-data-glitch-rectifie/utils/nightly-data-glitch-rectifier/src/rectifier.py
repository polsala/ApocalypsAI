import argparse
import json
import re
import sys

def _trim_whitespace(text):
    """Removes leading and trailing whitespace from a string."""
    return text.strip()

def _normalize_case(text, case_type):
    """Converts string to specified case type."""
    if case_type == "lower":
        return text.lower()
    elif case_type == "upper":
        return text.upper()
    elif case_type == "title":
        return text.title()
    else:
        raise ValueError(f"Unknown case type: {case_type}")

def _simple_replace(text, old_substring, new_substring):
    """Replaces all occurrences of old_substring with new_substring."""
    return text.replace(old_substring, new_substring)

def _regex_replace(text, pattern, replacement):
    """Replaces all matches of a regex pattern with replacement."""
    return re.sub(pattern, replacement, text)

def rectify_string(input_string: str, rules: list) -> str:
    """
    Applies a list of rectification rules to a single string.

    Args:
        input_string: The string to rectify.
        rules: A list of dictionaries, each defining a rectification rule.

    Returns:
        The rectified string.
    """
    current_string = input_string
    for rule in rules:
        rule_type = rule.get("type")
        if rule_type == "trim":
            current_string = _trim_whitespace(current_string)
        elif rule_type in ["lower", "upper", "title"]:
            current_string = _normalize_case(current_string, rule_type)
        elif rule_type == "replace":
            old = rule.get("old")
            new = rule.get("new")
            if old is None or new is None:
                raise ValueError(f"Missing 'old' or 'new' for 'replace' rule: {rule}")
            current_string = _simple_replace(current_string, old, new)
        elif rule_type == "regex_replace":
            pattern = rule.get("pattern")
            replacement = rule.get("replacement")
            if pattern is None or replacement is None:
                raise ValueError(f"Missing 'pattern' or 'replacement' for 'regex_replace' rule: {rule}")
            current_string = _regex_replace(current_string, pattern, replacement)
        else:
            raise ValueError(f"Unknown rectification rule type: {rule_type}")
    return current_string

def main():
    parser = argparse.ArgumentParser(
        description="Rectify data glitches in text files using defined rules."
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        help="Path to the input text file. Reads from stdin if not provided.",
    )
    parser.add_argument(
        "--rules",
        "-r",
        type=str,
        required=True,
        help="Path to a JSON file containing rectification rules.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Path to the output text file. Writes to stdout if not provided.",
    )

    args = parser.parse_args()

    try:
        with open(args.rules, "r", encoding="utf-8") as f:
            rules = json.load(f)
    except FileNotFoundError:
        print(f"Error: Rules file not found at {args.rules}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in rules file at {args.rules}", file=sys.stderr)
        sys.exit(1)

    input_lines = []
    if args.input:
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                input_lines = f.readlines()
        except FileNotFoundError:
            print(f"Error: Input file not found at {args.input}", file=sys.stderr)
            sys.exit(1)
    else:
        input_lines = sys.stdin.readlines()

    output_lines = []
    for line in input_lines:
        try:
            # Remove newline characters for processing, add back later
            processed_line = rectify_string(line.rstrip('\n'), rules)
            output_lines.append(processed_line + '\n')
        except ValueError as e:
            print(f"Error applying rule to line '{line.strip()}': {e}", file=sys.stderr)
            # Decide whether to skip, output original, or exit. For now, output original with error.
            output_lines.append(line) # Keep original if error
            continue # Continue processing other lines

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.writelines(output_lines)
        except IOError as e:
            print(f"Error writing to output file {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        sys.stdout.writelines(output_lines)

if __name__ == "__main__":
    main()
