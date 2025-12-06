# Markdown TOC Generator

A tiny, self‑contained utility that scans a Markdown document for headings and produces a Table of Contents (TOC) in Markdown format. Perfect for README files, wikis, or any post‑apocalyptic journal you keep in plain text.

## Features

* Supports ATX headings (`#`, `##`, `###`, …) up to level 6.
* Generates slugified links compatible with GitHub‑flavored Markdown.
* CLI for quick one‑off usage:
  ```bash
  python -m utils.markdown-toc-generator.src.generator path/to/file.md
  ```

## Example

```markdown
# My Project
## Installation
## Usage
### Advanced
```

Running the generator yields:

```markdown
- [My Project](#my-project)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Advanced](#advanced)
```

## License

MIT
