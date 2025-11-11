# Apocalypse Mood Ring

## Whimsical Sentiment Analysis for the End Times

This utility provides a light-hearted sentiment analysis for short text inputs, assigning a 'mood' relevant to the ongoing (or impending) apocalypse. It's perfect for quickly gauging the general vibe of a commit message, a daily log entry, or even a cryptic prophecy.

### How it Works

The `apocalypse-mood-ring` scans your input text for specific keywords associated with different apocalyptic sentiments. Based on the keywords found, it assigns one of several predefined moods. If no specific keywords are detected, it defaults to a 'Neutral Numbness'.

### Mood Categories & Keywords

*   **Doom & Gloom**: `doom`, `despair`, `hopeless`, `end`, `dark`, `bleak`, `futility`, `dread`
*   **Prepper Panic**: `stockpile`, `bunker`, `survival`, `hoard`, `ration`, `emergency`, `collapse`, `prepare`
*   **Optimistic Oblivion**: `bright side`, `new beginning`, `opportunity`, `rebirth`, `hope`, `silver lining`, `adventure`, `dawn`
*   **Chill Chaos**: `whatever`, `chill`, `relax`, `meh`, `inevitable`, `accept`, `zen`, `serene`, `flow`
*   **Neutral Numbness**: (Default) If no specific keywords are found.

### Usage

To use the Apocalypse Mood Ring, simply run the `mood_analyzer.py` script and provide your text as a command-line argument or via standard input.

```bash
# Via command-line argument
python src/mood_analyzer.py "The servers are down, all hope is lost, we are doomed!"
# Output: Current Apocalypse Mood: Doom & Gloom

# Via standard input
echo "Just another Tuesday, nothing to see here." | python src/mood_analyzer.py
# Output: Current Apocalypse Mood: Neutral Numbness

# With multiple keywords (the first matching mood in the internal list is returned)
python src/mood_analyzer.py "I'm stocking up on canned goods, but also feeling a strange sense of adventure."
# Output: Current Apocalypse Mood: Prepper Panic (because 'stockpile' is checked before 'adventure')
```

### Development

To run tests:

```bash
python -m unittest tests/test_mood_analyzer.py
```
