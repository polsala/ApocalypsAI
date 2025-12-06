import os
import argparse
from collections import defaultdict
import fnmatch

def count_keywords_in_file(filepath, keywords):
    """
    Counts occurrences of specified keywords in a given file.
    Keywords are searched case-insensitively.
    """
    keyword_counts = defaultdict(int)
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                for keyword in keywords:
                    if keyword.lower() in line.lower():
                        keyword_counts[keyword] += 1
    except FileNotFoundError:
        print(f"Warning: File not found: {filepath}")
    except Exception as e:
        print(f"Error processing file {filepath}: {e}")
    return dict(keyword_counts)

def scan_directory_for_logs(directory, keywords, file_pattern='*.log'):
    """
    Scans a directory for files matching the pattern and counts keyword occurrences.
    Returns a dictionary with file-specific counts and overall totals.
    """
    if not os.path.isdir(directory):
        raise ValueError(f"Directory not found: {directory}")

    results = {
        'files': {},
        'overall_totals': defaultdict(int)
    }

    for root, _, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, file_pattern):
            filepath = os.path.join(root, filename)
            file_keyword_counts = count_keywords_in_file(filepath, keywords)
            if file_keyword_counts:
                results['files'][filepath] = file_keyword_counts
                for keyword, count in file_keyword_counts.items():
                    results['overall_totals'][keyword] += count

    results['overall_totals'] = dict(results['overall_totals'])
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Scans log files for keywords and generates a summary report."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The path to the directory containing log files."
    )
    parser.add_argument(
        "--keywords",
        nargs='+',
        default=['ERROR', 'WARNING', 'INFO'],
        help="Space-separated list of keywords to search for (default: ERROR WARNING INFO)"
    )
    parser.add_argument(
        "--file-pattern",
        type=str,
        default='*.log',
        help="Glob-style pattern to filter files (default: *.log)"
    )

    args = parser.parse_args()

    try:
        summary_data = scan_directory_for_logs(
            args.directory, args.keywords, args.file_pattern
        )

        print(f"Salvage Log Summary Report for: {args.directory}")
        print(f"File Pattern: {args.file_pattern}")
        print(f"Keywords: {', '.join(args.keywords)}\n")
        print("--------------------------------------------------")

        if not summary_data['files']:
            print("No matching files found or no keywords detected.")
        else:
            for filepath, counts in summary_data['files'].items():
                print(f"File: {filepath}")
                for keyword in args.keywords:
                    print(f"  {keyword}: {counts.get(keyword, 0)}")
                print()

            print("--------------------------------------------------")
            print("Overall Totals:")
            for keyword in args.keywords:
                print(f"  {keyword}: {summary_data['overall_totals'].get(keyword, 0)}")
            print("--------------------------------------------------")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
