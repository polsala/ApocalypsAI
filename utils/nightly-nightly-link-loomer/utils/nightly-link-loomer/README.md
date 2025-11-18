# Nightly Link-Loomer

## Overview

The Nightly Link-Loomer is a vigilant utility designed to scour your repository's Markdown files for any signs of digital decay: broken external links. In an an ever-shifting digital landscape, ensuring your documentation points to valid resources is crucial. This tool helps you identify and fix those broken connections before they lead to frustration.

It performs a `HEAD` request on all identified external HTTP/HTTPS links within `.md` files in a specified directory, reporting any that return non-success status codes (e.g., 404, 500) or cause network errors.

## Usage

To run the Link-Loomer, simply provide the path to the directory you wish to scan:

```bash
python src/link_loomer.py <path_to_directory>
```

### Example

```bash
python src/link_loomer.py .
```

This will scan all Markdown files in the current directory and its subdirectories.

## Output

The utility will print a list of all broken links found, grouped by the file they appear in. If no broken links are found, it will report a clean bill of health.

## Dependencies

This utility requires the `requests` library.

You can install it using pip:

```bash
pip install requests
```
