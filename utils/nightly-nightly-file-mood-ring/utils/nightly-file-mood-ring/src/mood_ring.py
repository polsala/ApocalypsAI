import sys
import os

def get_file_mood(filepath: str) -> tuple[str, str]:
    """
    Analyzes a file's content and returns a mood emoji and description.
    """
    if not os.path.exists(filepath):
        return "❓", "Mysterious Void - File not found."
    if not os.path.isfile(filepath):
        return "❓", "Mysterious Void - Not a regular file."

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        return "❓", "Mysterious Void - Could not read file."

    lines = content.splitlines()
    line_count = len(lines)
    lower_content = content.lower()

    # Keyword counts
    todo_fixme_count = lower_content.count('todo') + lower_content.count('fixme') + lower_content.count('bug')
    error_critical_count = lower_content.count('error') + lower_content.count('critical')
    positive_count = lower_content.count('clean') + lower_content.count('simple') + lower_content.count('success')
    deprecated_count = lower_content.count('deprecated') + lower_content.count('stale')

    # Mood determination logic (order matters for precedence)
    if line_count == 0:
        return "❓", "Mysterious Void - The file is empty."
    
    if error_critical_count >= 3:
        return "💀", "Critical Collapse - This file indicates severe problems."
    
    if todo_fixme_count >= 5:
        return "🔥", "Fiery Frontier - This file is bustling with activity, possibly needing attention or refactoring."

    if deprecated_count >= 2:
        return "🧊", "Icy Inertia - This file seems stale or deprecated."

    if positive_count >= 2 and todo_fixme_count == 0 and error_critical_count == 0:
        return "✨", "Sparkling Serenity - This file is a beacon of clarity and simplicity."

    if line_count < 10 and todo_fixme_count == 0 and error_critical_count == 0:
        return "🌿", "Budding Bloom - A healthy, growing file with a balanced disposition."

    return "🚧", "Under Construction - This file is a work in progress or has general content."


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python src/mood_ring.py <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    emoji, description = get_file_mood(filepath)
    print(f"File Mood: {emoji} {description}")
