import sys

def analyze_mood(text: str) -> str:
    """
    Analyzes the given text and returns an 'apocalypse mood'.
    """
    text_lower = text.lower()

    mood_keywords = {
        "Doom & Gloom": ["doom", "despair", "hopeless", "end", "dark", "bleak", "futility", "dread"],
        "Prepper Panic": ["stockpile", "bunker", "survival", "hoard", "ration", "emergency", "collapse", "prepare"],
        "Optimistic Oblivion": ["bright side", "new beginning", "opportunity", "rebirth", "hope", "silver lining", "adventure", "dawn"],
        "Chill Chaos": ["whatever", "chill", "relax", "meh", "inevitable", "accept", "zen", "serene", "flow"]
    }

    for mood, keywords in mood_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                return mood

    return "Neutral Numbness"

def main():
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
    else:
        # Read from stdin if no command-line argument
        input_text = sys.stdin.read().strip()

    if not input_text:
        print("Please provide text to analyze. Usage: python mood_analyzer.py \"Your text\" or echo \"Your text\" | python mood_analyzer.py")
        sys.exit(1)

    mood = analyze_mood(input_text)
    print(f"Current Apocalypse Mood: {mood}")

if __name__ == "__main__":
    main()
