import os
import ast
import argparse

def get_docstring_status(node):
    """Checks if a node (class or function) has a docstring."""
    return ast.get_docstring(node) is not None

def analyze_python_file(filepath):
    """Analyzes a single Python file for docstrings and comment density."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    tree = ast.parse(content)

    missing_docstrings = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not get_docstring_status(node):
                node_type = 'Class' if isinstance(node, ast.ClassDef) else 'Function'
                missing_docstrings.append(f"- {node_type}: {node.name}")

    # Calculate comment density
    total_lines = len(content.splitlines())
    comment_lines = 0
    for line in content.splitlines():
        stripped_line = line.strip()
        if stripped_line.startswith('#'):
            comment_lines += 1

    comment_density = (comment_lines / total_lines) * 100 if total_lines > 0 else 0

    return {
        'filepath': filepath,
        'missing_docstrings': missing_docstrings,
        'comment_density': comment_density,
        'total_lines': total_lines,
        'comment_lines': comment_lines
    }

def generate_report(results, min_comment_density, scanned_dir):
    """Generates a formatted report from analysis results."""
    report_lines = []
    report_lines.append("Quantum Quill Sharpening Report")
    report_lines.append("--------------------------------")
    report_lines.append(f"\nScanning directory: {scanned_dir}\n")

    total_files_scanned = len(results)
    files_low_density = 0
    total_missing_docstrings = 0

    for result in results:
        report_lines.append(f"File: {result['filepath']}")
        report_lines.append(f"  Comment Density: {result['comment_density']:.2f}%")
        if result['comment_density'] < min_comment_density:
            report_lines.append(f"  (Below {min_comment_density:.2f}% threshold)")
            files_low_density += 1

        if result['missing_docstrings']:
            report_lines.append("  Missing Docstrings:")
            report_lines.extend([f"    {ds}" for ds in result['missing_docstrings']])
            total_missing_docstrings += len(result['missing_docstrings'])
        else:
            report_lines.append("  Missing Docstrings: None")
        report_lines.append("") # Blank line for readability

    report_lines.append("--------------------------------")
    report_lines.append("Summary:")
    report_lines.append(f"  Total files scanned: {total_files_scanned}")
    report_lines.append(f"  Files with low comment density: {files_low_density}")
    report_lines.append(f"  Total missing docstrings: {total_missing_docstrings}")

    return "\n".join(report_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Scan Python files for missing docstrings and low comment density."
    )
    parser.add_argument(
        '--path', 
        type=str, 
        required=True, 
        help='The root directory to start scanning for Python files.'
    )
    parser.add_argument(
        '--min-comment-density', 
        type=float, 
        default=10.0, 
        help='Threshold for flagging files with low comment density (percentage).'
    )

    args = parser.parse_args()

    target_dir = args.path
    min_density = args.min_comment_density

    if not os.path.isdir(target_dir):
        print(f"Error: Directory '{target_dir}' not found.")
        exit(1)

    all_results = []
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    result = analyze_python_file(filepath)
                    all_results.append(result)
                except Exception as e:
                    print(f"Warning: Could not analyze {filepath} - {e}")

    if all_results:
        report = generate_report(all_results, min_density, target_dir)
        print(report)
    else:
        print(f"No Python files found in '{target_dir}'.")

if __name__ == '__main__':
    main()
