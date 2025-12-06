import sys
import argparse

def analyze_text(text: str) -> tuple[int, str]:
    """
    Analyzes the sentiment of the given text and returns a score and a whimsical mood.
    """
    text_lower = text.lower()
    score = 0

    positive_keywords = {
        "success": 3, "complete": 2, "done": 1, "yay": 3, "good": 1,
        "excellent": 3, "happy": 2, "optimistic": 2, "thrive": 2,
        "perfect": 3, "achieved": 2, "resolved": 2, "smooth": 1
    }
    negative_keywords = {
        "error": -3, "fail": -3, "bug": -2, "issue": -1, "problem": -2,
        "crash": -3, "sad": -2, "grumpy": -2, "frustrated": -2, "broken": -3,
        "blocked": -2, "stuck": -1, "warning": -1, "critical": -3, "abort": -2
    }
    # Neutral keywords don't change score but can influence mood if score is near zero
    # For simplicity, we'll just use score for now.

    for keyword, value in positive_keywords.items():
        if keyword in text_lower:
            score += value
    for keyword, value in negative_keywords.items():
        if keyword in text_lower:
            score += value

    if score >= 5:
        mood = "Ecstatic & Harmonious"
    elif score >= 1:
        mood = "Content & Productive"
    elif score == 0:
        mood = "Pondering & Observing"
    elif score <= -5:
        mood = "Meltdown Imminent!"
    else: # score between -1 and -4
        mood = "Grumpy & Frustrated"

    return score, mood

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI's AI-Whisperer Mood Ring: Analyze text sentiment."
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Text to analyze, or '-' to read from stdin. If omitted, reads from stdin."
    )
    args = parser.parse_args()

    if args.input and args.input != '-':
        text_to_analyze = args.input
    else:
        text_to_analyze = sys.stdin.read()

    if not text_to_analyze.strip():
        print("No input text provided for analysis.")
        sys.exit(1)

    score, mood = analyze_text(text_to_analyze)
    print(f"ApocalypsAI Mood Ring Analysis:")
    print(f"  Text: '{text_to_analyze.strip()[:70]}...'" if len(text_to_analyze.strip()) > 70 else f"  Text: '{text_to_analyze.strip()}'")
    print(f"  Sentiment Score: {score}")
    print(f"  Current Mood: {mood}")

if __name__ == "__main__":
    main()
