# Nightly Broken Link Bureaucrat

## 📜 Overview

The Nightly Broken Link Bureaucrat is a diligent utility designed to patrol your repository's Markdown files, ensuring that all links — both internal and external — are in perfect working order. No more dead ends or frustrating "404 Not Found" messages for your readers! This bureaucrat meticulously checks every `http(s)://` link and verifies the existence of every relative file path reference, reporting any discrepancies with bureaucratic precision.

## ✨ Features

*   **Markdown File Scanning**: Automatically discovers and processes all `.md` files within the current directory and its subdirectories.
*   **External Link Validation**: Performs lightweight HTTP HEAD requests to verify the reachability of external URLs.
*   **Internal Link Verification**: Checks if relative file paths referenced in Markdown files actually exist within the repository.
*   **Comprehensive Reporting**: Outputs a clear, concise list of all broken links, categorized by file and type.

## 🚀 Usage

To run the Broken Link Bureaucrat, navigate to the root of your repository and execute the script:

```bash
python src/link_checker.py
```

The script will then scan all Markdown files and print a report of any broken links found.

## ⚙️ Configuration

Currently, the bureaucrat operates with default settings, scanning all `.md` files. Future enhancements might include configurable paths or exclusion patterns.

## 🧪 Development & Testing

To run the tests for this utility:

```bash
python -m unittest tests/test_link_checker.py
```

The tests are designed to be deterministic and offline, using mocks for file system operations and network requests.
