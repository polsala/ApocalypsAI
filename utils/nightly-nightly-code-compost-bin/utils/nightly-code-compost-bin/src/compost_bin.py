import os
import argparse
import re

def find_compostable_code(root_path, ignore_dirs=None, min_consecutive_comments=3):
    """
    Scans Python files in the given root_path for 'compostable' code patterns.

    Args:
        root_path (str): The root directory to scan.
        ignore_dirs (list): A list of directory names to ignore.
        min_consecutive_comments (int): Minimum number of consecutive comment lines to flag.

    Returns:
        list: A list of dictionaries, each representing a compostable item.
              Each dict contains 'file_path', 'line_number', 'type', 'snippet'.
    """
    compostable_items = []
    ignore_dirs = [d.lower() for d in ignore_dirs] if ignore_dirs else []

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Modify dirnames in-place to prune directories for os.walk
        dirnames[:] = [d for d in dirnames if d.lower() not in ignore_dirs]

        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()

                    consecutive_comment_count = 0
                    comment_block_start_line = -1
                    comment_block_lines = []

                    for i, line in enumerate(lines):
                        line_num = i + 1
                        stripped_line = line.strip()

                        # 1. Detect 'if False:' or 'if 0:' blocks
                        if re.match(r'^\s*if\s+(False|0):', stripped_line):
                            compostable_items.append({
                                'file_path': file_path,
                                'line_number': line_num,
                                'type': 'Dead Code (if False/0:)',
                                'snippet': line.rstrip()
                            })

                        # 2. Detect TODO/FIXME markers
                        if re.search(r'#\s*(TODO|FIXME):', stripped_line, re.IGNORECASE):
                            compostable_items.append({
                                'file_path': file_path,
                                'line_number': line_num,
                                'type': 'TODO/FIXME Marker',
                                'snippet': line.rstrip()
                            })

                        # 3. Detect large blocks of consecutive comments
                        if stripped_line.startswith('#'):
                            if consecutive_comment_count == 0:
                                comment_block_start_line = line_num
                                comment_block_lines = []
                            consecutive_comment_count += 1
                            comment_block_lines.append(line.rstrip())
                        else:
                            if consecutive_comment_count >= min_consecutive_comments:
                                compostable_items.append({
                                    'file_path': file_path,
                                    'line_number': f"{comment_block_start_line}-{comment_block_start_line + consecutive_comment_count - 1}",
                                    'type': 'Consecutive Comments',
                                    'snippet': '\n'.join(comment_block_lines)
                                })
                            consecutive_comment_count = 0
                            comment_block_start_line = -1
                            comment_block_lines = []

                    # Check for a comment block at the end of the file
                    if consecutive_comment_count >= min_consecutive_comments:
                        compostable_items.append({
                            'file_path': file_path,
                            'line_number': f"{comment_block_start_line}-{comment_block_start_line + consecutive_comment_count - 1}",
                            'type': 'Consecutive Comments',
                            'snippet': '\n'.join(comment_block_lines)
                        })

                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

    return compostable_items

def main():
    parser = argparse.ArgumentParser(
        description="Scan Python files for 'compostable' code (dead code, old comments, TODOs)."
    )
    parser.add_argument(
        '--path', 
        type=str, 
        required=True, 
        help='The root directory to start scanning from.'
    )
    parser.add_argument(
        '--ignore', 
        type=str, 
        default='', 
        help='Comma-separated list of directory names to ignore (e.g., venv,build).'
    )

    args = parser.parse_args()
    ignore_dirs = [d.strip() for d in args.ignore.split(',') if d.strip()]

    print(f"Scanning {args.path} for compostable code...")
    items = find_compostable_code(args.path, ignore_dirs)

    if items:
        print(f"\nFound {len(items)} compostable items:\n")
        for item in items:
            print(f"File: {item['file_path']}")
            print(f"  Line {item['line_number']}: Type: {item['type']}")
            print(f"    Snippet: {item['snippet'].replace('\n', '\n             ')}\n")
    else:
        print("\nNo compostable code found. Your codebase is sparkling clean!")

    print("Scan complete. Consider reviewing these items for removal or refactoring.")

if __name__ == '__main__':
    main()
