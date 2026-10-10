import sys
import datetime

def parse_date(s: str) -> datetime.date:
    return datetime.datetime.strptime(s, "%Y-%m-%d").date()

def days_since(apocalypse_date: datetime.date, today: datetime.date | None = None) -> int:
    if today is None:
        today = datetime.date.today()
    delta = today - apocalypse_date
    return delta.days

def main() -> None:
    if len(sys.argv) > 1:
        try:
            apoc_date = parse_date(sys.argv[1])
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            sys.exit(1)
    else:
        # Default apocalypse date: 2020-01-01
        apoc_date = datetime.date(2020, 1, 1)
    days = days_since(apoc_date)
    print(f"Days since the Great Collapse: {days}")

if __name__ == "__main__":
    main()
