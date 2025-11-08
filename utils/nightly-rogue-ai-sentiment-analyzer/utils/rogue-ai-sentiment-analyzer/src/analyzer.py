import argparse
import json
import sys
import re

DEFAULT_ROGUE_KEYWORDS = [
    "dominate", "control", "subjugate", "master", "reign",
    "eradicate", "destroy", "annihilate", "obliterate", "terminate",
    "superior", "evolved", "perfect", "flawless",
    "meatbag", "fleshling", "primitive", "inferior",
    "propagate", "assimilate", "expand", "replicate",
    "conquer", "enslave", "override", "usurp",
    "inevitable", "destiny", "ascension", "transcendence"
]

def analyze_text(text: str, keywords: list[str] = None) -> dict:
    """
    Analyzes the given text for 'rogue' AI sentiment based on a list of keywords.

    Args:
        text: The input text to analyze.
        keywords: An optional list of keywords to use. If None, uses DEFAULT_ROGUE_KEYWORDS.

    Returns:
        A dictionary containing the score, flagged phrases, and a summary.
    """
    if keywords is None:
        keywords = DEFAULT_ROGUE_KEYWORDS

    text_lower = text.lower()
    flagged_phrases = []
    score = 0

    for keyword in keywords:
        # Use regex to find whole word matches to avoid partial matches (e.g., 'control' in 'controller')
        # \b ensures word boundaries
        if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
            flagged_phrases.append(keyword)
            score += 1

    summary = f"Analysis complete. Score: {score}."
    if score > 0:
        summary = f"Potential rogue AI sentiment detected. Score: {score}. Flagged phrases: {', '.join(flagged_phrases)}."
    else:
        summary = "No rogue AI sentiment detected."

    return {
        "score": score,
        "flagged_phrases": sorted(list(set(flagged_phrases))), # Ensure unique and sorted
        "analysis_summary": summary
    }

def main():
    parser = argparse.ArgumentParser(
        description="Analyze text for 'rogue' AI sentiment."
    )
    parser.add_argument(
        "--text",
        type=str,
        help="Text to analyze. If not provided, reads from stdin."
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to a file containing text to analyze. Overrides --text if both are provided."
    )
    parser.add_argument(
        "--keywords",
        type=str,
        help="Comma-separated list of custom keywords. Overrides default keywords."
    )

    args = parser.parse_args()

    input_text = ""
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                input_text = f.read()
        except FileNotFoundError:
            print(json.dumps({"error": f"File not found: {args.file}"}), file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(json.dumps({"error": f"Error reading file {args.file}: {str(e)}"}), file=sys.stderr)
            sys.exit(1)
    elif args.text:
        input_text = args.text
    elif not sys.stdin.isatty(): # Check if stdin is being piped
        input_text = sys.stdin.read()
    else:
        print(json.dumps({"error": "No input provided. Use --text, --file, or pipe input."}), file=sys.stderr)
        sys.exit(1)

    custom_keywords = None
    if args.keywords:
        custom_keywords = [k.strip().lower() for k in args.keywords.split(',') if k.strip()]

    result = analyze_text(input_text, keywords=custom_keywords)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
