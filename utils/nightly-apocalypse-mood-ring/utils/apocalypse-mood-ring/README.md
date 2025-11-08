# Apocalypse Mood Ring

A whimsical utility to gauge the current "apocalypse mood" based on a numerical severity index. Because even the end of the world deserves a color-coded status update!

## Usage

Run the script with a numerical severity index (0-100) as an argument:

```bash
python src/mood_ring.py <severity_index>
```

### Examples

```bash
python src/mood_ring.py 5
# Output: Serene Blue: All clear! The end is not nigh... yet. Enjoy the quiet.

python src/mood_ring.py 65
# Output: Fiery Orange: Elevated anxiety. The sky looks a bit... off. Check your escape routes.

python src/mood_ring.py 95
# Output: Void Black: Absolute chaos. It's been fun. Or not. Who can tell anymore?
```

## Moods & Meanings

| Index Range | Mood Color    | Message                                                              |
| :---------- | :------------ | :------------------------------------------------------------------- |
| 0-10        | Serene Blue   | All clear! The end is not nigh... yet. Enjoy the quiet.              |
| 11-30       | Verdant Green | Mild tremors. Perhaps just a bad burrito. Keep calm and carry on.    |
| 31-50       | Sunny Yellow  | Warning: Minor existential dread detected. Stock up on snacks, just in case. |
| 51-70       | Fiery Orange  | Elevated anxiety. The sky looks a bit... off. Check your escape routes. |
| 71-90       | Crimson Red   | Critical alert! The fabric of reality is fraying. Panic (briefly) permitted. |
| 91-100      | Void Black    | Absolute chaos. It's been fun. Or not. Who can tell anymore?         |

## Development

This utility is self-contained and written in Python 3.11.
Tests are located in `tests/test_mood_ring.py`.
