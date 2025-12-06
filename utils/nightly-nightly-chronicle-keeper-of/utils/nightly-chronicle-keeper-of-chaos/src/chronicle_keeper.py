import os
import sys

def format_size(size_bytes):
    """Formats a size in bytes into a human-readable string."""
    if size_bytes == 0:
        return "0 Bytes"
    size_name = ("Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(os.floor(os.log(size_bytes, 1024)))
    p = os.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def generate_chronicle(directory_path, top_n=5):
    """Generates a Markdown summary of the given directory."""
    if not os.path.isdir(directory_path):
        return f"# Error: Directory not found at {directory_path}"

    total_files = 0
    total_dirs = 0
    total_size = 0
    largest_files = []  # List of (size, path)

    for root, dirs, files in os.walk(directory_path):
        total_dirs += len(dirs)
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                total_files += 1
                total_size += size
                largest_files.append((size, file_path))
            except OSError: # Handle cases like broken symlinks or permission issues
                pass
    
    # Sort largest files in descending order
    largest_files.sort(key=lambda x: x[0], reverse=True)
    
    # Prepare Markdown output
    markdown_output = []
    markdown_output.append(f"# Chronicle of {directory_path}")
    markdown_output.append("\n## Summary\n")
    markdown_output.append(f"- **Total Directories:** {total_dirs}")
    markdown_output.append(f"- **Total Files:** {total_files}")
    markdown_output.append(f"- **Total Size:** {format_size(total_size)}")

    if largest_files:
        markdown_output.append(f"\n## Largest Files (Top {top_n})\n")
        for size, path in largest_files[:top_n]:
            relative_path = os.path.relpath(path, directory_path)
            markdown_output.append(f"- `{relative_path}`: {format_size(size)}")
    else:
        markdown_output.append("\n## Largest Files\n")
        markdown_output.append("No files found in this directory.")

    return "\n".join(markdown_output)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chronicle_keeper.py <directory_path>")
        sys.exit(1)
    
    target_directory = sys.argv[1]
    print(generate_chronicle(target_directory))
