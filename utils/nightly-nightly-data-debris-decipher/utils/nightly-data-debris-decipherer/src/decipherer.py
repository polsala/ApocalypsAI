import os
import re
import json
import argparse
from typing import List, Dict, Any

# Regex patterns for common data debris
# Source: https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url
URL_PATTERN = re.compile(
    r'https?://(?:www\.)?[a-zA-Z0-9./?#&=_-]+'
)
# Source: https://emailregex.com/
EMAIL_PATTERN = re.compile(
    r'(?:[a-z0-9!#$%&\'*.+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*.+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x5f-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'
)
# ISO 8601 timestamp (date only or date-time with optional timezone)
# Simplified for common cases, e.g., 2023-10-27, 2023-10-27T10:00:00Z, 2023-10-27T10:00:00+01:00
TIMESTAMP_PATTERN = re.compile(
    r'\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:[.,]\d+)?(?:Z|[+-]\d{2}:\d{2})?)?'
)

def decipher_file(filepath: str) -> Dict[str, Any]:
    """
    Reads a file and extracts URLs, email addresses, and ISO 8601 timestamps.

    Args:
        filepath (str): The path to the file to decipher.

    Returns:
        Dict[str, Any]: A dictionary containing the filepath and lists of found patterns.
    """
    urls = set()
    emails = set()
    timestamps = set()

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

            for match in URL_PATTERN.finditer(content):
                urls.add(match.group(0))
            for match in EMAIL_PATTERN.finditer(content):
                emails.add(match.group(0))
            for match in TIMESTAMP_PATTERN.finditer(content):
                timestamps.add(match.group(0))

    except Exception as e:
        print(f"Warning: Could not process file {filepath} - {e}")
        return {
            "filepath": filepath,
            "urls": [],
            "emails": [],
            "timestamps": [],
            "error": str(e)
        }

    return {
        "filepath": filepath,
        "urls": sorted(list(urls)),
        "emails": sorted(list(emails)),
        "timestamps": sorted(list(timestamps))
    }

def main():
    parser = argparse.ArgumentParser(
        description="Sifts through digital debris to extract URLs, emails, and ISO 8601 timestamps."
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="The directory to scan for data debris."
    )
    parser.add_argument(
        "--output-file",
        type=str,
        help="Optional. The path to save the JSON report. If not provided, prints to stdout."
    )
    parser.add_argument(
        "--file-extensions",
        type=str,
        default="txt,log,md,json",
        help="Optional. Comma-separated list of file extensions to process (e.g., 'txt,log')."
    )

    args = parser.parse_args()

    input_dir = args.input_dir
    output_file = args.output_file
    allowed_extensions = {f".{ext.strip().lower()}" for ext in args.file_extensions.split(',')}

    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist or is not a directory.")
        exit(1)

    results: List[Dict[str, Any]] = []
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if any(filename.lower().endswith(ext) for ext in allowed_extensions):
                filepath = os.path.join(root, filename)
                result = decipher_file(filepath)
                if result:
                    results.append(result)

    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4, ensure_ascii=False)
            print(f"Report saved to {output_file}")
        except Exception as e:
            print(f"Error: Could not write to output file {output_file} - {e}")
            exit(1)
    else:
        print(json.dumps(results, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
