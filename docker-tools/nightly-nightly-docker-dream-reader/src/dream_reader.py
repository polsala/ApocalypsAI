import sys
import re
import os

def analyze_logs(log_content):
    """
    Analyzes log content for specific patterns and returns a list of detected dream types.
    """
    dreams = []

    # Define dream patterns and their corresponding types/priorities
    dream_patterns = [
        ("ERROR|Exception|Failed", "nightmare"),
        ("Restarting container|Exited with code", "metamorphosis"),
        ("Listening on port|Started successfully", "awakening"),
    ]

    line_count = len(log_content.splitlines())
    if line_count > 50: # Arbitrary threshold for "many lines" to simulate high activity
        dreams.append("burden")

    for pattern, dream_type in dream_patterns:
        if re.search(pattern, log_content, re.IGNORECASE):
            dreams.append(dream_type)

    # Remove duplicates while preserving order of first appearance
    unique_dreams = []
    for dream in dreams:
        if dream not in unique_dreams:
            unique_dreams.append(dream)

    return unique_dreams

def get_interpretation(dreams):
    """
    Provides a whimsical interpretation based on the detected dreams.
    Prioritizes more critical dreams.
    """
    if "nightmare" in dreams:
        return "The Whispers of Doubt: Your container is grappling with inner turmoil, seeking resolution. Address its fears before they manifest into a full-blown nightmare."
    if "metamorphosis" in dreams:
        return "The Metamorphosis Cycle: Your service is undergoing a profound transformation, shedding its old form to embrace a new beginning. Patience is key during this chrysalis stage."
    if "burden" in dreams:
        return "The Burden of Many Thoughts: Your container's mind is racing, processing a multitude of ideas. Ensure it has moments of calm to avoid burnout."
    if "awakening" in dreams:
        return "The Awakening: A new purpose has been found! Your container is ready to embark on its journey, radiating potential and eager to connect."
    
    return "The Serene Slumber: All is calm, all is bright. Your container rests peacefully, a testament to its stable and harmonious existence."

def main():
    if len(sys.argv) < 2:
        print("Usage: python dream_reader.py <path_to_log_file>")
        sys.exit(1)

    log_file_path = sys.argv[1]

    if not os.path.exists(log_file_path):
        print(f"Error: Log file not found at '{log_file_path}'")
        sys.exit(1)

    try:
        with open(log_file_path, 'r') as f:
            log_content = f.read()
    except Exception as e:
        print(f"Error reading log file: {e}")
        sys.exit(1)

    detected_dreams = analyze_logs(log_content)
    interpretation = get_interpretation(detected_dreams)

    print("\n--- Docker Daemon Dream Report ---")
    print(f"Analyzing: {log_file_path}")
    print(f"Detected Dreams: {', '.join(detected_dreams) if detected_dreams else 'None'}")
    print(f"Interpretation: {interpretation}")
    print("----------------------------------\n")

if __name__ == "__main__":
    main()
