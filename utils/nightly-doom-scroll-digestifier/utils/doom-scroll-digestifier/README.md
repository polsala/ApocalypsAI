# Doom-Scroll Digestifier

## Overview

The `doom-scroll-digestifier` is a whimsical utility designed to help you navigate the often overwhelming and anxiety-inducing landscape of online news. It takes a URL to a news article, fetches its content, strips away the HTML, analyzes the text for 'doom' keywords, calculates a 'doom level' score, and provides a concise, less stressful summary.

Think of it as your personal digital filter against the relentless tide of bad news, offering a quick glance at the severity without diving headfirst into the abyss.

## Features

*   **URL Fetching**: Grabs content from any provided web URL.
*   **HTML Stripping**: Extracts plain text from HTML, removing clutter like scripts and styles.
*   **Doom Level Analysis**: Scans for predefined 'doom' keywords to assign a severity score (0-10).
*   **Concise Summarization**: Provides a brief summary of the article's core message.

## Installation

This utility is self-contained and written in Python 3.11. It requires the `requests` library.

```bash
pip install requests
```

## Usage

Run the `digestifier.py` script with the `--url` argument:

```bash
python src/digestifier.py --url "https://example.com/some-news-article"
```

### Example Output

```
Fetching content from: https://example.com/some-news-article

URL: https://example.com/some-news-article
Doom Level: 7/10 (Severe)
Summary: A recent report indicates a significant global challenge related to climate change, urging immediate action to mitigate potential long-term consequences. Experts highlight the urgency of international cooperation.
```

## Development

### Running Tests

To ensure the digestifier is functioning correctly, run the provided tests:

```bash
python -m unittest tests/test_digestifier.py
```
