import argparse
import os
import shutil

def clean_config_content(content_lines, comment_chars):
    """
    Cleans a list of configuration lines by removing full-line comments and empty lines.
    Inline comments are preserved.
    """
    cleaned_lines = []
    for line in content_lines:
        stripped_line = line.strip()
        
        # Check if the line is empty after stripping
        if not stripped_line:
            continue
        
        # Check if the line starts with any of the specified comment characters
        is_full_line_comment = False
        for char in comment_chars:
            if stripped_line.startswith(char):
                is_full_line_comment = True
                break
        
        if is_full_line_comment:
            continue
            
        cleaned_lines.append(line)
            
    return cleaned_lines

def main():
    parser = argparse.ArgumentParser(
        description="Excavates and purifies configuration files by removing digital 'fossils'."
    )
    parser.add_argument(
        "input_file_path", 
        type=str, 
        help="The path to the configuration file to be cleaned."
    )
    parser.add_argument(
        "--output", 
        type=str, 
        help="(Optional) Specify an output file path. If not provided, the input file will be overwritten."
    )
    parser.add_argument(
        "--backup", 
        action="store_true", 
        help="(Optional) If provided, a backup of the original file will be created with a .bak extension."
    )
    parser.add_argument(
        "--comment-chars", 
        nargs='*', 
        default=['#', ';'], 
        help="(Optional) Space-separated list of characters to treat as comment prefixes. Defaults to '#' and ';'."
    )

    args = parser.parse_args()

    input_path = args.input_file_path
    output_path = args.output if args.output else input_path
    comment_chars = args.comment_chars

    if not os.path.exists(input_path):
        print(f"Error: Input file not found at '{input_path}'")
        exit(1)

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            original_content_lines = f.readlines()

        cleaned_content_lines = clean_config_content(original_content_lines, comment_chars)
        
        if args.backup and input_path == output_path:
            backup_path = input_path + '.bak'
            shutil.copyfile(input_path, backup_path)
            print(f"Backup created at '{backup_path}'")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_content_lines)
        
        print(f"Configuration file cleaned and saved to '{output_path}'.")

    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
