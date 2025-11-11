# Doom-Scroll Digestifier

## Overview

The `Doom-Scroll Digestifier` is a whimsical-yet-useful utility designed to combat information overload and anxiety caused by constant exposure to overwhelming news. It processes a stream of "catastrophic" or "doom-and-gloom" articles (simulated from various feeds) and distills them into a concise, actionable, and less sensationalized digest. Instead of endless scrolling, get the gist and move on with your day, prepared but not paralyzed.

## Features

*   **Concise Summarization**: Reduces lengthy articles into key points.
*   **Actionable Insights**: Attempts to extract potential actions or preparedness steps.
*   **Anxiety Reduction**: Filters out sensational language to present facts calmly.
*   **Configurable Filters**: (Future enhancement) Allow users to define keywords for filtering or prioritization.

## Installation

This utility is self-contained and requires Python 3.11+.

1.  Navigate to the `utils/doom-scroll-digestifier/` directory.
2.  Ensure you have Python 3.11 or newer installed.

## Usage

Run the `digestifier.py` script directly. It will process a predefined (or mocked) set of articles and print the digest to the console.

```bash
python src/digestifier.py
```

### Example Output

```
--- Doom-Scroll Digest ---
Date: 2023-10-27

[Article 1: Global Warming Accelerates]
Summary: Recent data indicates a faster-than-expected rise in global temperatures, impacting polar ice caps and sea levels.
Actionable: Support sustainable initiatives, reduce personal carbon footprint.
Source: ClimateWatch

[Article 2: Cyberattack on Critical Infrastructure]
Summary: A sophisticated cyberattack targeted a major power grid, causing temporary outages in several regions. Investigations are ongoing.
Actionable: Review personal cybersecurity practices, ensure strong passwords and multi-factor authentication.
Source: TechSecurity Daily

--- End Digest ---
```

## Development

### Running Tests

To run the tests, navigate to the utility's root directory and execute `pytest` (if installed) or run the test file directly:

```bash
python -m unittest tests/test_digestifier.py
```

## License

This project is licensed under the MIT License. See the main repository's `LICENSE` file for details.
