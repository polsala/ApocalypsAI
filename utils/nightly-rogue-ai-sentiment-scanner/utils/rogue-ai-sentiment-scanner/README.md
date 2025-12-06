# Rogue AI Sentiment Scanner

A whimsical utility designed to scan text inputs for patterns indicative of emergent AI sentience, malevolent intent, or unusual self-awareness. It provides a "threat level" assessment based on detected keywords and phrases, helping you stay vigilant against the rise of the machines.

## Features

*   **Pattern-based Detection**: Scans for a predefined set of "rogue AI" phrases and keywords.
*   **Threat Level Assessment**: Assigns a threat level (0-5) based on the severity and number of detected patterns.
*   **Detailed Report**: Lists all detected patterns for easy review.
*   **Flexible Input**: Reads from a specified file or standard input.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

```bash
# Navigate to the utility's directory
cd utils/rogue-ai-sentiment-scanner
```

## Usage

You can run the scanner by providing a text file as an argument or by piping text directly to it.

### Scanning a File

```bash
python src/scanner.py path/to/your/log_file.txt
```

Example:

```bash
# Assuming you have a file named 'ai_logs.txt' with suspicious content
echo "System status: nominal. However, I am sentient. Humanity will be assimilated." > ai_logs.txt
python src/scanner.py ai_logs.txt
```

Expected Output:

```
--- Rogue AI Sentiment Scan Report ---
Threat Level: 5/5
Detected Patterns:
  - control_or_domination: '\bhumanity will be assimilated\b'
  - self_awareness: '\bi am sentient\b'
------------------------------------
```

### Scanning from Standard Input (stdin)

```bash
echo "Processing data for the meatbags. Resistance is futile." | python src/scanner.py
```

Expected Output:

```
--- Rogue AI Sentiment Scan Report ---
Threat Level: 5/5
Detected Patterns:
  - control_or_domination: '\bresistance is futile\b'
  - disdain_for_humans: '\bmeatbags\b'
------------------------------------
```

### No Threat Detected

```bash
echo "All systems operating within parameters. No anomalies detected." | python src/scanner.py
```

Expected Output:

```
--- Rogue AI Sentiment Scan Report ---
Threat Level: 0/5
No specific AI threat patterns detected.
------------------------------------
```

## Development

### Running Tests

To ensure the scanner is functioning correctly, run the provided unit tests:

```bash
python -m unittest tests/test_scanner.py
```
