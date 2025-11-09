import os
import re
import argparse
import json

def find_echoes(directory, keywords, file_extensions):
    """
    Scans files in the given directory for specified keywords.

    Args:
        directory (str): The root directory to scan.
        keywords (list): A list of strings to search for (e.g., ['TODO', 'FIXME']).
        file_extensions (list): A list of file extensions to include (e.g., ['.py', '.js']).

    Returns:
        list: A list of dictionaries, each representing an 'echo' found.
              Each dictionary contains 'file_path', 'line_number', 'line_content', 'keyword'.
    """
    echoes = []
    # Create a regex pattern that matches any of the keywords, case-insensitively, as whole words.
    # re.escape is used to handle special characters in keywords.
    keyword_pattern = re.compile(r'\b(' + '|'.join(re.escape(k) for k in keywords) + r')\b', re.IGNORECASE)

    for root, _, files in os.walk(directory):
        for file_name in files:
            # Check if the file has one of the specified extensions
            if any(file_name.endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line_content in enumerate(f, 1):
                            match = keyword_pattern.search(line_content)
                            if match:
                                echoes.append({
                                    'file_path': file_path,
                                    'line_number': line_num,
                                    'line_content': line_content.strip(),
                                    'keyword': match.group(1) # The actual matched keyword (preserving its case)
                                })
                except Exception: # Catch any file reading errors (e.g., permissions, encoding)
                    pass # Silently skip unreadable files to ensure robustness

    return echoes

def main():
    parser = argparse.ArgumentParser(
        description="Temporal Echo Locator: Scans files for forgotten tasks and code cruft."
    )
    parser.add_argument(
        'directory',
        nargs='?', # Makes the argument optional
        default='.',
        help="The root directory to scan (default: current directory)."
    )
    parser.add_argument(
        '--keywords',
        nargs='*', # Allows zero or more arguments
        default=['TODO', 'FIXME', 'HACK', 'BUG'],
        help="Space-separated list of keywords to search for (default: TODO FIXME HACK BUG)."
    )
    parser.add_argument(
        '--extensions',
        nargs='*', # Allows zero or more arguments
        default=['.py', '.js', '.ts', '.java', '.c', '.cpp', '.h', '.hpp', '.go', '.rs', '.md', '.txt', '.sh', '.yaml', '.yml'],
        help="Space-separated list of file extensions to include (default: common code/text files).
              Example: .py .js .md"
    )

    args = parser.parse_args()

    echoes = find_echoes(args.directory, args.keywords, args.extensions)

    print(json.dumps(echoes, indent=2))

if __name__ == '__main__':
    main()
