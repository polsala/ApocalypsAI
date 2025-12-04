import os
import re
from datetime import datetime
import sys

DATE_PATTERN = re.compile(r'^(\d{4}-\d{2}-\d{2})')
DATE_FORMAT = '%Y-%m-%d'

def extract_date_from_filename(filename):
    """Extracts a date from the beginning of a filename (e.g., 'YYYY-MM-DD_name.txt')."""
    match = DATE_PATTERN.match(filename)
    if match:
        try:
            return datetime.strptime(match.group(1), DATE_FORMAT)
        except ValueError:
            pass
    return None

def compile_chronicle(input_dir, output_file):
    """Scans a directory for text files, extracts dates, and compiles them chronologically.

    Args:
        input_dir (str): Path to the directory containing text files.
        output_file (str): Path to the output file where the chronicle will be saved.
    """
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' not found.", file=sys.stderr)
        sys.exit(1)

    entries = []
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(input_dir, filename)
            if os.path.isfile(filepath):
                date = extract_date_from_filename(filename)
                if date:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    entries.append({'date': date, 'filename': filename, 'content': content})
                else:
                    print(f"Warning: Could not extract date from '{filename}'. Skipping.", file=sys.stderr)

    entries.sort(key=lambda x: x['date'])

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for entry in entries:
            outfile.write(f"--- {entry['date'].strftime(DATE_FORMAT)} ---\n")
            outfile.write(entry['content'].strip())
            outfile.write("\n\n") # Add an extra newline for separation between entries

    print(f"Chronicle compiled successfully to '{output_file}'.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python src/compiler.py <input_directory> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_dir = sys.argv[1]
    output_file = sys.argv[2]
    compile_chronicle(input_dir, output_file)

if __name__ == '__main__':
    main()
