import os
import datetime
import argparse
import ast

def get_file_age_days(filepath):
    """Returns the age of a file in days."""
    if not os.path.exists(filepath):
        return None
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
    return (datetime.datetime.now() - mtime).days

def count_lines_of_code(filepath):
    """Counts non-empty, non-comment lines of code in a file."""
    if not os.path.exists(filepath):
        return 0
    loc = 0
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                stripped_line = line.strip()
                if stripped_line and not stripped_line.startswith('#'):
                    loc += 1
    except IOError:
        pass # Handle unreadable files gracefully
    return loc

def check_python_docstrings(filepath):
    """Checks for missing docstrings in functions and classes in a Python file."""
    missing_docstrings = []
    if not filepath.endswith('.py') or not os.path.exists(filepath):
        return missing_docstrings

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            tree = ast.parse(f.read(), filename=filepath)

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    missing_docstrings.append(f"  - {node.name} (line {node.lineno})")
    except (SyntaxError, IOError):
        pass # Handle syntax errors or unreadable files gracefully
    return missing_docstrings

def scan_codebase(path, min_stale_days=90, max_file_loc=500):
    """Scans the given path for entropy and returns a report."""
    report = {
        'stale_files': [],
        'large_files': [],
        'undocumented_python_files': {}
    }

    if not os.path.isdir(path):
        return {'error': f"Path '{path}' is not a directory."}

    for root, _, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(root, filename)

            # Stale files
            age_days = get_file_age_days(filepath)
            if age_days is not None and age_days >= min_stale_days:
                report['stale_files'].append(f"{filepath} (age: {age_days} days)")

            # Large files
            loc = count_lines_of_code(filepath)
            if loc > max_file_loc:
                report['large_files'].append(f"{filepath} (LOC: {loc})")

            # Undocumented Python files
            if filepath.endswith('.py'):
                missing_docs = check_python_docstrings(filepath)
                if missing_docs:
                    report['undocumented_python_files'][filepath] = missing_docs

    return report

def format_report(report, min_stale_days, max_file_loc):
    """Formats the scan report into a human-readable string."""
    output = []
    output.append("--- Codebase Entropy Report ---")
    output.append(f"Scan Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("\n")

    if 'error' in report:
        output.append(f"ERROR: {report['error']}")
        return "\n".join(output)

    if report['stale_files']:
        output.append(f"[!] Stale Files (untouched for {min_stale_days} days or more):")
        for item in report['stale_files']:
            output.append(f"  - {item}")
        output.append("\n")
    else:
        output.append("[*] No stale files detected. Good job!")
        output.append("\n")

    if report['large_files']:
        output.append(f"[!] Large Files (over {max_file_loc} lines of code):")
        for item in report['large_files']:
            output.append(f"  - {item}")
        output.append("\n")
    else:
        output.append("[*] No overly large files detected. Keep it concise!")
        output.append("\n")

    if report['undocumented_python_files']:
        output.append("[!] Undocumented Python Code:")
        for filepath, docs in report['undocumented_python_files'].items():
            output.append(f"  - {filepath}:")
            for doc_item in docs:
                output.append(f"    {doc_item}")
        output.append("\n")
    else:
        output.append("[*] All Python functions/classes appear to have docstrings. Excellent documentation!")
        output.append("\n")

    output.append("--- End of Report ---")
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description="Scan a codebase for signs of entropy (stale files, undocumented code, large files)."
    )
    parser.add_argument(
        "path",
        type=str,
        help="Path to the codebase directory to scan."
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=90,
        help="Minimum number of days a file must be untouched to be considered stale. Default: 90."
    )
    parser.add_argument(
        "--max-file-loc",
        type=int,
        default=500,
        help="Maximum lines of code a file can have before being flagged as large. Default: 500."
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to save the report. If not provided, prints to console."
    )

    args = parser.parse_args()

    report = scan_codebase(args.path, args.stale_days, args.max_file_loc)
    formatted_report = format_report(report, args.stale_days, args.max_file_loc)

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(formatted_report)
            print(f"Entropy report saved to {args.output}")
        except IOError as e:
            print(f"Error saving report to {args.output}: {e}")
    else:
        print(formatted_report)

if __name__ == '__main__':
    main()
