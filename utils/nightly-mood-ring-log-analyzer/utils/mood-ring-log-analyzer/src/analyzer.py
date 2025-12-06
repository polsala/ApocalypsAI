import sys
import os

def analyze_log_content(log_content: str) -> dict:
    """
    Analyzes the given log content string and determines its 'mood'.
    """
    mood_counts = {
        'Calm': 0,       # INFO, DEBUG, NOTICE
        'Anxious': 0,    # WARNING, WARN
        'Critical': 0,   # ERROR, CRITICAL, FATAL
        'Mysterious': 0  # Unrecognized entries
    }

    keywords = {
        'Critical': ['ERROR', 'CRITICAL', 'FATAL'],
        'Anxious': ['WARNING', 'WARN'],
        'Calm': ['INFO', 'DEBUG', 'NOTICE']
    }

    lines = log_content.splitlines()
    if not lines:
        return {
            'mood_counts': mood_counts,
            'overall_mood': 'SERENE',
            'message': 'The log is utterly serene. Nothing to report!'
        }

    for line in lines:
        line_classified = False
        # Check for critical, anxious, then calm keywords in order of priority
        for mood_type, kws in keywords.items():
            if any(kw in line.upper() for kw in kws):
                mood_counts[mood_type] += 1
                line_classified = True
                break
        if not line_classified:
            mood_counts['Mysterious'] += 1

    overall_mood = 'SERENE'
    message = 'The log is utterly serene. Nothing to report!'

    # Determine overall mood based on priority
    if mood_counts['Critical'] > 0:
        overall_mood = 'CRITICAL'
        message = 'The air crackles with criticality! Immediate attention required!'
    elif mood_counts['Anxious'] > 0:
        overall_mood = 'ANXIOUS'
        message = 'The air feels a bit tense. Some warnings are present, but no critical failures yet. Keep an eye on things!'
    elif mood_counts['Calm'] > 0:
        overall_mood = 'CALM'
        message = 'A wave of calm washes over the system. All seems well.'
    elif mood_counts['Mysterious'] > 0:
        overall_mood = 'MYSTERIOUS'
        message = 'The system feels... enigmatic. Unrecognized entries abound. Investigation might be warranted.'

    return {
        'mood_counts': mood_counts,
        'overall_mood': overall_mood,
        'message': message
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <path_to_log_file>")
        sys.exit(1)

    log_file_path = sys.argv[1]

    if not os.path.exists(log_file_path):
        print(f"Error: Log file not found at '{log_file_path}'")
        sys.exit(1)

    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            log_content = f.read()
    except Exception as e:
        print(f"Error reading log file '{log_file_path}': {e}")
        sys.exit(1)

    print(f"Analyzing log file: {log_file_path}\n")
    analysis = analyze_log_content(log_content)

    print("--- Mood-Ring Log Analysis ---")
    print("\nMood Counts:")
    for mood, count in analysis['mood_counts'].items():
        print(f"  {mood}: {count}")

    print(f"\nOverall System Mood: {analysis['overall_mood']}")
    print(f"\n{analysis['message']}")

if __name__ == '__main__':
    main()
