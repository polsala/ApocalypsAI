import argparse
import re
import os

def summarize_text(text_content: str, max_sentences: int = 5, min_sentence_length: int = 50) -> list[str]:
    """
    Extracts key sentences from a given text content to form a summary.

    Args:
        text_content: The full text content to summarize.
        max_sentences: The maximum number of sentences to include in the summary.
        min_sentence_length: The minimum character length a sentence must have to be considered.

    Returns:
        A list of strings, where each string is a key sentence from the summary.
    """
    if not text_content:
        return []

    # Split text into sentences using common delimiters. 
    # This regex handles periods, exclamation marks, and question marks, 
    # ensuring they are followed by a space or end of string.
    sentences = re.split(r'(?<=[.!?])\s+', text_content)

    # Filter sentences based on minimum length and remove leading/trailing whitespace
    filtered_sentences = [
        s.strip()
        for s in sentences
        if len(s.strip()) >= min_sentence_length
    ]

    # Take the first 'max_sentences' from the filtered list
    summary_sentences = filtered_sentences[:max_sentences]

    return summary_sentences

def main():
    parser = argparse.ArgumentParser(
        description="Distill lengthy text files into concise, actionable summaries."
    )
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to the text file to summarize."
    )
    parser.add_argument(
        "--max-sentences",
        type=int,
        default=5,
        help="Maximum number of sentences to include in the summary (default: 5)."
    )
    parser.add_argument(
        "--min-length",
        type=int,
        default=50,
        help="Minimum character length for a sentence to be considered (default: 50)."
    )

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File not found at '{args.file}'")
        exit(1)

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file '{args.file}': {e}")
        exit(1)

    summary = summarize_text(content, args.max_sentences, args.min_length)

    print(f"Summary of {os.path.basename(args.file)}:")
    if summary:
        for sentence in summary:
            print(f"- {sentence}")
    else:
        print("No significant sentences found to summarize.")


if __name__ == "__main__":
    main()
