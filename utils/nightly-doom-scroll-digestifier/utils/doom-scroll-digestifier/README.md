# Doom Scroll Digestifier

## Overview

The `Doom Scroll Digestifier` is a whimsical-yet-useful command-line utility designed to help you navigate the relentless tide of "doom and gloom" news. In an age where information overload can lead to anxiety, this tool aims to provide a concise, thematic summary of simulated current events, allowing you to grasp the gist without getting lost in the overwhelming details.

It's like having a tiny, slightly cynical, but ultimately helpful AI assistant filter the noise, leaving you with just the essential (and perhaps a touch less soul-crushing) takeaways.

## Features

*   **Simulated News Stream Processing**: Takes a list of mock news headlines/articles.
*   **Keyword-Based Analysis**: Identifies key themes and sentiment (doom vs. resilience).
*   **Concise Summarization**: Generates a brief digest, focusing on core issues.
*   **Offline & Self-Contained**: No external APIs or internet connection required for operation.

## Installation

This utility is self-contained and written in Python 3.11+. No special installation steps are required beyond having a compatible Python interpreter.

1.  Navigate to the `utils/doom-scroll-digestifier/` directory.
2.  Ensure you have Python 3.11 or newer installed.

## Usage

Run the `digestifier.py` script directly from the `src/` directory.

```bash
python src/digestifier.py
```

The script will process a predefined set of mock news items and print a summary to the console. For a more interactive experience or to process custom inputs, you would modify the `main` function in `digestifier.py`.

### Example Output

```
--- Doom Scroll Digest ---
Date: 2242-10-27

Key Themes:
- Global climate shifts and environmental degradation
- Economic instability and resource scarcity
- Geopolitical tensions and social unrest
- Public health challenges
- Technological advancements and innovative solutions
- Community resilience and adaptive strategies
- Sustainable development and mitigation efforts

Overall Sentiment:
A mixed bag of challenges and emerging solutions. The future remains fluid, requiring adaptive strategies.
```

## Development & Testing

To run the automated tests:

```bash
python -m unittest tests/test_digestifier.py
```
