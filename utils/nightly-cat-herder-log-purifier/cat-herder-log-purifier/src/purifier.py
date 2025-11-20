import argparse
import re
import sys
from collections import Counter
from typing import List, Optional, Tuple

from rich.console import Console
from rich.text import Text

# Define log level mapping for consistent parsing and filtering
LOG_LEVELS = {
    'DEBUG': 0,
    'INFO': 1,
    'WARNING': 2,
    'ERROR': 3,
    'CRITICAL': 4
}

# Regex to parse common log formats. This is a simplified example.
# It tries to capture a timestamp (optional), a log level, and the message.
LOG_PATTERN = re.compile(r'^(?:\S+\s+){0,2}?\[?(DEBUG|INFO|WARNING|ERROR|CRITICAL)\]?\s*(.*)$', re.IGNORECASE)

def parse_log_line(line: str) -> Tuple[Optional[str], str]:
    """
    Parses a log line to extract its level and message.
    Returns (level, message) or (None, original_line) if parsing fails.
    """
    match = LOG_PATTERN.match(line)
    if match:
        level = match.group(1).upper()
        message = match.group(2).strip()
        return level, message
    return None, line.strip()

def purify_logs(
    log_file_path: str,
    min_level_str: str = 'DEBUG',
    highlight_keywords: Optional[List[str]] = None,
    show_summary: bool = False,
    no_color: bool = False
) -> None:
    """
    Processes a log file, filters, highlights, and prints entries.
    Optionally provides a summary.
    """
    console = Console(no_color=no_color)
    min_level_value = LOG_LEVELS.get(min_level_str.upper(), LOG_LEVELS['DEBUG'])
    highlight_patterns = [re.compile(re.escape(k), re.IGNORECASE) for k in (highlight_keywords or [])]
    log_counts = Counter()
    line_num = 0

    try:
        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line_num += 1
                level, message = parse_log_line(line)

                if level:
                    log_counts[level] += 1
                    if LOG_LEVELS[level] < min_level_value:
                        continue # Skip if level is below minimum
                else:
                    # If no level found, treat as UNCLASSIFIED, but still process if not filtered by level
                    log_counts['UNCLASSIFIED'] += 1
                    if min_level_value > LOG_LEVELS['DEBUG']:
                        continue # If we're filtering, unclassified lines are usually noise

                display_text = Text(f"[{line_num}] ")

                # Apply level coloring
                if level == 'DEBUG':
                    display_text.append(f"[{level}] ", style="dim")
                elif level == 'INFO':
                    display_text.append(f"[{level}] ", style="cyan")
                elif level == 'WARNING':
                    display_text.append(f"[{level}] ", style="yellow")
                elif level == 'ERROR':
                    display_text.append(f"[{level}] ", style="red bold")
                elif level == 'CRITICAL':
                    display_text.append(f"[{level}] ", style="white on red bold")
                else:
                    display_text.append(f"[UNCLASSIFIED] ", style="grey50")

                # Apply keyword highlighting
                highlighted_message = Text(message)
                for pattern in highlight_patterns:
                    for match in pattern.finditer(message):
                        highlighted_message.highlight_span(match.start(), match.end(), style="bold magenta on black")
                
                display_text.append(highlighted_message)
                console.print(display_text)

    except FileNotFoundError:
        console.print(f"[red bold]Error:[/red bold] Log file not found at '{log_file_path}'")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red bold]An unexpected error occurred:[/red bold] {e}")
        sys.exit(1)

    if show_summary:
        console.print("\n--- Log Summary ---", style="bold")
        total_entries = sum(log_counts.values())
        # Sort levels by their defined order, then add UNCLASSIFIED if present
        sorted_levels = sorted(LOG_LEVELS.keys(), key=lambda x: LOG_LEVELS[x])
        if 'UNCLASSIFIED' in log_counts and 'UNCLASSIFIED' not in sorted_levels:
            sorted_levels.append('UNCLASSIFIED')

        for level_name in sorted_levels:
            count = log_counts.get(level_name, 0)
            if count > 0:
                console.print(f"{level_name:<12}: {count}")
        console.print(f"{'Total':<12}: {total_entries}", style="bold")

def main():
    parser = argparse.ArgumentParser(
        description="Cat Herder Log Purifier: Tame your chaotic log files."
    )
    parser.add_argument(
        "log_file_path",
        type=str,
        help="Path to the log file to purify."
    )
    parser.add_argument(
        "--level",
        type=str,
        default="DEBUG",
        choices=list(LOG_LEVELS.keys()),
        help="Minimum log level to display (DEBUG, INFO, WARNING, ERROR, CRITICAL). Default: DEBUG."
    )
    parser.add_argument(
        "--highlight",
        nargs='+',
        help="One or more keywords to highlight in the output. Case-insensitive."
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Display a summary of log levels at the end."
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable color output."
    )

    args = parser.parse_args()

    purify_logs(
        args.log_file_path,
        min_level_str=args.level,
        highlight_keywords=args.highlight,
        show_summary=args.summary,
        no_color=args.no_color
    )

if __name__ == "__main__":
    main()
