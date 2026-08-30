import json
import sys
import os

def load_items(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading items: {e}", file=sys.stderr)
        sys.exit(1)

def emoji_for(name):
    mapping = {
        "canned beans": "🥫",
        "bottled water": "💧",
        "first aid kit": "🩹",
        "flashlight": "🔦",
        "battery": "🔋",
        "radio": "📻",
        "knife": "🔪",
    }
    return mapping.get(name.lower(), "📦")

def generate_report(items):
    lines = ["🗃️ Scavenger Report", "--------------------"]
    for item in items:
        name = item.get("name", "unknown")
        qty = item.get("quantity", 1)
        lines.append(f"{emoji_for(name)} {name} x{qty}")
    return "\n".join(lines)

def main():
    path = os.getenv("ITEMS_PATH", "/app/items.json")
    items = load_items(path)
    report = generate_report(items)
    print(report)

if __name__ == "__main__":
    main()
