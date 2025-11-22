import sys
import os

def analyze_log(log_content: str) -> dict:
    """
    Analyzes log content for 'gloom' and 'glimmer' keywords.

    Args:
        log_content: A string containing the entire log file content.

    Returns:
        A dictionary with counts of gloom and glimmer events.
    """
    gloom_keywords = {
        "ERROR": 0,
        "WARNING": 0,
        "CRITICAL": 0,
        "FAILURE": 0,
        "FAIL": 0,
        "EXCEPTION": 0,
        "DENIED": 0,
        "TIMEOUT": 0,
    }
    glimmer_keywords = {
        "SUCCESS": 0,
        "INFO": 0,
        "OK": 0,
        "COMPLETED": 0,
        "HEALED": 0,
        "CONNECTED": 0,
        "READY": 0,
        "OPTIMAL": 0,
    }

    total_lines = 0
    lines = log_content.splitlines()
    total_lines = len(lines)

    for line in lines:
        upper_line = line.upper()
        for keyword in gloom_keywords:
            if keyword in upper_line:
                gloom_keywords[keyword] += 1
        for keyword in glimmer_keywords:
            if keyword in upper_line:
                glimmer_keywords[keyword] += 1

    total_gloom = sum(gloom_keywords.values())
    total_glimmer = sum(glimmer_keywords.values())

    return {
        "total_lines": total_lines,
        "gloom_keywords": {k: v for k, v in gloom_keywords.items() if v > 0},
        "glimmer_keywords": {k: v for k, v in glimmer_keywords.items() if v > 0},
        "total_gloom": total_gloom,
        "total_glimmer": total_glimmer,
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyzer.py <path_to_log_file>")
        sys.exit(1)

    log_file_path = sys.argv[1]

    if not os.path.exists(log_file_path):
        print(f"Error: Log file not found at '{log_file_path}'")
        sys.exit(1)

    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            log_content = f.read()
    except Exception as e:
        print(f"Error reading log file: {e}")
        sys.exit(1)

    results = analyze_log(log_content)

    print("\n--- Gloom-Glimmer Log Analysis ---")
    print(f"Log File: {log_file_path}")
    print(f"Total Lines Scanned: {results['total_lines']}\n")

    print("Gloom Events:")
    if results['gloom_keywords']:
        for keyword, count in results['gloom_keywords'].items():
            print(f"  - {keyword}: {count}")
    else:
        print("  No significant gloom detected.")
    print(f"Total Gloom: {results['total_gloom']}\n")

    print("Glimmer Events:")
    if results['glimmer_keywords']:
        for keyword, count in results['glimmer_keywords'].items():
            print(f"  - {keyword}: {count}")
    else:
        print("  No significant glimmer detected.")
    print(f"Total Glimmer: {results['total_glimmer']}\n")

    print("--- Overall System Mood ---")
    if results['total_glimmer'] > results['total_gloom'] * 2:
        mood = "Mostly Glimmering!"
    elif results['total_glimmer'] > results['total_gloom']:
        mood = "Leaning Glimmering."
    elif results['total_gloom'] > results['total_glimmer'] * 2:
        mood = "Deeply Gloomy."
    elif results['total_gloom'] > results['total_glimmer']:
        mood = "Leaning Gloomy."
    else:
        mood = "Balanced, or eerily quiet."

    print(f"Feeling: {mood} ({results['total_glimmer']} Glimmer vs {results['total_gloom']} Gloom)")


if __name__ == "__main__":
    main()
