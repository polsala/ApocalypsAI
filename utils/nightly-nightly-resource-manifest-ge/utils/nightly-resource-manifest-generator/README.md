# Nightly Resource Manifest Generator

## 🌌 The ApocalypsAI Nightly Integrator's Drop: Resource Manifest Generator 🌌

In the chaotic aftermath, knowing what resources your systems rely on is paramount. The `nightly-resource-manifest-generator` is your digital cartographer, meticulously mapping out all external dependencies across your projects. No more guessing which ancient library powers your critical infrastructure when the internet is just a myth.

This utility scans a specified directory for common dependency files (like `requirements.txt`, `package.json`, `go.mod`, `Cargo.toml`) and compiles a consolidated, human-readable Markdown manifest. It's like a survival guide for your codebase's supply chain!

## ✨ Features

*   **Multi-language Support**: Parses dependencies from Python, Node.js, Go, and Rust projects.
*   **Consolidated View**: Gathers all detected dependencies into a single, easy-to-read Markdown file.
*   **Offline & Self-contained**: No external network calls needed. Runs entirely on your local files.
*   **Whimsical Utility**: Helps you prepare for the "dependency dark ages."

## 🚀 Usage

```bash
python src/manifest_generator.py --path /path/to/your/project --output /path/to/output/manifest.md
```

### Arguments:

*   `--path <directory>`: The root directory to scan for dependency files. (Required)
*   `--output <file_path>`: The path where the generated Markdown manifest will be saved. (Required)

## 🛠️ Development & Testing

The utility is written in Python 3.11+ and requires the `toml` library.
Install dependencies:

```bash
pip install -r requirements.txt
```

Tests are located in `tests/test_manifest_generator.py` and can be run using `pytest`.

```bash
# From the utils/nightly-resource-manifest-generator directory
pip install pytest
pytest tests/
```

## 📜 Example Output (`manifest.md`)

```markdown
# Project Resource Manifest

Generated on: 2023-10-27 10:30:00 UTC

## Python Dependencies

*   requests==2.28.1
*   pyyaml>=6.0
*   rich~=13.0

## Node.js Dependencies

*   express: ^4.18.2
*   lodash: ~4.17.21

## Go Dependencies

*   github.com/gin-gonic/gin v1.8.1
*   golang.org/x/text v0.3.7

## Rust Dependencies

*   serde = "1.0"
*   tokio = { features = ["full"], version = "1.20" }
```
