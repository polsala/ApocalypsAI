# Nightly Broken Link Beacon

## 🚨 Whimsical Purpose

In the post-apocalyptic digital landscape, even the most robust documentation can suffer from link rot. The 'Nightly Broken Link Beacon' is your vigilant sentinel, tirelessly scanning all Markdown files within the repository to identify and report any broken external or internal links. It ensures that every path to knowledge remains open, preventing users from stumbling into digital dead ends.

## 🛠️ How it Works

This utility recursively searches for `.md` files, extracts all Markdown-style links `[text](url)`, and then verifies their accessibility:

*   **External Links**: It attempts to make a `HEAD` request to the URL. A non-200/300 status code indicates a broken link.
*   **Internal Links**: It checks if the referenced file or directory exists relative to the Markdown file's location. This includes links to other Markdown files, images, or any other repository asset.

## 🚀 Usage

To run the beacon, navigate to the `utils/nightly-broken-link-beacon` directory and execute the `beacon.py` script. It will scan the current working directory and its subdirectories.

```bash
python3 src/beacon.py
```

### Example Output

```
Scanning for broken links in the repository...

Found 3 Markdown files.

--- File: README.md ---
  ✅ Valid External: https://github.com/polsala/ApocalypsAI
  ❌ Broken External: https://example.com/non-existent (Status: 404)
  ❌ Broken Internal: ./non-existent-file.md (File not found)

--- File: agents/AGENTS.md ---
  ✅ Valid Internal: ./base.py
  ❌ Broken External: https://broken-api.dev (Status: 500)

--- File: docs/CONTRIBUTING.md ---
  ✅ Valid Internal: ../README.md

Scan complete. 3 broken links found.
```

## ⚙️ Development

### Dependencies

*   Python 3.11+
*   `requests` library (`pip install requests`)

### Running Tests

```bash
python3 -m unittest tests/test_beacon.py
```
