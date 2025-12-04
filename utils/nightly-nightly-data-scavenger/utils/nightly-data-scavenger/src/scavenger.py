import os
import re
import json
import argparse

PREDEFINED_PATTERNS = {
    'url': r'https?://(?:www\.)?[a-zA-Z0-9./\-]+(?:/[^\s]*)?',
    'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
}

def scavenge_file(filepath: str, patterns: list[str]) -> list[str]:
    """Scavenges a single file for given regex patterns and returns unique matches."""
    found_matches = set()
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for pattern_str in patterns:
                for match in re.findall(pattern_str, content):
                    found_matches.add(match)
    except IOError:
        # Silently skip unreadable files, as this is a 'scavenging' operation
        pass
    return sorted(list(found_matches))

def scavenge_directory(root_dir: str, patterns: list[str]) -> dict[str, list[str]]:
    """Scavenges a directory recursively for given regex patterns, or a single file."""
    results = {}
    if not os.path.exists(root_dir):
        raise FileNotFoundError(f"Path does not exist: {root_dir}")

    if os.path.isfile(root_dir):
        matches = scavenge_file(root_dir, patterns)
        if matches:
            results[root_dir] = matches
        return results

    if os.path.isdir(root_dir):
        for dirpath, _, filenames in os.walk(root_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                matches = scavenge_file(filepath, patterns)
                if matches:
                    results[filepath] = matches
        return results
    
    # Should not be reached if os.path.exists is true and it's neither file nor dir
    raise ValueError(f"Path is neither a file nor a directory: {root_dir}")

def main():
    parser = argparse.ArgumentParser(
        description="Scavenge files for specific patterns (URLs, emails, custom regex)."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The directory or file path to scavenge."
    )
    parser.add_argument(
        "--patterns",
        nargs='*', # 0 or more arguments
        default=[],
        help="One or more custom regular expressions to search for."
    )
    parser.add_argument(
        "--types",
        nargs='*', # 0 or more arguments
        default=[],
        choices=PREDEFINED_PATTERNS.keys(),
        help="One or more predefined pattern types (e.g., url, email) to search for."
    )

    args = parser.parse_args()

    all_patterns = list(args.patterns)
    for p_type in args.types:
        if p_type in PREDEFINED_PATTERNS:
            all_patterns.append(PREDEFINED_PATTERNS[p_type])

    if not all_patterns:
        print(json.dumps({}))
        return

    try:
        results = scavenge_directory(args.path, all_patterns)
        print(json.dumps(results, indent=2))
    except (FileNotFoundError, ValueError) as e:
        print(json.dumps({"error": str(e)}), file=os.sys.stderr)
        exit(1)
    except Exception as e:
        print(json.dumps({"error": f"An unexpected error occurred: {e}"}), file=os.sys.stderr)
        exit(1)

if __name__ == "__main__":
    main()
