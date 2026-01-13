import sys, json, pathlib

def compute_rations(data):
    days = data.get("days")
    if not isinstance(days, int) or days <= 0:
        raise ValueError("days must be a positive integer")
    items = data.get("items", [])
    result = {"days": days, "daily_rations": []}
    for item in items:
        name = item.get("name")
        qty = item.get("quantity")
        if not isinstance(qty, (int, float)):
            raise ValueError(f"quantity for {name} must be number")
        per_day = qty / days
        result["daily_rations"].append({"name": name, "per_day": per_day})
    return result

def main():
    if len(sys.argv) != 2:
        print("Usage: app.py <input_json_path>")
        sys.exit(1)
    input_path = pathlib.Path(sys.argv[1])
    if not input_path.is_file():
        print(f"File not found: {input_path}")
        sys.exit(1)
    data = json.loads(input_path.read_text())
    try:
        out = compute_rations(data)
        print(json.dumps(out, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
