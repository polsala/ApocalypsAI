# Nightly Data Debris Decipherer

## Overview

The `nightly-data-debris-decipherer` is a whimsical-yet-useful utility designed to sift through the digital 'rubble' of unstructured text and extract common, recognizable data patterns. In a world where information can be fragmented or corrupted, this tool helps you pinpoint crucial details like URLs, email addresses, IP addresses, and dates.

It's like having a digital metal detector for your text files, helping you find the valuable bits amidst the noise.

## Usage

To use the decipherer, simply provide it with a string of text. It will return a structured dictionary containing all identified patterns.

### As a Python module:

```python
from utils.nightly-data-debris-decipherer.src.decipherer import decipher_debris

text_sample = "Found a strange link: https://example.com/path?q=data and an old email: user@domain.org. Also, a server IP 192.168.1.1 and a log entry from 2023-10-27T14:30:00. Some random numbers: 123.45 and 987."
deciphered_data = decipher_debris(text_sample)
print(deciphered_data)
```

### From the command line:

```bash
python -m utils.nightly-data-debris-decipherer.src.decipherer "Found a link: https://example.com and an email: test@example.com"
```

## Extracted Patterns

The utility currently extracts the following types of data:

*   **URLs**: Web addresses (e.g., `http://example.com`, `https://sub.domain.net/path`)
*   **Emails**: Email addresses (e.g., `user@domain.com`)
*   **IPv4 Addresses**: Standard IPv4 addresses (e.g., `192.168.1.1`)
*   **ISO 8601 Dates/Datetimes**: Dates and datetimes in ISO 8601 format (e.g., `2023-10-27`, `2023-10-27T14:30:00`)
*   **Numbers**: Integer and floating-point numbers.

## Installation

This utility is self-contained and requires no external dependencies beyond Python's standard library (`re`, `json`). Simply place the `nightly-data-debris-decipherer` folder within your `utils/` directory.
