import os
import sys
import datetime

def is_comment_line(line, extension):
    line = line.strip()
    if not line:
        return False
    
    # Common single-line comment markers (simple heuristic)
    if extension == '.py' or extension == '.sh':
        return line.startswith('#')
    elif extension in ('.js', '.c', '.cpp', '.java', '.go', '.css'):
        return line.startswith('//') or line.startswith('/*')
    elif extension in ('.html', '.xml'):
        # Simple check for single-line HTML/XML comments
        return line.startswith('<!--') and line.endswith('-->')
    elif extension == '.yml':
        return line.startswith('#')
    elif extension == '.md':
        # Markdown doesn't have a universal comment syntax, treat as code/text
        return False
    return False

def analyze_directory(path, ancient_threshold_days=365):
    if not os.path.isdir(path):
        print(f"Error: Directory not found at '{path}'")
        sys.exit(1)

    total_files = 0
    total_lines = 0
    total_comment_lines = 0
    ancient_files = []
    file_type_summary = {}

    now = datetime.datetime.now()
    ancient_threshold_date = now - datetime.timedelta(days=ancient_threshold_days)

    supported_extensions = (
        '.py', '.js', '.md', '.sh', '.yml', '.json', '.txt', '.xml', '.html', '.css', '.go', '.java', '.c', '.cpp', '.h'
    )

    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file).lower()

            if ext not in supported_extensions:
                continue

            total_files += 1
            file_type_summary.setdefault(ext, {'files': 0, 'lines': 0, 'comments': 0})
            file_type_summary[ext]['files'] += 1

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    file_lines = len(lines)
                    file_comment_lines = 0

                    for line in lines:
                        if is_comment_line(line, ext):
                            file_comment_lines += 1
                    
                    total_lines += file_lines
                    total_comment_lines += file_comment_lines
                    file_type_summary[ext]['lines'] += file_lines
                    file_type_summary[ext]['comments'] += file_comment_lines

                # Check for ancient files
                mtime_timestamp = os.path.getmtime(file_path)
                mtime_datetime = datetime.datetime.fromtimestamp(mtime_timestamp)
                if mtime_datetime < ancient_threshold_date:
                    ancient_files.append((file_path, mtime_datetime.strftime('%Y-%m-%d')))

            except Exception as e:
                print(f"Warning: Could not process '{file_path}': {e}")

    print("\n--- Chronicle Keeper Report ---")
    print(f"Scanned Directory: {path}")
    print(f"Total Files Processed: {total_files}")
    print(f"Total Lines of Code/Text: {total_lines}")
    print(f"Total Comment Lines: {total_comment_lines}")
    print("\n--- Breakdown by File Type ---")
    for ext, data in sorted(file_type_summary.items()):
        print(f"  {ext.ljust(5)}: {data['files']} files, {data['lines']} lines, {data['comments']} comments")

    print("\n--- Ancient Scrolls (Files not modified in the last {} days) ---".format(ancient_threshold_days))
    if ancient_files:
        for af_path, af_date in sorted(ancient_files):
            print(f"  - {af_path} (Last modified: {af_date})")
    else:
        print("  No ancient scrolls found. Your code is fresh!")
    print("-------------------------------")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python src/chronicle_keeper.py <path_to_directory>")
        sys.exit(1)
    
    target_path = sys.argv[1]
    analyze_directory(target_path)
