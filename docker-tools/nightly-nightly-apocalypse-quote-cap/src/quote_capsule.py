#!/usr/bin/env python3
import sys, json, base64, datetime

def encode(text):
    return {
        "quote": text,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "encoded": base64.b64encode(text.encode()).decode()
    }

def decode(b64):
    try:
        decoded = base64.b64decode(b64).decode()
        return {"decoded": decoded}
    except Exception as e:
        return {"error": str(e)}

def main():
    if "--decode" in sys.argv:
        b64 = sys.stdin.read().strip()
        result = decode(b64)
    else:
        text = sys.stdin.read().strip()
        result = encode(text)
    json.dump(result, sys.stdout)

if __name__ == "__main__":
    main()

