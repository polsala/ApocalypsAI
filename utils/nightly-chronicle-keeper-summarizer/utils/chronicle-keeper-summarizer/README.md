# Chronicle Keeper's Content Summarizer

## Overview

The `chronicle-keeper-summarizer` is a vital tool for any archivist or historian navigating the vast, often overwhelming, data streams of the post-apocalyptic era. It distills lengthy texts – be they ancient logs, salvaged reports, or cryptic transmissions – into concise, 'chronicle-style' summaries. This utility helps you quickly grasp the essence of a document, identifying key events, entities, and their significance, without getting lost in the minutiae.

## Features

*   **Concise Summarization**: Extracts the most important sentences to form a brief overview.
*   **Chronicle Style**: Designed to present information in a clear, impactful manner, suitable for historical records.
*   **Flexible Input**: Accepts text from a file path or directly from standard input.
*   **Self-Contained**: No external dependencies beyond standard Python libraries.

## Installation

This utility is self-contained. Simply navigate to its directory:

```bash
cd utils/chronicle-keeper-summarizer
```

## Usage

### From a file:

```bash
python src/summarizer.py --file path/to/your/document.txt --sentences 3
```

### From standard input (piping):

```bash
cat path/to/your/document.txt | python src/summarizer.py --sentences 5
```

### From standard input (interactive):

```bash
python src/summarizer.py
# Type your text, then press Ctrl+D (Unix/Linux) or Ctrl+Z then Enter (Windows)
```

**Arguments:**

*   `--file <path>`: Path to the text file to summarize. If not provided, reads from stdin.
*   `--sentences <int>`: (Optional) The desired number of sentences in the summary. Defaults to 3.

## Example

Given a file `ancient_log.txt` with the content:

```
Day 734. The sky remains a perpetual twilight, a testament to the Great Dusting. Our scouts reported unusual energy signatures emanating from Sector Gamma, near the old power plant ruins. We dispatched a small recon team, led by Commander Vex, to investigate. Supplies are dwindling, and morale is low. The discovery of the ancient data core last week provided a temporary boost, but its contents remain encrypted. We must find a way to decipher it soon, for the sake of our future.
```

Running `python src/summarizer.py --file ancient_log.txt --sentences 2` might produce (output order is preserved from original text):

```
Our scouts reported unusual energy signatures emanating from Sector Gamma, near the old power plant ruins.
We must find a way to decipher it soon, for the sake of our future.
```
