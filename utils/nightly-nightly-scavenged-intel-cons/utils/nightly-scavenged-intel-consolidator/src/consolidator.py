import os
import sys

def consolidate_intel(directory_path):
    """
    Scans a directory for .txt files, extracts intel (TIP, LOCATION, WARNING),
    de-duplicates, and prints a consolidated report.
    """
    intel_categories = {
        "TIPS": set(),
        "LOCATIONS": set(),
        "WARNINGS": set()
    }

    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found at '{directory_path}'", file=sys.stderr)
        return

    found_files = False
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            found_files = True
            filepath = os.path.join(directory_path, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('TIP:'):
                            intel_categories['TIPS'].add(line[4:].strip())
                        elif line.startswith('LOCATION:'):
                            intel_categories['LOCATIONS'].add(line[9:].strip())
                        elif line.startswith('WARNING:'):
                            intel_categories['WARNINGS'].add(line[8:].strip())
            except IOError as e:
                print(f"Warning: Could not read file '{filepath}': {e}", file=sys.stderr)
            except UnicodeDecodeError as e:
                print(f"Warning: Could not decode file '{filepath}' (might not be UTF-8): {e}", file=sys.stderr)

    if not found_files:
        print(f"No .txt files found in '{directory_path}'. Nothing to consolidate.")
        return

    print("\n--- Consolidated Scavenged Intel ---\n")

    for category, intel_set in intel_categories.items():
        print(f"[ {category} ]")
        if intel_set:
            for item in sorted(list(intel_set)):
                print(f"- {item}")
        else:
            print("- No intel found for this category.")
        print()

    print("------------------------------------\n")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python src/consolidator.py <path_to_intel_directory>", file=sys.stderr)
        sys.exit(1)

    target_directory = sys.argv[1]
    consolidate_intel(target_directory)
