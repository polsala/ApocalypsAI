# Nightly Link Necromancer

## 💀 Purpose

The Nightly Link Necromancer is a whimsical-yet-vital utility designed to prevent the decay of our documentation. It scours specified Markdown files for external HTTP/HTTPS links and attempts to "resurrect" them by checking their availability. Any links found to be unresponsive are reported, ensuring our documentation remains accurate and free of digital tombstones.

## ✨ Features

*   **Markdown Link Extraction**: Identifies `[text](url)` patterns in Markdown files.
*   **HTTP Status Checking**: Pings identified URLs to verify their accessibility.
*   **Clear Reporting**: Outputs a list of all dead links found.

## 🚀 Usage

Run the utility from the command line, providing one or more Markdown file paths as arguments.

```bash
python src/link_necromancer.py path/to/README.md path/to/AGENTS.md
```

### Example Output (for dead links)

```
Scanning path/to/README.md...
  💀 Dead link found: https://broken.example.com (Status: 404)
  💀 Dead link found: https://another-broken.link (Error: Connection refused)
Scanning path/to/AGENTS.md...
  ✅ All links alive.
```

### Example Output (for no dead links)

```
Scanning path/to/README.md...
  ✅ All links alive.
Scanning path/to/AGENTS.md...
  ✅ All links alive.
No dead links found across all scanned files. The documentation lives!
```

## 🛠️ Development

### Dependencies

*   `requests`

Install with: `pip install requests`

### Running Tests

```bash
python -m unittest tests/test_link_necromancer.py
```
