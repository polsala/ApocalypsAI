import os
import re
import argparse
from collections import defaultdict

def collect_dust(scan_dirs, custom_patterns=None):
    """
    Scans specified directories for .log files and collects counts of defined patterns.

    Args:
        scan_dirs (list): A list of directory paths to scan.
        custom_patterns (dict, optional): A dictionary of {name: regex_string} for custom patterns.
                                         If None, default patterns are used.

    Returns:
        dict: A dictionary containing the scan results.
              Example: {'file_results': {'/path/to/log.log': {'ERROR': 5, 'WARNING': 2}}, 'summary': {'ERROR': 7, 'WARNING': 3}, ...}
    """
    default_patterns = {
        'ERROR': r'ERROR|Exception|Failed',
        'WARNING': r'WARN|Warning',
        'CRITICAL': r'CRITICAL|Fatal'
    }

    patterns_to_use = {}
    if custom_patterns:
        for name, regex_str in custom_patterns.items():
            try:
                patterns_to_use[name] = re.compile(regex_str)
            except re.error as e:
                print(f"Error compiling regex for pattern '{name}': {e}. Skipping this pattern.")
    else:
        for name, regex_str in default_patterns.items():
            patterns_to_use[name] = re.compile(regex_str)

    results = defaultdict(lambda: defaultdict(int))
    total_files_scanned = 0
    overall_pattern_counts = defaultdict(int)

    print("--- Cosmic Dust Collection Report ---")
    print(f"\nScanning directories: {scan_dirs}")

    for scan_dir in scan_dirs:
        if not os.path.isdir(scan_dir):
            print(f"Warning: Directory not found: {scan_dir}. Skipping.")
            continue

        for root, _, files in os.walk(scan_dir):
            for file in files:
                if file.endswith('.log'):
                    file_path = os.path.join(root, file)
                    total_files_scanned += 1
                    print(f"\nFile: {file_path}")
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            for pattern_name, compiled_regex in patterns_to_use.items():
                                count = len(compiled_regex.findall(content))
                                results[file_path][pattern_name] = count
                                overall_pattern_counts[pattern_name] += count
                                print(f"  {pattern_name}: {count} occurrences")
                    except IOError as e:
                        print(f"  Error reading file {file_path}: {e}")

    print("\n--- Summary ---")
    print(f"Total files scanned: {total_files_scanned}")
    total_issues_found = sum(overall_pattern_counts.values())
    print(f"Total issues found: {total_issues_found}")

    print("\nOverall Pattern Counts:")
    for name, count in overall_pattern_counts.items():
        print(f"  {name}: {count}")

    print("\nDust collection complete. Keep your systems sparkling!")

    return {'file_results': dict(results), 'summary': dict(overall_pattern_counts), 'total_files_scanned': total_files_scanned, 'total_issues_found': total_issues_found}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collects cosmic dust (errors/warnings) from log files.')
    parser.add_argument('--dirs', nargs='+', required=True, help='One or more directories to scan for .log files.')
    parser.add_argument('--patterns', nargs='*', help='Custom patterns (NAME=REGEX). Overrides default patterns.')

    args = parser.parse_args()

    custom_patterns_dict = None
    if args.patterns:
        custom_patterns_dict = {}
        for p in args.patterns:
            if '=' in p:
                name, regex_str = p.split('=', 1)
                custom_patterns_dict[name] = regex_str
            else:
                print(f"Warning: Invalid pattern format '{p}'. Expected NAME=REGEX. Skipping.")

    collect_dust(args.dirs, custom_patterns_dict)
