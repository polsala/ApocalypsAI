import argparse
import os
from collections import defaultdict

class LogAnalyzer:
    def __init__(self, gloom_keywords=None, glimmer_keywords=None):
        self.gloom_keywords = [k.lower() for k in gloom_keywords or ["error", "fail", "warning", "critical", "exception", "broken", "denied"]]
        self.glimmer_keywords = [k.lower() for k in glimmer_keywords or ["success", "complete", "healthy", "ok", "healed", "restored", "granted"]]

    def analyze_file(self, filepath):
        gloom_count = 0
        glimmer_count = 0
        gloom_lines = []
        glimmer_lines = []

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    lower_line = line.lower()
                    for keyword in self.gloom_keywords:
                        if keyword in lower_line:
                            gloom_count += 1
                            gloom_lines.append(f"  Line {line_num}: {line.strip()}")
                            break # Count only once per line for gloom
                    for keyword in self.glimmer_keywords:
                        if keyword in lower_line:
                            glimmer_count += 1
                            glimmer_lines.append(f"  Line {line_num}: {line.strip()}")
                            break # Count only once per line for glimmer
        except IOError as e:
            return {
                "filepath": filepath,
                "gloom_count": 0,
                "glimmer_count": 0,
                "gloom_lines": [],
                "glimmer_lines": [],
                "error": str(e)
            }
        return {
            "filepath": filepath,
            "gloom_count": gloom_count,
            "glimmer_count": glimmer_count,
            "gloom_lines": gloom_lines,
            "glimmer_lines": glimmer_lines,
            "error": None
        }

    def analyze_paths(self, paths):
        results = []
        for path in paths:
            if os.path.isfile(path):
                results.append(self.analyze_file(path))
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        filepath = os.path.join(root, file)
                        results.append(self.analyze_file(filepath))
            else:
                results.append({
                    "filepath": path,
                    "gloom_count": 0,
                    "glimmer_count": 0,
                    "gloom_lines": [],
                    "glimmer_lines": [],
                    "error": "Path not found or not a file/directory."
                })
        return results

def main():
    parser = argparse.ArgumentParser(
        description="Gloom-Glimmer Log Analyzer: Scan logs for system health."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="One or more file or directory paths to analyze."
    )
    parser.add_argument(
        "--gloom-keywords",
        nargs="+",
        help="Custom keywords for 'gloom' (e.g., 'error', 'fail'). Overrides defaults."
    )
    parser.add_argument(
        "--glimmer-keywords",
        nargs="+",
        help="Custom keywords for 'glimmer' (e.g., 'success', 'ok'). Overrides defaults."
    )
    parser.add_argument(
        "--show-lines",
        action="store_true",
        help="Show specific lines where gloom/glimmer keywords were found."
    )

    args = parser.parse_args()

    analyzer = LogAnalyzer(args.gloom_keywords, args.glimmer_keywords)
    results = analyzer.analyze_paths(args.paths)

    total_gloom = 0
    total_glimmer = 0
    
    print("\n--- Gloom-Glimmer Log Analysis Report ---")
    print("-----------------------------------------")

    for res in results:
        if res["error"]:
            print(f"\n[!] Skipping {res['filepath']}: {res['error']}")
            continue

        total_gloom += res["gloom_count"]
        total_glimmer += res["glimmer_count"]

        print(f"\nFile: {res['filepath']}")
        print(f"  Gloom Count: {res['gloom_count']}")
        print(f"  Glimmer Count: {res['glimmer_count']}")
        
        if args.show_lines:
            if res["gloom_lines"]:
                print("  Gloom Lines:")
                for line in res["gloom_lines"]:
                    print(line)
            if res["glimmer_lines"]:
                print("  Glimmer Lines:")
                for line in res["glimmer_lines"]:
                    print(line)
    
    print("\n--- Overall System Vibe ---")
    print(f"Total Gloom Events: {total_gloom}")
    print(f"Total Glimmer Events: {total_glimmer}")

    if total_gloom == 0 and total_glimmer == 0:
        print("The logs are silent... perhaps too silent.")
    elif total_gloom > total_glimmer * 2:
        print("Warning: Heavy gloom detected. System integrity might be compromised.")
    elif total_gloom > total_glimmer:
        print("Caution: More gloom than glimmer. Keep an eye on things.")
    elif total_glimmer > total_gloom * 2:
        print("Excellent! Abundant glimmer. System appears robust.")
    elif total_glimmer > total_gloom:
        print("Good: More glimmer than gloom. System is generally healthy.")
    else:
        print("Balanced: Gloom and glimmer are in equilibrium. A stable state.")

    print("-----------------------------------------")

if __name__ == "__main__":
    main()
