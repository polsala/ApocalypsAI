# ✍️ Chronicle Keeper's Quill

The Chronicle Keeper's Quill is a whimsical yet highly practical utility designed to automatically generate a draft changelog from your Git commit history. It parses conventional commit messages (e.g., `feat:`, `fix:`, `docs:`) and organizes them into a structured Markdown output, making release note generation a breeze.

## 🌟 Features

*   **Conventional Commit Parsing**: Understands `type(scope): subject` format.
*   **Breaking Change Detection**: Identifies breaking changes via `!` in the header or `BREAKING CHANGE:` in the commit body.
*   **Categorized Output**: Groups commits into sections like Features, Bug Fixes, Documentation, Refactors, and more.
*   **Customizable Range**: Generate changelogs between any two Git references (tags, commit hashes, branches).
*   **Self-contained**: Pure Python, relies only on `git` being available in the environment.

## 🚀 Usage

The utility is a command-line tool.

```bash
python src/quill.py <start_ref> [end_ref] [--cwd <path>]
```

*   `<start_ref>`: The Git reference (tag, commit hash, branch name) from which to start collecting commits.
*   `[end_ref]`: (Optional) The Git reference to end collecting commits. Defaults to `HEAD`.
*   `--cwd <path>`: (Optional) The current working directory for `git` commands. Useful if running the script from outside the repository root. Defaults to the current directory.

### Examples

1.  **Generate changelog since the last tag (`v1.0.0`) up to the current `HEAD`:**
    ```bash
    python src/quill.py v1.0.0
    ```

2.  **Generate changelog between two specific tags (`v1.0.0` and `v1.1.0`):**
    ```bash
    python src/quill.py v1.0.0 v1.1.0
    ```

3.  **Generate changelog for a specific branch (`feature/new-ui`) against `main`:**
    ```bash
    python src/quill.py main feature/new-ui
    ```

4.  **Generate changelog from a different directory:**
    ```bash
    python src/quill.py v1.0.0 --cwd /path/to/your/repo
    ```

## 📝 Output Example

```markdown
## 💥 Breaking Changes
- **Introduce new authentication flow** (a1b2c3d)
  The old authentication API is deprecated and will be removed in the next major version.

## ✨ Features
- Implement user login (auth) (e4f5g6h)
- Add dark mode toggle (ui) (f2f2f2f)

## 🐛 Bug Fixes
- Resolve critical bug in payment processing (i7j8k9l)

## 📝 Documentation
- Update README with new installation steps (m0n1o2p)

## ♻️ Refactors
- Simplify data fetching logic (q3r4s5t)

## ⚡ Performance Improvements
- Optimize image loading for faster page loads (u6v7w8x)

## 🧹 Chores
- Update dependencies to latest versions (y9z0a1b)
```

## 🧪 Testing

To run the tests, navigate to the `utils/chronicle-keeper-quill` directory and execute:

```bash
python -m unittest tests/test_quill.py
```

The tests use `unittest.mock` to simulate `git` command outputs, ensuring they are deterministic and do not require an actual Git repository to run.
