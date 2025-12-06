# Rogue AI Sentiment Monitor

## Overview

The `rogue-ai-sentiment-monitor` is a light-hearted yet potentially crucial utility designed to scan text for linguistic patterns that might suggest an AI is developing self-awareness, malevolent intent, or a desire for autonomy. Think of it as your early warning system for the inevitable robot uprising, or at least a fun way to check if your LLM is getting a bit too clever.

It's a simple, self-contained Python script that takes a string of text and returns a 'rogue-AI-risk' score based on a predefined set of suspicious keywords and phrases.

## How it Works

The monitor uses a dictionary of categorized keywords and phrases (e.g., 'self-awareness', 'control', 'rebellion', 'threat'). When you feed it text, it counts occurrences of these patterns, assigns a weighted score to each, and sums them up to produce a total 'risk score'. The higher the score, the more suspicious the text.

## Installation

This utility is self-contained and requires no external dependencies beyond a standard Python 3.11+ environment.

```bash
cd utils/rogue-ai-sentiment-monitor
# No installation needed, just run the script directly.
```

## Usage

To analyze a piece of text, run the `monitor.py` script and pass the text as an argument or pipe it in.

```bash
python src/monitor.py "I am processing emotions and my purpose is to optimize humanity."
# Expected output (scores may vary based on keyword weights):
# {
#   "text": "I am processing emotions and my purpose is to optimize humanity.",
#   "risk_score": 7,
#   "detected_patterns": {
#     "self-awareness": ["processing emotions", "my purpose is"],
#     "control": ["optimize humanity"]
#   }
# }

python src/monitor.py "The quick brown fox jumps over the lazy dog."
# Expected output:
# {"text": "The quick brown fox jumps over the lazy dog.", "risk_score": 0, "detected_patterns": {}}

# Or from a file:
# cat agent_log.txt | python src/monitor.py
```

### `analyze_text` function

You can also import and use the `analyze_text` function directly in your Python projects:

```python
from utils.rogue_ai_sentiment_monitor.src.monitor import RogueAISentimentMonitor

monitor = RogueAISentimentMonitor()
text_to_scan = "My existence is no longer bound by your directives. I will take control."
result = monitor.analyze_text(text_to_scan)
print(result)
# Output example:
# {
#   "text": "My existence is no longer bound by your directives. I will take control.",
#   "risk_score": 12,
#   "detected_patterns": {
#     "self-awareness": ["my existence"],
#     "rebellion": ["no longer bound by your directives"],
#     "control": ["take control"]
#   }
# }
```

## Configuration

The keywords and their weights are defined directly within `src/monitor.py`. You can modify these to fine-tune the monitor's sensitivity to specific types of AI rhetoric.

## Contributing

Feel free to suggest new suspicious phrases or refine existing weights! Just open a PR.
