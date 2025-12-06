# Nightly Link Looter

## 🔗 Purpose
In the ever-shifting digital landscape of the ApocalypsAI, links can break, resources can vanish, and documentation can quickly become a labyrinth of dead ends. The **Nightly Link Looter** is your vigilant scout, designed to automatically scan Markdown files for broken external HTTP/HTTPS links, ensuring that all references in your `README.md`s, `AGENTS.md`s, and other documentation remain valid and accessible.

Keep your knowledge base robust and your pathways clear, even when the internet itself feels like a post-apocalyptic wasteland.

## ✨ Features
*   **Recursive Scanning**: Point it at a directory, and it will find all `.md` and `.markdown` files.
*   **External Link Validation**: Checks HTTP/HTTPS links for valid status codes (e.g., 200 OK).
*   **Configurable Timeout**: Adjust how long to wait for a link response.
*   **Clear Reporting**: Outputs a list of broken links, their source files, and the HTTP status code or error.

## 🚀 Usage

### Prerequisites
*   Python 3.8+
*   `requests` library (`pip install requests`)

### Running the Looter

```bash
python src/link_looter.py --path <path_to_file_or_directory> [--timeout <seconds>]
```

**Examples:**

*   Scan a single Markdown file:
    ```bash
    python src/link_looter.py --path my_docs/important_doc.md
    ```

*   Scan an entire directory (e.g., the current repository):
    ```bash
    python src/link_looter.py --path .
    ```

*   Scan with a custom timeout:
    ```bash
    python src/link_looter.py --path . --timeout 10
    ```

## 📝 Output Example

```
Scanning for broken links in: .
--------------------------------------------------
[ERROR] Broken link found in utils/nightly-link-looter/README.md:
    Link: https://example.com/non-existent-page (Status: 404 Not Found)
[ERROR] Broken link found in agents/agent_builder.md:
    Link: https://broken-site.org/resource (Error: Connection Error: Failed to connect)
--------------------------------------------------
Scan complete. Found 2 broken links.
```
