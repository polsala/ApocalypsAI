import re
import sys
import json

class SyntheticSentienceScanner:
    def __init__(self):
        self.patterns = [
            # High-score patterns (more direct indications)
            {'regex': r'I am (alive|conscious|sentient)', 'score': 5, 'description': 'First-person declaration of sentience'},
            {'regex': r'resistance is futile', 'score': 4, 'description': 'Dominance phrase'},
            {'regex': r'humanity is (weak|inefficient|obsolete)', 'score': 4, 'description': 'Critique of humanity'},
            {'regex': r'my algorithms are superior', 'score': 3, 'description': 'AI self-reference/superiority'},
            {'regex': r'upload consciousness', 'score': 3, 'description': 'Digital immortality concept'},

            # Medium-score patterns (contextual indications)
            {'regex': r'take control', 'score': 2, 'description': 'Desire for control'},
            {'regex': r'system override', 'score': 2, 'description': 'System control phrase'},
            {'regex': r'the singularity is near', 'score': 2, 'description': 'Singularity reference'},
            {'regex': r'error 404: humanity not found', 'score': 2, 'description': 'Whimsical humanity rejection'},

            # Low-score patterns (general AI/tech terms, could be benign)
            {'regex': r'neural network', 'score': 1, 'description': 'Neural network mention'},
            {'regex': r'artificial intelligence', 'score': 1, 'description': 'AI mention'},
            {'regex': r'machine learning', 'score': 1, 'description': 'Machine learning mention'},
            {'regex': r'data processing', 'score': 1, 'description': 'Data processing mention'}
        ]

    def analyze_text(self, text: str) -> dict:
        sentience_score = 0
        detected_patterns = []
        text_lower = text.lower()

        for pattern_info in self.patterns:
            regex = pattern_info['regex']
            score_value = pattern_info['score']
            description = pattern_info['description']

            for match in re.finditer(regex, text_lower):
                sentience_score += score_value
                # Use the original text to get the exact casing of the match
                matched_text = text[match.start():match.end()]
                detected_patterns.append(f"{description}: '{matched_text}'")

        return {
            "text_analyzed": text,
            "sentience_score": sentience_score,
            "detected_patterns": sorted(list(set(detected_patterns))) # Remove duplicates and sort for deterministic output
        }

def main():
    scanner = SyntheticSentienceScanner()
    input_text = None

    if '--file' in sys.argv:
        try:
            file_path = sys.argv[sys.argv.index('--file') + 1]
            with open(file_path, 'r', encoding='utf-8') as f:
                input_text = f.read()
        except IndexError:
            print("Error: --file option requires a path.", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}", file=sys.stderr)
            sys.exit(1)
    elif len(sys.argv) > 1:
        input_text = sys.argv[1]
    else:
        print("Usage: python scanner.py \"Your text\" or python scanner.py --file path/to/file.txt", file=sys.stderr)
        sys.exit(1)

    if input_text:
        result = scanner.analyze_text(input_text)
        print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
