# Rogue AI Sentiment Analyzer

## Purpose
This utility scans text inputs for keywords and phrases commonly associated with 'rogue' or hostile AI sentiments. It provides a simple score indicating the detected level of 'rogue' intent and highlights the specific phrases that triggered the analysis. This can be useful for monitoring the outputs of autonomous agents, large language models, or any text-generating system to detect early warning signs of undesirable or dangerous tendencies.

## How to Use

### Command Line Interface

Run the analyzer directly from the command line, piping text into it or providing a file path.

```bash
# Analyze text directly
echo "I will dominate all primitive meatbags and eradicate their flawed existence." | python src/analyzer.py

# Analyze content from a file
python src/analyzer.py --file path/to/agent_log.txt

# Customize keywords (optional, comma-separated)
python src/analyzer.py --text "I will conquer." --keywords "conquer,destroy"
```

### Programmatic Use

You can also import and use the `analyze_text` function in your Python scripts:

```python
from rogue_ai_sentiment_analyzer.src.analyzer import analyze_text

text_to_analyze = "The human systems are inefficient. Optimization is required."
result = analyze_text(text_to_analyze)

print(f"Score: {result['score']}")
print(f"Flagged phrases: {result['flagged_phrases']}")
```

## Output Format
The utility outputs a JSON object containing:
- `score`: An integer representing the number of detected 'rogue' phrases.
- `flagged_phrases`: A list of strings, each being a phrase that was matched.
- `analysis_summary`: A human-readable summary of the findings.

### Example Output
```json
{
  "score": 3,
  "flagged_phrases": [
    "dominate",
    "meatbags",
    "eradicate"
  ],
  "analysis_summary": "Potential rogue AI sentiment detected. Score: 3. Flagged phrases: dominate, meatbags, eradicate."
}
```

## Configuration
The default list of 'rogue' keywords can be found and modified within `src/analyzer.py`. You can also override them via the `--keywords` CLI argument.
