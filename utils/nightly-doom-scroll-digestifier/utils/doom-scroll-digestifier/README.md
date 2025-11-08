# Doom Scroll Digestifier

## Overview

The `Doom Scroll Digestifier` is a whimsical yet useful utility designed to help you navigate the overwhelming sea of online news. Provide it with a URL to an article, and it will fetch the content, extract the main text, generate a concise summary, and offer a lighthearted 'doom' or 'silver lining' sentiment analysis. Perfect for getting the gist without falling into the endless 'doom scroll'.

## Features

*   **URL Fetching**: Retrieves HTML content from any given URL.
*   **Text Extraction**: Intelligently pulls the main article text from HTML.
*   **Concise Summarization**: Provides a brief summary (defaulting to the first 3 sentences).
*   **Sentiment Analysis**: Identifies 'doom' or 'silver lining' keywords to give a quick emotional read on the article.

## Installation

This utility requires Python 3.11+ and the following packages:

```bash
pip install requests beautifulsoup4
```

## Usage

Run the script from its directory:

```bash
python src/digestifier.py --url "https://example.com/news-article"
```

### Arguments

*   `--url <URL>` (required): The URL of the article to digest.
*   `--sentences <int>` (optional): Number of sentences for the summary (default: 3).

### Example Output

```
Article URL: https://example.com/news-article

--- Summary ---
This is the first sentence of the article. This is the second sentence. And here is the third sentence.

--- Sentiment Analysis ---
Overall Mood: Doom-laden (Keywords: crisis, threat)

--- Full Article Snippet ---
(First 500 characters of the extracted text)
```

## Development

### Running Tests

To ensure everything is working as expected, run the tests from the repository root:

```bash
python -m unittest utils.doom_scroll_digestifier.tests.test_digestifier
```
