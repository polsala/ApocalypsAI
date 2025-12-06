# Echoes of the Void - Dead Link Detector

In the vast, silent expanse of the post-apocalyptic digital landscape, even the most robust links can decay into echoes of the void. This utility, the `echoes-of-the-void-dead-link-detector`, is your vigilant sentinel against the creeping entropy of broken URLs.

It meticulously scans your project's documentation and text files, identifying any external links that have succumbed to the ravages of time or server collapse. By ensuring your references remain valid, you safeguard the collective knowledge and prevent future explorers from falling into digital chasms.

## Usage

```bash
python src/detector.py <file1> [file2 ...]
```

### Example:

```bash
python src/detector.py README.md agents/AGENTS.md
```

This will scan `README.md` and `AGENTS.md` for URLs and report any that are unreachable or return an error status code.

## Features

- **URL Extraction**: Intelligently pulls HTTP/HTTPS URLs from various text formats.
- **Reachability Check**: Performs HTTP HEAD requests to verify link validity without downloading full content, falling back to GET if HEAD is not supported.
- **Detailed Reporting**: Outputs broken links along with their HTTP status codes or a generic '0' for connection/timeout errors.
- **Configurable Timeout**: Prevents hanging on unresponsive servers.

## Installation

This utility requires the `requests` library.

```bash
pip install requests
```

## Development

To run tests:

```bash
python -m pytest utils/echoes-of-the-void-dead-link-detector/tests/
```
