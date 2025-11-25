import argparse
import sys
from collections import defaultdict

def analyze_log_content(log_content, gloom_keywords, glimmer_keywords):
    """
    Analyzes log content for occurrences of gloom and glimmer keywords.
    Keywords are case-insensitive.
    """
    results = {
        "gloom_count": 0,
        "glimmer_count": 0,
        "gloom_lines": [],
        "glimmer_lines": [],
    }
    
    lower_gloom_keywords = [k.lower() for k in gloom_keywords]
    lower_glimmer_keywords = [k.lower() for k in glimmer_keywords]

    for i, line in enumerate(log_content.splitlines()):
        lower_line = line.lower()
        
        is_gloom = any(kw in lower_line for kw in lower_gloom_keywords)
        is_glimmer = any(kw in lower_line for kw in lower_glimmer_keywords)

        if is_gloom:
            results["gloom_count"] += 1
            results["gloom_lines"].append(f"Line {i+1}: {line.strip()}")
        if is_glimmer:
            results["glimmer_count"] += 1
            results["glimmer_lines"].append(f"Line {i+1}: {line.strip()}")
            
    return results

def analyze_log_file(filepath, gloom_keywords, glimmer_keywords):
    """
    Reads a log file and analyzes its content.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return analyze_log_content(content, gloom_keywords, glimmer_keywords)
    except FileNotFoundError:
        print(f"Error: Log file not found at '{filepath}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Gloom-Glimmer Log Analyzer: Scans log files for signs of doom and hope."
    )
    parser.add_argument(
        "filepath",
        help="Path to the log file to analyze."
    )
    parser.add_argument(
        "--gloom-keywords",
        nargs='*',
        default=["error", "fail", "exception", "critical", "denied", "broken"],
        help="Space-separated keywords indicating 'gloom'. Default: error fail exception critical denied broken"
    )
    parser.add_argument(
        "--glimmer-keywords",
        nargs='*',
        default=["success", "complete", "info", "healthy", "ok", "ready"],
        help="Space-separated keywords indicating 'glimmer'. Default: success complete info healthy ok ready"
    )

    args = parser.parse_args()

    print(f"Analyzing '{args.filepath}' for gloom and glimmer...")
    results = analyze_log_file(args.filepath, args.gloom_keywords, args.glimmer_keywords)

    print("\n--- Analysis Report ---")
    print(f"Gloom detected: {results['gloom_count']} instances")
    for line in results['gloom_lines']:
        print(f"  [Gloom] {line}")

    print(f"\nGlimmer detected: {results['glimmer_count']} instances")
    for line in results['glimmer_lines']:
        print(f"  [Glimmer] {line}")

    if results['gloom_count'] > results['glimmer_count']:
        print("\nOverall Outlook: The shadows lengthen. Proceed with caution, survivor.")
    elif results['glimmer_count'] > 0:
        print("\nOverall Outlook: A faint light pierces the gloom! Hope remains.")
    else:
        print("\nOverall Outlook: The logs are silent. Is that good or bad? Only time will tell.")

if __name__ == "__main__":
    main()
