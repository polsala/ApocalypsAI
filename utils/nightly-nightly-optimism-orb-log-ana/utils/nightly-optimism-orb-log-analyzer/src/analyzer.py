import argparse
import os
import fnmatch
from collections import defaultdict

# Define keywords for different sentiment categories
KEYWORDS = {
    "CRITICAL": ["ERROR", "CRITICAL", "FAILURE", "EXCEPTION", "DENIED", "TIMEOUT", "FATAL"],
    "WARNING": ["WARNING", "WARN", "DEPRECATED", "SLOW", "UNAUTHORIZED", "PENDING"],
    "POSITIVE": ["SUCCESS", "COMPLETED", "OK", "READY", "DEPLOYED", "HEALTHY", "UP", "PASSED"],
    "INFO": ["INFO", "DEBUG", "STARTING", "PROCESSING", "REQUEST", "CONNECTED", "INITIALIZED"],
}

# Assign weights for optimism calculation
WEIGHTS = {
    "CRITICAL": -10,
    "WARNING": -3,
    "POSITIVE": 5,
    "INFO": 1,
}

def analyze_log_file(filepath, max_lines=10000):
    """
    Analyzes a single log file for sentiment keywords.
    Returns a dictionary of counts and a list of critical lines.
    """
    counts = defaultdict(int)
    critical_lines = []
    lines_processed = 0

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                lines_processed += 1
                if lines_processed > max_lines:
                    break # Stop processing if max_lines is reached

                line_upper = line.upper()
                found_category = False
                for category, keywords in KEYWORDS.items():
                    if any(kw in line_upper for kw in keywords):
                        counts[category] += 1
                        if category == "CRITICAL":
                            critical_lines.append(line.strip())
                        found_category = True
                        break # Count only the first matching category per line

                if not found_category:
                    counts["UNKNOWN"] += 1 # Catch lines that don't match any specific keyword

    except Exception as e:
        print(f"Warning: Could not read file {filepath}: {e}")
        return None, None, 0 # Indicate failure to read

    return counts, critical_lines, lines_processed

def calculate_optimism_rating(total_counts):
    """
    Calculates an optimism rating based on the total counts of different sentiments.
    Returns a score out of 10 and a descriptive message.
    """
    total_score = 0
    total_weighted_items = 0

    for category, count in total_counts.items():
        if category in WEIGHTS:
            total_score += count * WEIGHTS[category]
            total_weighted_items += count

    if total_weighted_items == 0:
        return 5.0, "The Orb is silent, finding neither joy nor despair. A neutral calm pervades."

    # Normalize score to a 0-10 scale
    # A simple normalization: assume min_score = -10 * total_weighted_items, max_score = 5 * total_weighted_items
    # This is a heuristic, adjust weights and normalization as needed.
    min_possible_score = sum(count * WEIGHTS.get(cat, 0) for cat, count in total_counts.items() if WEIGHTS.get(cat, 0) < 0)
    max_possible_score = sum(count * WEIGHTS.get(cat, 0) for cat, count in total_counts.items() if WEIGHTS.get(cat, 0) > 0)

    # If only negative or only positive, avoid division by zero or negative range issues
    if min_possible_score == 0 and max_possible_score == 0: # Only neutral/unknown
        rating = 5.0
    elif total_score <= min_possible_score:
        rating = 0.0
    elif total_score >= max_possible_score:
        rating = 10.0
    else:
        # Scale score from [min_possible_score, max_possible_score] to [0, 10]
        # This is a simplified scaling. A more robust approach might involve sigmoid or more complex weighting.
        if (max_possible_score - min_possible_score) == 0: # Should not happen if both min/max are not zero
            rating = 5.0
        else:
            rating = 10 * (total_score - min_possible_score) / (max_possible_score - min_possible_score)
            rating = max(0.0, min(10.0, rating)) # Ensure it's within 0-10

    message = ""
    if rating >= 8.0:
        message = "The digital winds sing a triumphant song! Systems are robust, and the future is bright. Keep up the stellar work!"
    elif rating >= 6.0:
        message = "A steady hum of progress fills the air. Minor ripples exist, but the core systems are strong. Vigilance is key!"
    elif rating >= 4.0:
        message = "The Orb senses some turbulence. While not critical, attention to warnings and minor issues could prevent future storms."
    else:
        message = "Dark clouds gather on the horizon. Critical issues demand immediate attention to avert potential digital catastrophe!"

    return round(rating, 1), message


def main():
    parser = argparse.ArgumentParser(
        description="🔮 Nightly Optimism Orb Log Analyzer: Scans logs for system sentiment."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning for log files.",
    )
    parser.add_argument(
        "--patterns",
        nargs=":",
        default=["*.log"],
        help="Glob patterns for log files to include (e.g., '*.log', 'app_*.txt').",
    )
    parser.add_argument(
        "--exclude-patterns",
        nargs=":",
        default=[],
        help="Glob patterns for log files to exclude (e.g., 'debug.log', 'temp_*.log').",
    )
    parser.add_argument(
        "--max-lines",
        type=int,
        default=10000,
        help="Maximum lines to process per file to prevent excessive memory usage.",
    )

    args = parser.parse_args()

    print("🔮 Optimism Orb Log Analysis Report 🔮\n")
    print(f"Scanning directory: {args.path}")
    print(f"Patterns: {args.patterns}")
    print(f"Exclude Patterns: {args.exclude_patterns}\n")
    print("---\n✨ Orb's Glimmering Insights ✨\n---\n")

    total_files_scanned = 0
    total_lines_processed = 0
    total_counts = defaultdict(int)
    files_with_critical_issues = set()

    for root, _, filenames in os.walk(args.path):
        for filename in filenames:
            # Check if filename matches any include pattern
            if not any(fnmatch.fnmatch(filename, p) for p in args.patterns):
                continue

            # Check if filename matches any exclude pattern
            if any(fnmatch.fnmatch(filename, p) for p in args.exclude_patterns):
                continue

            filepath = os.path.join(root, filename)
            total_files_scanned += 1

            file_counts, critical_lines, lines_read = analyze_log_file(filepath, args.max_lines)
            if file_counts is None: # File read error
                continue

            total_lines_processed += lines_read
            for category, count in file_counts.items():
                total_counts[category] += count

            if critical_lines:
                files_with_critical_issues.add(filepath)

    print(f"Total files scanned: {total_files_scanned}")
    print(f"Total lines processed: {total_lines_processed}\n")

    print(f"Critical Messages: {total_counts['CRITICAL']} "
          f"{'(Found in: ' + ', '.join(sorted(list(files_with_critical_issues))) + ')' if files_with_critical_issues else ''}")
    print(f"Warning Messages: {total_counts['WARNING']}")
    print(f"Positive Messages: {total_counts['POSITIVE']}")
    print(f"Informative Messages: {total_counts['INFO']}")
    print(f"Unknown Messages: {total_counts['UNKNOWN']}\n") # Include unknown for completeness

    optimism_rating, rating_message = calculate_optimism_rating(total_counts)

    print("---\n🌟 Optimism Rating: {}/10 🌟".format(optimism_rating))
    print(rating_message)

if __name__ == "__main__":
    main()
