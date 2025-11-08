# Dependency Graveyard Gardener

## Whimsical Purpose
In the ever-expanding digital wilderness of our repositories, unused dependencies can accumulate like forgotten relics, weighing down our projects and inviting potential vulnerabilities. The **Dependency Graveyard Gardener** is here to tend to your codebase, meticulously identifying those declared dependencies that are no longer actively imported or utilized. It helps you prune the digital 'graveyards' and keep your project lean, efficient, and ready for the next apocalypse (or just the next release).

## How It Works
The Gardener scans your project directory for common Python dependency manifest files (like `requirements.txt` and `pyproject.toml`) and then parses your Python source files (`.py`) to detect actual `import` statements. By comparing the declared dependencies against the observed imports, it unearths the 'ghost' dependencies – those that are present in your manifests but seem to have no active role in your code.

## Usage
To run the Dependency Graveyard Gardener, navigate to your project's root directory and execute the `gardener.py` script. It will automatically scan the current directory and its subdirectories.

```bash
python3 src/gardener.py
```

### Output
The utility will print a list of identified unused dependencies to standard output. If no unused dependencies are found, it will report a clean bill of health.

```
Scanning project for unused dependencies...
Found 3 declared dependencies.
Found 2 active imports.

--- Unused Dependencies Found ---
- unused-package
- another-dead-lib
---------------------------------

Project is clean of unused dependencies.
```

(Example output will vary based on findings)

## Supported Manifests & Languages
Currently, the Gardener supports:
-   **Python**: `requirements.txt` and `pyproject.toml` (specifically the `[project].dependencies` section).
-   **Python**: `.py` source files for import detection.

## Future Enhancements
-   Support for other languages and package managers (e.g., `package.json` for Node.js, `Cargo.toml` for Rust).
-   More sophisticated import detection (e.g., dynamic imports, `__init__.py` patterns, `__all__` exports).
-   Configuration options for specifying manifest paths or exclusion patterns.
-   Integration with virtual environments to check installed packages vs. declared.
