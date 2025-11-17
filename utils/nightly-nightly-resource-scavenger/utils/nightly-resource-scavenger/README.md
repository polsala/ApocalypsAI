# Nightly Resource Scavenger

## Description
In the post-apocalyptic digital landscape, resources are scarce and connections are vital. The Nightly Resource Scavenger is a vigilant utility designed to patrol your repository's markdown files, identifying and reporting any broken external or internal links. It ensures that all pathways to information remain intact, preventing digital dead ends and preserving the integrity of your documentation.

## Features
- Scans `.md` files for both HTTP/HTTPS links and relative file paths.
- Reports broken external links (HTTP status codes outside 200-399 range).
- Reports broken internal file links (non-existent files).
- Provides clear output indicating the file, line number, and the broken link.

## Usage
To run the scavenger, simply execute the `scavenger.py` script with the target directory as an argument. It will recursively scan all `.md` files within that directory.

```bash
python3 src/scavenger.py --path .
```

### Arguments
- `--path <directory>`: The root directory to start scanning from (e.g., `.`, `docs/`). Defaults to the current directory.

## Example Output
```
Scanning directory: .

Broken Links Found:
--------------------
File: README.md, Line: 10 - External: https://broken.example.com (Status: Unreachable)
File: docs/guide.md, Line: 5 - Internal: ../non-existent-file.md (Status: File not found)
--------------------
Scan complete. 2 broken links found.
```
