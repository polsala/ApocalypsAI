# Nightly Survival Kit Scavenger

The ApocalypsAI Nightly Survival Kit Scavenger is a crucial utility for ensuring your projects are "self-sufficient" and ready for any post-apocalyptic scenario (or just a new developer joining the team). It scans a specified directory for a predefined set of essential project files and reports on their presence or absence.

Think of it as checking your project's emergency backpack – does it have the README map? The LICENSE survival guide? The `requirements.txt` rations?

## Usage

```bash
python src/scavenger.py <path_to_project_directory>
```

### Example Output

```
Scanning project at: /path/to/my/awesome-project

--- Survival Kit Status ---

✅ README.md (Project overview and instructions)
✅ LICENSE (Legal survival guide)
❌ requirements.txt (Python dependency rations)
✅ Dockerfile (Containerized shelter blueprint)
❌ Makefile (Build automation tools)
✅ .gitignore (Unwanted debris filter)
✅ pyproject.toml (Modern Python project manifest)

--- Summary ---
Your project is missing 2 essential survival items.
Consider adding: requirements.txt, Makefile
```

## Essential Files Checked

The scavenger currently looks for the following files and directories:

*   `README.md`: Project overview, setup, and usage instructions.
*   `LICENSE`: Legal terms and conditions.
*   `requirements.txt` (or `pyproject.toml` with `[tool.poetry]` or `[project]`): Python dependency management.
*   `Dockerfile`: Containerization instructions.
*   `Makefile`: Common build and automation tasks.
*   `.gitignore`: Specifies intentionally untracked files to ignore.
*   `pyproject.toml`: Modern Python project manifest (also checked for dependency management).
*   `CONTRIBUTING.md`: Guidelines for contributing to the project.
*   `docs/`: A directory for additional documentation.

## Development

This utility is written in Python 3.11 and is self-contained.
