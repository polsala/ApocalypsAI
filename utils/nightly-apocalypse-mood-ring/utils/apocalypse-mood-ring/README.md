# ApocalypsAI Mood Ring

A whimsical command-line utility to gauge your current "apocalypse readiness" and offer a lighthearted, actionable tip. Because even impending doom deserves a little self-reflection!

## Usage

Run the script directly:

```bash
python src/mood_ring.py
```

For deterministic results (useful for scripting or just reliving a specific doom level), you can provide a seed:

```bash
python src/mood_ring.py --seed 123
```

## Output Example

```
🔮 ApocalypsAI Mood Ring 🔮

Current Doom Level: 3/5 (😬 Slightly Anxious)
Your Apocalyptic Vibe: "Slightly Anxious"

Whimsical Tip: "Check your bunker's snack supply. Are the Twinkies still fresh!"
```

## How it Works

The utility randomly (or deterministically, if a seed is provided) selects a "doom level" and a corresponding "apocalyptic vibe" and "whimsical tip" from a predefined set. No actual doom-scrolling required!
