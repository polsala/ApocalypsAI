import argparse
import os
from collections import defaultdict

def analyze_logs(log_paths, keywords):
    """
    Scans specified log files for predefined keywords and generates a summary report.

    Args:
        log_paths (list): A list of file paths to log files.
        keywords (list): A list of keywords to search for (case-insensitive).

    Returns:
        dict: A dictionary containing the analysis report.
              Example:
              {
                  "total_files_scanned": 2,
                  "files_with_issues": 1,
                  "report": {
                      "log_file_1.log": {
                          "ERROR": 2,
                          "WARNING": 1,
                          "CRITICAL": 0,
                          "total_matches": 3
                      },
                      "log_file_2.log": {
                          "ERROR": 0,
                          "WARNING": 0,
                          "CRITICAL": 0,
                          "total_matches": 0
                      }
                  },
                  "overall_summary": {
                      "ERROR": 2,
                      "WARNING": 1,
                      "CRITICAL": 0,
                      "total_matches": 3
                  }
              }
    """
    report = {
        "total_files_scanned": 0,
        "files_with_issues": 0,
        "report": {},
        "overall_summary": defaultdict(int)
    }
    
    lower_keywords = [k.lower() for k in keywords]

    for path in log_paths:
        report["total_files_scanned"] += 1
        file_summary = {k: 0 for k in keywords}
        file_summary["total_matches"] = 0
        
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    lower_line = line.lower()
                    for original_keyword, lower_keyword in zip(keywords, lower_keywords):
                        if lower_keyword in lower_line:
                            file_summary[original_keyword] += 1
                            file_summary["total_matches"] += 1
                            report["overall_summary"][original_keyword] += 1
                            report["overall_summary"]["total_matches"] += 1
            
            report["report"][os.path.basename(path)] = file_summary
            if file_summary["total_matches"] > 0:
                report["files_with_issues"] += 1

        except FileNotFoundError:
            report["report"][os.path.basename(path)] = {"error": "File not found"}
        except Exception as e:
            report["report"][os.path.basename(path)] = {"error": str(e)}

    # Convert defaultdict to dict for final output
    report["overall_summary"] = dict(report["overall_summary"])
    return report

def main():
    parser = argparse.ArgumentParser(
        description="Gloom-Glimmer Log Analyzer: Scans log files for keywords and provides a summary."
    )
    parser.add_argument(
        "log_paths",
        nargs=":",
        help="One or more paths to log files to analyze."
    )
    parser.add_argument(
        "--keywords",
        nargs=":",
        default=["ERROR", "WARNING", "CRITICAL"],
        help="Keywords to search for (case-insensitive). Default: ERROR WARNING CRITICAL"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output the report in JSON format."
    )

    args = parser.parse_args()

    if not args.log_paths:
        parser.error("At least one log file path is required.")

    analysis_result = analyze_logs(args.log_paths, args.keywords)

    if args.json:
        import json
        print(json.dumps(analysis_result, indent=2))
    else:
        print("--- Gloom-Glimmer Log Analysis Report ---")
        print(f"Total files scanned: {analysis_result['total_files_scanned']}")
        print(f"Files with issues: {analysis_result['files_with_issues']}")
        print("\n--- File-specific Reports ---")
        for filename, summary in analysis_result["report"].items():
            print(f"\nFile: {filename}")
            if "error" in summary:
                print(f"  Error: {summary['error']}")
            else:
                for keyword, count in summary.items():
                    if keyword != "total_matches":
                        print(f"  {keyword}: {count}")
                print(f"  Total matches in file: {summary['total_matches']}")
        
        print("\n--- Overall Summary ---")
        for keyword, count in analysis_result["overall_summary"].items():
            if keyword != "total_matches":
                print(f"  {keyword}: {count}")
        print(f"  Total matches overall: {analysis_result['overall_summary'].get('total_matches', 0)}")
        print("\n---------------------------------------")

if __name__ == "__main__":
    main()
