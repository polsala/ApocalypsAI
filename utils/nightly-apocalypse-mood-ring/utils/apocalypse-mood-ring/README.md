# Apocalypse Mood Ring

## Overview

The `apocalypse-mood-ring` is a whimsical utility designed to analyze any given text input and assign it an 'apocalyptic mood' along with a corresponding color code. Ever wonder if your commit message is radiating 'Impending Doom' or 'Post-Apocalyptic Chill'? This tool has you covered!

It's perfect for adding a touch of thematic flair to your CI/CD pipelines, log analysis, or just for fun.

## Usage

Run the utility from your terminal, passing the text you want to analyze as an argument:

```bash
python src/mood_ring.py "Your text goes here, perhaps a commit message or a log entry."
```

### Examples

```bash
python src/mood-ring.py "Critical system failure detected. The end is nigh!"
# Output: Mood: Impending Doom (Red)

python src/mood-ring.py "Minor network instability, monitoring situation."
# Output: Mood: Slightly Uneasy (Orange)

python src/mood-ring.py "Daily backup completed successfully. All systems nominal."
# Output: Mood: Business as Usual (Green)

python src/mood-ring.py "After the great reboot, we're rebuilding stronger than ever! Feeling optimistic."
# Output: Mood: Post-Apocalyptic Chill (Blue)

python src/mood-ring.py ""
# Output: Mood: Mysterious Void (Purple)
```

## Moods & Colors

*   **Impending Doom**: Red
*   **Slightly Uneasy**: Orange
*   **Business as Usual**: Green
*   **Post-Apocalyptic Chill**: Blue
*   **Mysterious Void**: Purple
