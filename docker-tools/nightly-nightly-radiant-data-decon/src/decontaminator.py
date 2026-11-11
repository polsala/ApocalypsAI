import os
import sys
import re

def clean_text(text):
    """Applies decontamination rules to a given string."""
    # 1. Remove non-printable ASCII characters (0-31 and 127 are control chars)
    #    Allow common whitespace: tab (9), newline (10), carriage return (13)
    cleaned_text = ''.join(char for char in text if 31 < ord(char) < 127 or ord(char) in [9, 10, 13])

    # 2. Remove 'temporal echoes' (example: repeated timestamps or specific patterns)
    #    This is a simple example; more complex patterns can be added.
    cleaned_text = re.sub(r'\[ECHO\]\s*\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2}\s*\[ECHO\]', '', cleaned_text)
    cleaned_text = re.sub(r'\s*\b(?:ERROR|DEBUG|INFO)\b\s*', ' ', cleaned_text) # Remove common log level noise

    # 3. Normalize whitespace: replace multiple spaces/tabs with single space, trim lines
    cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text) # Replace multiple spaces/tabs with one space
    cleaned_text = '\n'.join(line.strip() for line in cleaned_text.splitlines()) # Trim each line
    cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text) # Remove excessive empty lines
    cleaned_text = cleaned_text.strip() # Trim leading/trailing newlines/spaces from the whole text

    return cleaned_text

def decontaminate_files(input_dir, output_dir):
    """Processes all text files in input_dir and writes cleaned versions to output_dir."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        input_filepath = os.path.join(input_dir, filename)
        output_filepath = os.path.join(output_dir, filename) # Keep original filename

        if os.path.isfile(input_filepath):
            try:
                with open(input_filepath, 'r', encoding='utf-8', errors='ignore') as f_in:
                    content = f_in.read()
                cleaned_content = clean_text(content)
                with open(output_filepath, 'w', encoding='utf-8') as f_out:
                    f_out.write(cleaned_content)
                print(f"Decontaminated '{filename}'")
            except Exception as e:
                print(f"Error processing '{filename}': {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python decontaminator.py <input_directory> <output_directory>")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]

    decontaminate_files(input_directory, output_directory)
