import argparse
import os
from collections import defaultdict

DEFAULT_GLOOM_KEYWORDS = ["ERROR", "FAILURE", "CRITICAL", "FAIL", "EXCEPTION"]
DEFAULT_GLIMMER_KEYWORDS = ["SUCCESS", "COMPLETE", "CONNECTED", "ONLINE", "OK", "INFO"]

def analyze_log_file(filepath: str, gloom_keywords: list[str], glimmer_keywords: list[str]) -> dict:
    """
    Analyzes a single log file for gloom and glimmer keywords.
    Returns a dictionary with counts.
    """
    gloom_count = 0
    glimmer_count = 0
    total_lines = 0

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                total_lines += 1
                line_upper = line.upper()
                for keyword in gloom_keywords:
                    if keyword in line_upper:
                        gloom_count += 1
                        break # Count only once per line for gloom
                for keyword in glimmer_keywords:
                    if keyword in line_upper:
                        glimmer_count += 1
                        break # Count only once per line for glimmer
    except IOError as e:
        print(f"Warning: Could not read file {filepath}: {e}")
        return {"gloom": 0, "glimmer": 0, "lines": 0}

    return {"gloom": gloom_count, "glimmer": glimmer_count, "lines": total_lines}

def analyze_logs(
    path: str,
    gloom_keywords: list[str] = None,
    glimmer_keywords: list[str] = None
) -> dict:
    """
    Analyzes log files in a given path (file or directory).
    """
    if gloom_keywords is None:
        gloom_keywords = DEFAULT_GLOOM_KEYWORDS
    if glimmer_keywords is None:
        glimmer_keywords = DEFAULT_GLIMMER_KEYWORDS

    total_gloom = 0
    total_glimmer = 0
    total_lines_processed = 0
    files_scanned = 0
    
    log_files_to_process = []

    if os.path.isfile(path):
        log_files_to_process.append(path)
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".log"):
                    log_files_to_process.append(os.path.join(root, file))
    else:
        raise FileNotFoundError(f"Path not found or is not a file/directory: {path}")

    for filepath in log_files_to_process:
        files_scanned += 1
        result = analyze_log_file(filepath, gloom_keywords, glimmer_keywords)
        total_gloom += result["gloom"]
        total_glimmer += result["glimmer"]
        total_lines_processed += result["lines"]

    glimmer_ratio = 0.0
    total_relevant_entries = total_gloom + total_glimmer
    if total_relevant_entries > 0:
        glimmer_ratio = total_glimmer / total_relevant_entries

    return {
        "files_scanned": files_scanned,
        "total_lines_processed": total_lines_processed,
        "total_gloom_entries": total_gloom,
        "total_glimmer_entries": total_glimmer,
        "glimmer_ratio": glimmer_ratio,
    }

def main():
    parser = argparse.ArgumentParser(
        description="Gloom-Glimmer Log Analyzer: Assess the mood of your systems."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Path to a log file or a directory containing .log files."
    )
    parser.add_argument(
        "--gloom-keywords",
        type=lambda s: [k.strip().upper() for k in s.split(',')],
        default=','.join(DEFAULT_GLOOM_KEYWORDS),
        help=f"Comma-separated list of keywords indicating 'gloom'. Default: {', '.join(DEFAULT_GLOOM_KEYWORDS)}"
    )
    parser.add_argument(
        "--glimmer-keywords",
        type=lambda s: [k.strip().upper() for k in s.split(',')],
        default=','.join(DEFAULT_GLIMMER_KEYWORDS),
        help=f"Comma-separated list of keywords indicating 'glimmer'. Default: {', '.join(DEFAULT_GLIMMER_KEYWORDS)}"
    )

    args = parser.parse_args()

    gloom_kws = args.gloom_keywords if args.gloom_keywords else DEFAULT_GLOOM_KEYWORDS
    glimmer_kws = args.glimmer_keywords if args.glimmer_keywords else DEFAULT_GLIMMER_KEYWORDS

    try:
        results = analyze_logs(args.path, gloom_kws, glimmer_kws)

        print("\n--- Gloom-Glimmer Log Analysis Report ---")
        print(f"Files Scanned: {results['files_scanned']}")
        print(f"Total Lines Processed: {results['total_lines_processed']}")
        print(f"Total Gloom Entries: {results['total_gloom_entries']}")
        print(f"Total Glimmer Entries: {results['total_glimmer_entries']}")
        print(f"Glimmer Ratio (Glimmers / Total Relevant): {results['glimmer_ratio']:.4f}")
        print("-----------------------------------------")
        if results['glimmer_ratio'] >= 0.75:
            print("Outlook: Highly hopeful! Keep up the good work.")
        elif results['glimmer_ratio'] >= 0.5:
            print("Outlook: Balanced. A good mix of challenges and successes.")
        elif results['glimmer_ratio'] >= 0.25:
            print("Outlook: Challenging. More gloom than glimmer, but not hopeless.")
        else:
            print("Outlook: Grim. Prepare for potential system collapse or a very bad day.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
