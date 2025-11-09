import argparse
import sys
import re

def dedramatize_text(text: str) -> str:
    """
    Filters and rephrases alarming text to reduce sensationalism and promote
    a more resilient perspective.
    """
    # Define replacement rules (order matters for some rules)
    # More specific rules should come before more general ones if they overlap.
    replacements = {
        r'\bcatastrophe\b': 'significant challenge',
        r'\bdisaster\b': 'serious situation',
        r'\bcrisis\b': 'critical event',
        r'\bchaos\b': 'disruption',
        r'\bdespair\b': 'concern',
        r'\bpanic\b': 'apprehension',
        r'\balarming\b': 'noteworthy',
        r'\burgent\b': 'proactive measures are advisable',
        r'\bbreaking\b': 'update',
        r'\bthreatens to devastate\b': 'poses a considerable challenge to',
        r'\bplunging the world into\b': 'leading to a period of',
        r'\bcollapse\b': 'downturn',
        r'\bcollapsing\b': 'experiencing a downturn',
        r'\bfragile society\b': 'interconnected community',
        r'\bwidespread\b': 'broad',
        r'\birreversible damage\b': 'significant impact',
        r'\bavert total\b': 'navigate the',
        r'!\s*!*': '.', # Reduce multiple exclamation marks to a single period
        r'\s+': ' ', # Normalize multiple spaces
    }

    # Apply replacements
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # Add a resilience-focused closing statement if the text still sounds negative
    # This is a simple heuristic; more advanced NLP would be needed for true sentiment analysis.
    negative_keywords = ['challenge', 'situation', 'concern', 'disruption', 'apprehension', 'impact']
    if any(keyword in text.lower() for keyword in negative_keywords):
        if not text.strip().endswith('.'):
            text += '.'
        text += ' Remember, adaptability is key.'
        # Ensure we don't add it multiple times if the text is processed repeatedly
        text = text.replace('Remember, adaptability is key. Remember, adaptability is key.', 'Remember, adaptability is key.')


    return text.strip()

def main():
    parser = argparse.ArgumentParser(
        description="De-dramatize alarming text to promote a more resilient perspective."
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="The text string to de-dramatize. If not provided, reads from --file or stdin."
    )
    parser.add_argument(
        "--file",
        "-f",
        help="Path to a file containing the text to de-dramatize."
    )

    args = parser.parse_args()

    input_text = ""
    if args.text:
        input_text = args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                input_text = f.read()
        except FileNotFoundError:
            print(f"Error: File not found at '{args.file}'", file=sys.stderr)
            sys.exit(1)
    elif not sys.stdin.isatty(): # Check if stdin is being piped
        input_text = sys.stdin.read()
    else:
        print("Error: No input text provided. Use a string argument, --file, or pipe input.", file=sys.stderr)
        sys.exit(1)

    if not input_text.strip():
        print("Warning: Input text is empty. Nothing to de-dramatize.", file=sys.stderr)
        sys.exit(0)

    dedramatized_output = dedramatize_text(input_text)
    print(dedramatized_output)

if __name__ == "__main__":
    main()
