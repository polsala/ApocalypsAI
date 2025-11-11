# Digital Dustbunny Duster

## 🧹 What is this?

In the vast, decaying digital landscape of the post-apocalypse, information is power, but only if you can find it! The **Digital Dustbunny Duster** is a whimsical utility designed to sweep away "digital dustbunnies" – those pesky, broken internal Markdown links that lead nowhere. It ensures your repository's documentation remains a coherent, navigable map, even when the servers are powered by potato batteries.

Think of it as a librarian for the end times, making sure every cross-reference in your survival guide actually points to a valid page.

## ✨ Features

*   **Scans Markdown files**: Recursively searches a specified directory for `.md` files.
*   **Detects broken internal links**: Identifies `[text](relative/path/to/file.md)` links where `relative/path/to/file.md` does not exist.
*   **Ignores external links**: `http://` or `https://` links are considered external and are not checked.
*   **Ignores anchor links**: Links like `[text](#anchor)` are ignored as they refer to sections within the same file.
*   **Clear reporting**: Outputs a list of files with broken links and the specific broken paths.

## 🚀 How to Use

1.  **Navigate**: Change into the `utils/digital-dustbunny-duster/` directory.
2.  **Run**: Execute the `duster.py` script with the `--path` argument pointing to the directory you want to scan.

    ```bash
    python src/duster.py --path ../../ # To scan the entire ApocalypsAI repo
    # Or for a specific directory:
    python src/duster.py --path ./docs
    ```

### Example Output

```
Scanning directory: /path/to/your/repo
---
File: README.md
  Broken link: [Non-existent file](docs/missing.md) -> docs/missing.md (Does not exist)
---
File: docs/guide.md
  Broken link: [Another missing doc](../broken-path.md) -> ../broken-path.md (Does not exist)
---
Scan complete. Found 2 broken links in 2 files.
```

## 🛠️ Development

The `duster.py` script is written in Python 3.11 and uses only standard library modules, making it highly self-contained and portable.

### Running Tests

To ensure the Duster is always ready for its vital mission, run the tests:

```bash
python -m unittest tests/test_duster.py
```
