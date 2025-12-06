import argparse
import os
from datetime import datetime
from typing import List, Dict, Optional

def analyze_log_file(
    log_file_path: str,
    keywords: List[str],
    context_lines: int = 2
) -> Dict:
    """
    Scans a log file for specified keywords and collects matching lines
    along with surrounding context.

    Args:
        log_file_path: Path to the log file.
        keywords: List of keywords to search for (case-insensitive).
        context_lines: Number of lines before and after a match to include.

    Returns:
        A dictionary containing scan results:
        {
            "log_file": str,
            "scan_date": str,
            "keywords_searched": List[str],
            "total_lines_scanned": int,
            "matches_found": int,
            "details": List[Dict]
        }
    """
    if not os.path.exists(log_file_path):
        raise FileNotFoundError(f"Log file not found: {log_file_path}")

    results: Dict = {
        "log_file": log_file_path,
        "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "keywords_searched": [k.upper() for k in keywords],
        "total_lines_scanned": 0,
        "matches_found": 0,
        "details": []
    }

    # Read all lines to easily get context
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        all_lines = f.readlines()
    
    results["total_lines_scanned"] = len(all_lines)

    for i, line in enumerate(all_lines):
        for keyword in keywords:
            if keyword.lower() in line.lower():
                results["matches_found"] += 1
                
                # Collect context lines
                start_index = max(0, i - context_lines)
                end_index = min(len(all_lines), i + context_lines + 1)
                
                context = []
                for j in range(start_index, end_index):
                    context.append(f"Line {j+1}: {all_lines[j].strip()}")

                results["details"].append({
                    "keyword": keyword.upper(),
                    "line_number": i + 1,
                    "matched_line": line.strip(),
                    "context": context
                })
                # Break from inner loop to avoid multiple matches on the same line
                break 
    
    return results

def format_report(results: Dict) -> str:
    """
    Formats the scan results into a human-readable report string.
    """
    report_parts = [
        "--- Log Whisperer Report ---",
        f"Scan Date: {results['scan_date']}",
        f"Log File: {results['log_file']}",
        f"Keywords Searched: {', '.join(results['keywords_searched'])}",
        "",
        "--- Summary ---",
        f"Total lines scanned: {results['total_lines_scanned']}",
        f"Matches found: {results['matches_found']}",
        "",
        "--- Details ---"
    ]

    if not results["details"]:
        report_parts.append("No matches found for the specified keywords.")
    else:
        for i, detail in enumerate(results["details"]):
            report_parts.append(f"\n[Match {i+1}] Keyword: {detail['keyword']} (Line {detail['line_number']})")
            report_parts.append("Context:")
            for ctx_line in detail['context']:
                report_parts.append(f"  {ctx_line}")

    report_parts.append("\n--- End Report ---")
    return "\n".join(report_parts)

def main():
    parser = argparse.ArgumentParser(
        description="Scan log files for keywords and generate a summary report."
    )
    parser.add_argument(
        "--log-file",
        "-l",
        required=True,
        help="Path to the log file to be analyzed."
    )
    parser.add_argument(
        "--keywords",
        "-k",
        nargs=":",
        default=["ERROR", "WARNING", "CRITICAL"],
        help="Space-separated list of keywords to search for. Case-insensitive. (Default: ERROR WARNING CRITICAL)"
    )
    parser.add_argument(
        "--output-file",
        "-o",
        help="Path to save the summary report. If not provided, report is printed to stdout."
    )
    parser.add_argument(
        "--context-lines",
        "-c",
        type=int,
        default=2,
        help="Number of lines before and after a keyword match to include in the report for context. (Default: 2)"
    )

    args = parser.parse_args()

    try:
        results = analyze_log_file(args.log_file, args.keywords, args.context_lines)
        report = format_report(results)

        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to {args.output_file}")
        else:
            print(report)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=os.sys.stderr)
        os.sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=os.sys.stderr)
        os.sys.exit(1)

if __name__ == "__main__":
    main()
