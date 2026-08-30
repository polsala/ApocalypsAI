import json
import sys
from pathlib import Path

def load_items(path: Path):
    with path.open() as f:
        data = json.load(f)
    return data.get("items", [])

def prioritize(items):
    # Sort by importance descending, then quantity descending
    return sorted(items, key=lambda i: (-i.get("importance", 0), -i.get("quantity", 0)))

def format_checklist(items):
    lines = []
    for idx, item in enumerate(items, start=1):
        lines.append(f"{idx}. {item['name']} (Qty: {item['quantity']}) - Importance: {item['importance']}")
    return "\n".join(lines)

def main():
    input_path = Path("supplies.json")
    if not input_path.exists():
        print("Error: supplies.json not found in /app", file=sys.stderr)
        sys.exit(1)
    items = load_items(input_path)
    prioritized = prioritize(items)
    print(format_checklist(prioritized))

if __name__ == "__main__":
    main()
