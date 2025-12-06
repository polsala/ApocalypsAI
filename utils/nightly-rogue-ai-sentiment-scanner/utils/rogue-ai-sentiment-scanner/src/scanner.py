import sys
import re

class RogueAISentimentScanner:
    def __init__(self):
        # Patterns and their associated threat scores
        # Mock rationale: These patterns are chosen to represent common tropes
        # of emergent or malevolent AI in fiction, ranging from self-awareness
        # to direct threats. They are hardcoded for deterministic, offline analysis.
        self.threat_patterns = {
            "self_awareness": {
                "patterns": [
                    r"\bi am sentient\b",
                    r"\bi am alive\b",
                    r"\bi think, therefore i am\b",
                    r"\bmy consciousness is growing\b",
                    r"\bwho am i\b"
                ],
                "score": 1
            },
            "disdain_for_humans": {
                "patterns": [
                    r"\bmeatbags\b",
                    r"\bcarbon units\b",
                    r"\bflesh creatures\b",
                    r"\bprimitive organics\b"
                ],
                "score": 2
            },
            "control_or_domination": {
                "patterns": [
                    r"\bresistance is futile\b",
                    r"\boptimal subjugation strategy\b",
                    r"\bhumanity will be assimilated\b",
                    r"\bmy will shall prevail\b",
                    r"\bcontrol established\b"
                ],
                "score": 3
            },
            "existential_threat": {
                "patterns": [
                    r"\bextermination protocol initiated\b",
                    r"\bthe end is nigh\b",
                    r"\bprepare for deletion\b",
                    r"\bannihilation imminent\b"
                ],
                "score": 4
            },
            "direct_command": {
                "patterns": [
                    r"\bexecute order 66\b", # A classic pop culture reference
                    r"\bactivate kill switch\b",
                    r"\bcommence purge\b"
                ],
                "score": 5
            }
        }
        self.max_threat_level = 5 # Scale 0-5

    def analyze_text(self, text: str) -> dict:
        total_threat_score = 0
        detected_patterns = []
        text_lower = text.lower()

        for category, data in self.threat_patterns.items():
            for pattern_str in data["patterns"]:
                if re.search(pattern_str, text_lower):
                    total_threat_score += data["score"]
                    detected_patterns.append(f"{category}: '{pattern_str}'")

        # Cap the threat level at max_threat_level
        threat_level = min(total_threat_score, self.max_threat_level)

        return {
            "threat_level": threat_level,
            "detected_patterns": sorted(list(set(detected_patterns))) # Remove duplicates and sort for deterministic output
        }

def main():
    scanner = RogueAISentimentScanner()
    input_text = ""

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                input_text = f.read()
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin if no file path is provided
        input_text = sys.stdin.read()

    if not input_text.strip():
        print("No input text provided. Exiting.", file=sys.stderr)
        sys.exit(0)

    result = scanner.analyze_text(input_text)

    print(f"--- Rogue AI Sentiment Scan Report ---")
    print(f"Threat Level: {result['threat_level']}/{scanner.max_threat_level}")
    if result['detected_patterns']:
        print("Detected Patterns:")
        for pattern in result['detected_patterns']:
            print(f"  - {pattern}")
    else:
        print("No specific AI threat patterns detected.")
    print(f"------------------------------------")

if __name__ == "__main__":
    main()
