import re
import sys
from typing import List, Tuple

# Define patterns for 'gloom' and 'glimmer' events
# These are regular expressions and can be customized.
GLOOM_PATTERNS = [
    re.compile(r'ERROR', re.IGNORECASE),
    re.compile(r'FAIL', re.IGNORECASE),
    re.compile(r'CRITICAL', re.IGNORECASE),
    re.compile(r'EXCEPTION', re.IGNORECASE),
    re.compile(r'WARNING', re.IGNORECASE),
    re.compile(r'DENIED', re.IGNORECASE),
    re.compile(r'TIMEOUT', re.IGNORECASE),
    re.compile(r'UNAUTHORIZED', re.IGNORECASE),
]

GLIMMER_PATTERNS = [
    re.compile(r'SUCCESS', re.IGNORECASE),
    re.compile(r'INFO', re.IGNORECASE),
    re.compile(r'START', re.IGNORECASE),
    re.compile(r'COMPLETE', re.IGNORECASE),
    re.compile(r'CONNECTED', re.IGNORECASE),
    re.compile(r'READY', re.IGNORECASE),
    re.compile(r'INITIALIZED', re.IGNORECASE),
]

# Scoring weights
GLOOM_WEIGHT = -2
GLIMMER_WEIGHT = 1

def analyze_log_content(log_content: List[str]) -> Tuple[int, int, int, int]:
    """
    Analyzes a list of log lines for gloom and glimmer patterns.
    Returns (total_lines, gloom_count, glimmer_count, gloom_glimmer_score).
    """
    total_lines = len(log_content)
    gloom_count = 0
    glimmer_count = 0
    gloom_glimmer_score = 0

    for line in log_content:
        is_gloom = False

        # Check for gloom patterns first. If found, prioritize it.
        for pattern in GLOOM_PATTERNS:
            if pattern.search(line):
                gloom_count += 1
                gloom_glimmer_score += GLOOM_WEIGHT
                is_gloom = True
                break # Count only one gloom event per line
        
        # Only count glimmer if no gloom was found on the same line
        if not is_gloom:
            for pattern in GLIMMER_PATTERNS:
                if pattern.search(line):
                    glimmer_count += 1
                    gloom_glimmer_score += GLIMMER_WEIGHT
                    break # Count only one glimmer event per line

    return total_lines, gloom_count, glimmer_count, gloom_glimmer_score

def get_sentiment_summary(score: int) -> str:
    """
    Generates a whimsical, apocalypse-themed summary based on the gloom-glimmer score.
    """
    if score >= 20:
        return "A beacon in the desolation! Your systems are thriving amidst the chaos. Keep up the excellent work, survivor!"
    elif score >= 5:
        return "A faint glimmer of hope pierces the perpetual twilight. Your systems are mostly holding together, but keep an eye on those flickering lights."
    elif score >= -5:
        return "The world is a grey expanse, neither truly doomed nor truly saved. Your systems are stable, but vigilance is key. The silence is often the most unsettling."
    elif score >= -20:
        return "Shadows lengthen, and the air grows heavy with foreboding. Your systems are showing signs of strain. Prepare for potential fallout."
    else:
        return "The abyss stares back. Your systems are in dire straits. Immediate intervention is required, or all will be lost to the encroaching darkness!"

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/analyzer.py <path_to_your_log_file>")
        sys.exit(1)

    log_file_path = sys.argv[1]

    try:
        with open(log_file_path, 'r') as f:
            log_content = f.readlines()
    except FileNotFoundError:
        print(f"Error: Log file not found at '{log_file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{log_file_path}': {e}")
        sys.exit(1)

    total_lines, gloom_count, glimmer_count, gloom_glimmer_score = analyze_log_content(log_content)

    print(f"Analyzing log file: {log_file_path}\n")
    print("--- Gloom-Glimmer Report ---")
    print(f"\nTotal Lines Scanned: {total_lines}")
    print(f"Gloom Events (Errors, Warnings, etc.): {gloom_count}")
    print(f"Glimmer Events (Successes, Info, etc.): {glimmer_count}")
    print(f"\nGloom-Glimmer Score: {gloom_glimmer_score}")
    print(f"\nOverall Sentiment: {get_sentiment_summary(gloom_glimmer_score)}")
    print("----------------------------")

if __name__ == '__main__':
    main()
