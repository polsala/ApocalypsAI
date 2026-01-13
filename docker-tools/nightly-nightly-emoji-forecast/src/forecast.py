import os
import sys
import random

def get_fake_weather(city: str) -> str:
    """Return a whimsical weather string for *city* using emojis."""
    conditions = ["☀️", "🌤️", "⛅", "🌧️", "⛈️", "❄️", "🌪️"]
    temps = ["🥶", "❄️", "🧊", "🌡️", "🔥", "🥵"]
    condition = random.choice(conditions)
    temp = random.choice(temps)
    return f"{city}: {condition} {temp}"

def main() -> None:
    city = os.getenv("CITY")
    if not city and len(sys.argv) > 1:
        city = sys.argv[1]
    if not city:
        print("Usage: set CITY env var or pass city name as argument", file=sys.stderr)
        sys.exit(1)
    print(get_fake_weather(city))

if __name__ == "__main__":
    main()

