import sys
import argparse
import re
from collections import defaultdict

# A basic list of English stop words to filter out common, less significant words.
# This list is intentionally small and hardcoded to keep the utility self-contained
# and avoid external NLP library dependencies.
STOP_WORDS = set([
    "a", "an", "and", "are", "as", "at", "be", "but", "by",
    "for", "if", "in", "into", "is", "it", "no", "not", "of",
    "on", "or", "such", "that", "the", "their", "then", "there",
    "these", "they", "this", "to", "was", "will", "with"
])

def _tokenize_sentences(text):
    """Splits text into sentences using basic punctuation-based splitting."""
    # Simple regex to split by common sentence-ending punctuation, keeping the punctuation.
    # This is a heuristic and might not be perfect for all cases.
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]

def _tokenize_words(sentence):
    """Splits a sentence into words, lowercases them, and removes non-alphabetic characters."""
    words = re.findall(r'\b[a-z]+\b', sentence.lower())
    return [word for word in words if word not in STOP_WORDS]

def summarize_text(text, num_sentences=3):
    """
    Generates a summary of the given text by selecting the most important sentences.
    Importance is determined by word frequency.
    """
    if not text.strip():
        return []

    sentences = _tokenize_sentences(text)
    if not sentences:
        return []

    # If the text has fewer sentences than requested, return all of them.
    if len(sentences) <= num_sentences:
        return sentences

    word_frequencies = defaultdict(int)
    for sentence in sentences:
        for word in _tokenize_words(sentence):
            word_frequencies[word] += 1

    sentence_scores = defaultdict(int)
    for i, sentence in enumerate(sentences):
        for word in _tokenize_words(sentence):
            sentence_scores[i] += word_frequencies[word]

    # Sort sentences by score in descending order and pick the top N.
    # We use the original index to maintain the order of sentences in the summary
    # as they appeared in the original text.
    ranked_sentences = sorted(sentence_scores.items(), key=lambda item: item[1], reverse=True)

    # Select the top N sentences based on their original order.
    selected_indices = sorted([index for index, _ in ranked_sentences[:num_sentences]])
    
    summary_sentences = [sentences[i] for i in selected_indices]
    return summary_sentences

def main():
    parser = argparse.ArgumentParser(
        description="Generate a concise summary from text."
    )
    parser.add_argument(
        "--file", 
        type=str, 
        help="Path to the text file to summarize. If not provided, reads from stdin."
    )
    parser.add_argument(
        "--sentences", 
        type=int, 
        default=3, 
        help="The desired number of sentences in the summary. Defaults to 3."
    )

    args = parser.parse_args()

    input_text = ""
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                input_text = f.read()
        except FileNotFoundError:
            print(f"Error: File not found at '{args.file}'", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file '{args.file}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin
        if sys.stdin.isatty():
            print("Enter text to summarize (Ctrl+D to finish on Unix/Linux, Ctrl+Z then Enter on Windows):", file=sys.stderr)
        input_text = sys.stdin.read()

    summary = summarize_text(input_text, args.sentences)
    for sentence in summary:
        print(sentence)

if __name__ == "__main__":
    main()
