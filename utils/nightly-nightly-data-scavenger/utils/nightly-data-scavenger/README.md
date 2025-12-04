# Nightly Data Scavenger

## Reclaiming the Digital Wasteland

The Nightly Data Scavenger is a crucial utility for sifting through the digital debris of the apocalypse, extracting valuable patterns from files. Whether you're looking for forgotten URLs, abandoned email addresses, or custom data fragments, this tool helps you reclaim useful information from the vast, unstructured wasteland.

## Usage

Run the scavenger from the command line, providing a target path and the patterns you wish to find.

```bash
python src/scavenger.py <target_path> [--patterns <regex1> <regex2> ...] [--types <type1> <type2> ...]
```

### Arguments:

*   `<target_path>`: The directory or file path to scavenge.
*   `--patterns <regex1> <regex2> ...`: One or more custom regular expressions to search for. Ensure regex patterns are properly quoted if they contain spaces or special characters.
*   `--types <type1> <type2> ...`: One or more predefined pattern types to search for. Currently supported types:
    *   `url`: Standard URL patterns.
    *   `email`: Standard email address patterns.

### Example:

To find all URLs and email addresses in the current directory and its subdirectories:

```bash
python src/scavenger.py . --types url email
```

To find specific API keys (e.g., starting with `API_KEY_`) and any mention of 'secret' in a specific file:

```bash
python src/scavenger.py my_config.txt --patterns "API_KEY_[A-Z0-9]+" "secret"
```

## Output

The utility outputs a JSON object to stdout, detailing the matches found per file. Each file path will be a key, with its value being a list of all unique matches found within that file for the specified patterns.

```json
{
  "path/to/file1.txt": [
    "match1",
    "match2"
  ],
  "path/to/file2.log": [
    "match3"
  ]
}
```

If no matches are found, an empty JSON object `{}` will be returned.
