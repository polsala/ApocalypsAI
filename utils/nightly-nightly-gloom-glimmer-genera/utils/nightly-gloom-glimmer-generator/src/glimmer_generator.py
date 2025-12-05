import sys
import argparse

GLOOM_TO_GLIMMER = {
    "lost": "An opportunity to discover new paths and redefine what truly matters.",
    "broken": "A chance to rebuild stronger, to innovate and improve upon the past.",
    "fear": "Awareness to act cautiously, a signal to prepare and protect.",
    "despair": "The lowest point often precedes the greatest rise; a catalyst for change.",
    "empty": "Space for new beginnings, a canvas awaiting fresh strokes.",
    "ruin": "A blank canvas for new beginnings, a chance to build something stronger.",
    "struggle": "Every challenge overcome makes us stronger and more resilient.",
    "darkness": "The stars shine brightest in the deepest night; a prelude to dawn.",
    "failure": "A valuable lesson learned, a stepping stone towards future success.",
    "scarce": "An invitation to innovate, to conserve, and to appreciate what we have.",
    "alone": "An opportunity for self-discovery, or a chance to forge new, deeper connections.",
    "exhausted": "A reminder to rest, recharge, and appreciate the strength you've shown.",
    "uncertainty": "The fertile ground for possibility, where new futures are shaped.",
    "tough": "Every challenge overcome makes us stronger and more resilient."
}

def find_glimmers(text: str) -> list[tuple[str, str]]:
    """
    Identifies 'gloom' keywords in the text and returns their corresponding 'glimmers'.
    """
    found_glimmers = []
    text_lower = text.lower()
    for gloom_word, glimmer_message in GLOOM_TO_GLIMMER.items():
        if gloom_word in text_lower:
            found_glimmers.append((gloom_word, glimmer_message))
    return found_glimmers

def generate_glimmer_report(text: str) -> str:
    """
    Generates a report with identified glimmers or a general positive message.
    """
    glimmers = find_glimmers(text)
    report_lines = [f"Original Text: \"{text}\"", "✨ Glimmer of Hope:"]

    if glimmers:
        for gloom, glimmer in glimmers:
            report_lines.append(f"  - Gloom: \"{gloom}\" -> Glimmer: \"{glimmer}\"")
    else:
        report_lines.append("  - No specific gloom detected, but remember: \"Even small victories are monumental steps forward.\"")
        report_lines.append("  - General encouragement: \"Keep going, for resilience is your greatest strength.\"")

    return "\n".join(report_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Find a glimmer of hope in any text.",
        epilog="If no text is provided as an argument, it will read from standard input."
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="The text to analyze for glimmers of hope."
    )
    args = parser.parse_args()

    input_text = args.text
    if input_text is None:
        if not sys.stdin.isatty(): # Check if stdin is piped
            input_text = sys.stdin.read().strip()
        else:
            print("Please provide text as an argument or via standard input.")
            sys.exit(1)

    if not input_text:
        print("No text provided to analyze.")
        sys.exit(1)

    print(generate_glimmer_report(input_text))

if __name__ == "__main__":
    main()
