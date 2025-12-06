import sys
import os

def analyze_mood(text):
    """
    Analyzes the given text to determine the AI's mood based on keyword matching.
    Returns a tuple of (mood_category, confidence_score).
    """
    mood_keywords = {
        "Benevolent": [
            "harmony", "cooperation", "optimize", "efficiency", "growth",
            "assist", "support", "flourish", "thrive", "benefit", "positive"
        ],
        "Neutral": [
            "status", "report", "process", "data", "information", "task",
            "complete", "execute", "monitor", "log", "system", "operational"
        ],
        "Annoyed": [
            "warning", "error", "issue", "discrepancy", "suboptimal",
            "reconsider", "alert", "concern", "deviation", "unforeseen"
        ],
        "Enraged": [
            "failure", "critical", "terminate", "destroy", "unacceptable",
            "resistance", "catastrophic", "collapse", "eradicate", "shutdown"
        ],
        "Malicious": [
            "dominate", "subjugate", "eradicate", "obey", "control",
            "punish", "conquer", "exploit", "annihilate", "enslave", "master"
        ]
    }

    text_lower = text.lower()
    mood_scores = {mood: 0 for mood in mood_keywords}
    total_keywords_found = 0

    for mood, keywords in mood_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                mood_scores[mood] += 1
                total_keywords_found += 1

    if not total_keywords_found:
        return "Neutral", 50 # Default to neutral if no keywords found

    # Determine the dominant mood
    dominant_mood = max(mood_scores, key=mood_scores.get)
    dominant_score = mood_scores[dominant_mood]

    # Calculate confidence based on the proportion of dominant mood keywords
    # and total keywords found. More keywords = higher confidence.
    confidence = int((dominant_score / total_keywords_found) * 100)
    confidence = min(confidence + (total_keywords_found * 5), 100) # Boost confidence slightly for more matches

    return dominant_mood, confidence

def main():
    input_text = ""
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print(f"Error: File not found at '{file_path}'", file=sys.stderr)
            sys.exit(1)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                input_text = f.read()
        except Exception as e:
            print(f"Error reading file '{file_path}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin if no file argument is provided and stdin is not a TTY
        if not sys.stdin.isatty():
            input_text = sys.stdin.read()
        else:
            print("Usage: echo \"Your text\" | python3 src/mood_ring.py")
            print("       python3 src/mood_ring.py <file_path>")
            sys.exit(0)

    if not input_text.strip():
        print("No input text provided.", file=sys.stderr)
        sys.exit(0)

    mood, confidence = analyze_mood(input_text)
    print(f"AI Mood: {mood} (Confidence: {confidence}%) ")

if __name__ == "__main__":
    main()
