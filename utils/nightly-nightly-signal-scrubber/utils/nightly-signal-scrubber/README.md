# Nightly Signal Scrubber

## Description
In the post-apocalyptic digital wasteland, signals can get messy. The Nightly Signal Scrubber is your trusty tool for purifying raw text data, removing the digital 'rubble' that obscures vital information. Whether it's corrupted logs, salvaged data fragments, or garbled transmissions, this utility helps you clean it up.

It can:
- Trim leading/trailing whitespace from each line.
- Remove entirely empty lines.
- Collapse multiple internal spaces into a single space.
- Remove lines matching a specified regular expression pattern.

## Usage
```bash
python src/scrubber.py <input_file> [output_file] [--no-empty-lines] [--no-trim-whitespace] [--collapse-spaces] [--remove-pattern <regex>]
```

### Arguments:
- `<input_file>`: Path to the text file to be scrubbed.
- `[output_file]`: Optional. Path to save the scrubbed content. If not provided, output is printed to stdout.

### Options:
- `--no-empty-lines`: Do not remove empty lines (they are removed by default).
- `--no-trim-whitespace`: Do not trim leading/trailing whitespace from lines (they are trimmed by default).
- `--collapse-spaces`: Replace multiple consecutive spaces within a line with a single space.
- `--remove-pattern <regex>`: A regular expression pattern. Any line fully matching this pattern will be removed.

## Examples

### Basic cleaning (trim whitespace, remove empty lines):
```bash
python src/scrubber.py raw_data.txt cleaned_data.txt
```

### Collapse spaces and remove lines with 'ADVERTISEMENT':
```bash
python src/scrubber.py log_dump.txt --collapse-spaces --remove-pattern '.*ADVERTISEMENT.*'
```

### Output to stdout:
```bash
python src/scrubber.py messy_notes.txt --no-trim-whitespace
```
