import os
import argparse

def generate_scrapbook(input_dir: str, output_file: str):
    """
    Compiles text files from an input directory into a single scrapbook file.
    Files are sorted by filename (lexicographically) and their content is
    concatenated with headers into the output file.
    """
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' not found.")
        return

    try:
        # Get all .txt files, sorted lexicographically by filename
        note_files = sorted([
            f for f in os.listdir(input_dir)
            if os.path.isfile(os.path.join(input_dir, f)) and f.endswith('.txt')
        ])

        if not note_files:
            print(f"No .txt files found in '{input_dir}'. Nothing to compile.")
            return

        with open(output_file, 'w', encoding='utf-8') as outfile:
            for filename in note_files:
                filepath = os.path.join(input_dir, filename)
                outfile.write(f"--- Entry from {filename} ---\n")
                try:
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(content.strip())
                        outfile.write("\n\n") # Add two newlines for separation
                except IOError as e:
                    print(f"Warning: Could not read file '{filename}': {e}")
                    outfile.write(f"[Error reading file: {e}]\n\n")
        print(f"Scrapbook successfully generated at '{output_file}'.")

    except IOError as e:
        print(f"Error writing to output file '{output_file}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Compile scattered text notes into a chronological scrapbook journal."
    )
    parser.add_argument(
        '--input-dir', 
        type=str, 
        required=True, 
        help="The directory containing your .txt notes."
    )
    parser.add_argument(
        '--output-file', 
        type=str, 
        required=True, 
        help="The path to the output .txt file where the scrapbook will be generated."
    )
    args = parser.parse_args()

    generate_scrapbook(args.input_dir, args.output_file)
