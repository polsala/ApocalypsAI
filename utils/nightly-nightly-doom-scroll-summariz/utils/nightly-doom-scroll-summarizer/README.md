# Nightly Doom Scroll Summarizer

## Overview
In the post-apocalyptic information deluge, sometimes you just need the gist. The `Nightly Doom Scroll Summarizer` is a Python utility designed to cut through the noise of lengthy text files – be it endless log streams, sprawling news feeds, or verbose reports – and extract the most critical or relevant sentences to form a concise summary.

It's your personal information filter, ensuring you don't miss the crucial signals amidst the digital rubble.

## Features
- **Extractive Summarization**: Identifies and pulls key sentences directly from the source text.
- **Configurable Length**: Adjust the number of sentences in the summary.
- **Minimum Sentence Length Filter**: Ignores trivial or incomplete sentences.
- **Self-contained**: Pure Python, no external dependencies.

## How to Use

### Prerequisites
- Python 3.11+

### Running the Utility

1.  Navigate to the utility's directory:
    ```bash
    cd utils/nightly-doom-scroll-summarizer
    ```

2.  Run the `summarizer.py` script with the path to your target file:
    ```bash
    python src/summarizer.py --file /path/to/your/doom_scroll.txt
    ```

3.  You can also specify the maximum number of sentences for the summary (default is 5) and the minimum character length for a sentence to be considered (default is 50):
    ```bash
    python src/summarizer.py --file /path/to/another/log.txt --max-sentences 3 --min-length 30
    ```

### Example

Given a file `report.txt`:

```
This is a very long report about the recent anomalies. Many strange things have been observed across multiple sectors. Critical system failures were reported in Sector 7, leading to a complete shutdown of the power grid. The recovery efforts are underway, but progress is slow due to unforeseen complications. Further investigation is required to determine the root cause of the widespread disruption. A small, almost imperceptible tremor was also detected near the old research facility. This tremor is not believed to be related to the power grid failure. However, all data points must be considered. The final conclusion will be presented next cycle.
```

Running `python src/summarizer.py --file report.txt --max-sentences 3 --min-length 50` might produce:

```
Summary of report.txt:
- Critical system failures were reported in Sector 7, leading to a complete shutdown of the power grid.
- The recovery efforts are underway, but progress is slow due to unforeseen complications.
- Further investigation is required to determine the root cause of the widespread disruption.
```
