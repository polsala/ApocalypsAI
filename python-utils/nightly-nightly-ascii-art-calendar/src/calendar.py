import argparse
import calendar
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple


def generate_ascii_calendar(
    year: int,
    month: int,
    events: Optional[Dict[str, str]] = None,
    show_year: bool = True,
) -> str:
    """
    Generate an ASCII-art calendar for the given month and year.
    
    Args:
        year: The year (e.g., 2024)
        month: The month (1-12)
        events: Dictionary mapping YYYY-MM-DD strings to symbols
        show_year: Whether to include the year in the header
    
    Returns:
        String containing the ASCII calendar
    """
    if not (1 <= month <= 12):
        raise ValueError("Month must be between 1 and 12")
    
    if events is None:
        events = {}
    
    # Get calendar data
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    # Build header
    if show_year:
        header = f"{month_name} {year}"
    else:
        header = f"{month_name}"
    
    # Center header
    header_line = f"{header:^21}"
    
    # Day headers
    day_headers = "Su Mo Tu We Th Fr Sa"
    
    # Separator
    separator = "--------------------"
    
    # Build calendar body
    calendar_lines = [header_line, day_headers, separator]
    
    for week in cal:
        week_line = ""
        for day in week:
            if day == 0:
                # Empty day
                week_line += "   "
            else:
                # Format day with potential event marker
                date_str = f"{year:04d}-{month:02d}-{day:02d}"
                if date_str in events:
                    # Day with event
                    marker = events[date_str]
                    if len(marker) == 1:
                        week_line += f" {marker} "
                    else:
                        # Truncate long markers
                        week_line += f" {marker[:1]} "
                else:
                    # Regular day
                    week_line += f"{day:2d} "
        calendar_lines.append(week_line.rstrip())
    
    return "\n".join(calendar_lines)


def parse_events(event_args: List[str]) -> Dict[str, str]:
    """
    Parse event arguments into a dictionary.
    
    Args:
        event_args: List of strings in format "YYYY-MM-DD=symbol"
    
    Returns:
        Dictionary mapping date strings to symbols
    """
    events = {}
    for event in event_args:
        if "=" not in event:
            raise ValueError(f"Event format should be YYYY-MM-DD=symbol, got: {event}")
        
        date_str, symbol = event.split("=", 1)
        
        # Validate date format
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD.")
        
        events[date_str] = symbol
    return events


def main():
    parser = argparse.ArgumentParser(
        description="Generate an ASCII-art calendar for any month/year"
    )
    parser.add_argument(
        "--year",
        type=int,
        default=datetime.now().year,
        help="Year (default: current year)",
    )
    parser.add_argument(
        "--month",
        type=int,
        default=datetime.now().month,
        help="Month (1-12, default: current month)",
    )
    parser.add_argument(
        "--events",
        nargs="*",
        default=[],
        help="Events in format YYYY-MM-DD=symbol (e.g., 2024-12-25=🎄)",
    )
    parser.add_argument(
        "--no-year",
        action="store_true",
        help="Hide year in header",
    )
    
    args = parser.parse_args()
    
    try:
        events = parse_events(args.events)
        calendar_output = generate_ascii_calendar(
            args.year, args.month, events, show_year=not args.no_year
        )
        print(calendar_output)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
