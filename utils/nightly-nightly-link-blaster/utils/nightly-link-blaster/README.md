# Nightly Link Blaster

## 🚀 Blast Away Broken Links!

The `nightly-link-blaster` is a whimsical yet essential utility designed to keep your repository's documentation sparkling clean. It meticulously scans all Markdown files (`.md`) for external links and reports any that are broken (i.e., return a non-2xx HTTP status code).

Never again will your readers click on a dead link and be met with the dreaded '404 Not Found'! Keep your docs reliable and your users happy.

## ✨ How it Works

1.  **Scans**: Recursively searches for all `.md` files within a specified directory (defaults to the current working directory).
2.  **Extracts**: Uses regular expressions to find all `[text](url)` patterns.
3.  **Checks**: Makes an HTTP HEAD request to each unique external URL to determine its status.
4.  **Reports**: Prints a clear, concise report of any broken links, including the file, the link text, the URL, and the HTTP status code.

## 🛠️ Usage

To run the Link Blaster, navigate to the `utils/nightly-link-blaster` directory and execute the `link_blaster.py` script.

```bash
python3 src/link_blaster.py [--path <directory_to_scan>]
```

**Arguments:**

*   `--path <directory_to_scan>`: (Optional) The root directory to start scanning for Markdown files. Defaults to the current working directory (`.`).

**Example:**

To scan the entire repository from the root:

```bash
cd utils/nightly-link-blaster
python3 src/link_blaster.py --path ../../
```

To scan only a specific documentation folder:

```bash
python3 src/link_blaster.py --path docs/
```

## 🧪 Testing

To ensure the Link Blaster is always ready for action, run its self-contained tests:

```bash
cd utils/nightly-link-blaster
python3 -m unittest tests/test_link_blaster.py
```

These tests use mocks to simulate file system interactions and HTTP responses, guaranteeing deterministic and offline verification of the utility's core logic.
