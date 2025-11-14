import sys

def get_apocalypse_mood(text: str) -> tuple[str, str]:
    """
    Analyzes the input text and returns its apocalyptic mood and corresponding color.
    Moods are prioritized from most severe to least severe.
    """
    text_lower = text.lower()

    # Define moods and their keywords, ordered by priority (most severe first)
    mood_definitions = [
        ("Impending Doom", "Red", [
            "apocalypse", "catastrophe", "collapse", "doomed", "end of world",
            "extinction", "ruin", "despair", "failure", "critical",
            "meltdown", "imminent", "fatal", "disaster", "crisis"
        ]),
        ("Slightly Uneasy", "Orange", [
            "warning", "concern", "risk", "unstable", "uncertain",
            "glitch", "bug", "issue", "alert", "monitor", "potential",
            "instability", "problem", "error"
        ]),
        ("Post-Apocalyptic Chill", "Blue", [
            "rebuild", "hope", "future", "peace", "calm", "restore",
            "recovery", "optimistic", "new beginning", "thrive", "growth",
            "serene", "tranquil"
        ]),
        ("Business as Usual", "Green", [
            "routine", "stable", "progress", "fix", "update",
            "completed", "success", "daily", "task", "working",
            "nominal", "operational", "functional"
        ])
    ]

    # Check for moods in order of priority
    for mood_name, color, keywords in mood_definitions:
        for keyword in keywords:
            if keyword in text_lower:
                return mood_name, color

    # If no specific mood keywords are found, check for general sentiment or default
    if not text.strip():
        return "Mysterious Void", "Purple"
    
    # If text exists but doesn't match specific keywords, default to Business as Usual
    return "Business as Usual", "Green"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/mood_ring.py \"<text_to_analyze>\"")
        sys.exit(1)

    input_text = sys.argv[1]
    mood, color = get_apocalypse_mood(input_text)
    print(f"Mood: {mood} ({color})")
