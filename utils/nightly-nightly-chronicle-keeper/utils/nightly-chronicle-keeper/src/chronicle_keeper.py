import os
import re
import argparse
from datetime import datetime

def extract_date_from_filename(filename):
    """
    Extracts a date (YYYY-MM-DD) from a filename.
    Prioritizes explicit YYYY-MM-DD patterns.
    """
    match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        try:
            return datetime.strptime(match.group(1), '%Y-%m-%d')
        except ValueError:
            pass
    return None

def get_file_date(filepath):
    """
    Attempts to get a date from the filename, falls back to modification time.
    Returns a tuple (datetime_object, source_string).
    """
    filename = os.path.basename(filepath)
    date_from_name = extract_date_from_filename(filename)
    if date_from_name:
        return date_from_name, date_from_name.strftime('%Y-%m-%d')
    else:
        # Fallback to modification time
        mod_timestamp = os.path.getmtime(filepath)
        mod_datetime = datetime.fromtimestamp(mod_timestamp)
        return mod_datetime, mod_datetime.strftime('%Y-%m-%d (modified)')

def create_chronicle(input_dir, output_file):
    """
    Scans input_dir for markdown files, sorts them by date, and
    writes their content to output_file with chronological headers.
    """
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return

    markdown_files = []
    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(input_dir, filename)
            if os.path.isfile(filepath):
                markdown_files.append(filepath)

    if not markdown_files:
        print(f"No markdown files found in '{input_dir}'. Nothing to chronicle.")
        return

    # Collect files with their associated dates
    dated_files = []
    for filepath in markdown_files:
        file_date, date_str = get_file_date(filepath)
        dated_files.append((file_date, date_str, filepath))

    # Sort files chronologically
    dated_files.sort(key=lambda x: x[0])

    print(f"Creating chronicle from {len(dated_files)} markdown files...")

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("# ApocalypsAI Chronicle\n\n")
        for _, date_str, filepath in dated_files:
            outfile.write(f"## Chronicle Entry: {date_str}\n")
            try:
                with open(filepath, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(content.strip()) # Remove leading/trailing whitespace from file content
                    outfile.write("\n\n") # Ensure separation between entries
            except Exception as e:
                outfile.write(f"**Error reading file '{os.path.basename(filepath)}': {e}**\n\n")
            print(f"  - Added '{os.path.basename(filepath)}' ({date_str})")

    print(f"Chronicle successfully created at '{output_file}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Consolidate markdown files into a chronological chronicle."
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        help="The directory containing markdown files to consolidate."
    )
    parser.add_argument(
        "--output-file",
        required=True,
        help="The path to the output markdown file for the chronicle."
    )
    args = parser.parse_args()

    create_chronicle(args.input_dir, args.output_file)
