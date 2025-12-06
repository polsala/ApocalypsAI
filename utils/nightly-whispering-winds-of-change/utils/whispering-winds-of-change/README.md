# Whispering Winds of Change: Git Diff Summarizer

## Purpose
This utility acts as a 'Temporal Anomaly Detector' for your codebase, providing a concise summary of changes within a Git diff. It helps you quickly grasp the scope of modifications, whether you're reviewing a Pull Request, understanding recent commits, or just curious about the 'whispers of change' in your repository.

It parses a Git diff (either generated directly from Git references or provided as a file) and reports:
- Total lines added
- Total lines removed
- List of unique files modified

## Usage

### Prerequisites
- Python 3.8+
- Git installed (if using Git reference mode)

### From Git References
To summarize the diff between two Git references (e.g., commits, branches, tags):

```bash
python src/diff_summarizer.py <ref1> <ref2>
```

**Examples:**
- Summarize changes between the last two commits:
  `python src/diff_summarizer.py HEAD~1 HEAD`
- Summarize changes between `main` and `feature-branch`:
  `python src/diff_summarizer.py main feature-branch`

### From a Diff File
To summarize a diff that has been saved to a file (e.g., from `git diff > my_changes.diff`):

```bash
python src/diff_summarizer.py --file <path_to_diff_file>
```

**Example:**
- Summarize a pre-generated diff file:
  `python src/diff_summarizer.py --file path/to/my_changes.diff`

## Output Example

```
--- Whispering Winds of Change Summary ---

Total Lines Added: 15
Total Lines Removed: 7

Files Changed:
- src/main.py
- docs/README.md
- tests/test_feature.py

------------------------------------------
```
