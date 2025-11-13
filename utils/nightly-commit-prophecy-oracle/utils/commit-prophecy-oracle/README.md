# Commit Prophecy Oracle

## 🔮 Gaze into the Future of Your Codebase! 🔮

The Commit Prophecy Oracle is a whimsical utility designed to peer into the mystical energies of your Git commit history and divine a prophecy about the current state and future trajectory of your project. By analyzing recent commit messages, the Oracle interprets the collective intent and effort, offering cryptic yet insightful pronouncements.

Is your codebase on the brink of a grand refactoring? Plagued by lingering bugs? Or perhaps blossoming with new features? Let the Oracle reveal your destiny!

## ✨ How it Works

The Oracle connects to the ethereal plane of your Git repository, specifically examining the last 10 commit messages. It then uses ancient algorithms (simple keyword analysis) to identify prevailing themes such as bug fixes, new features, refactoring efforts, or breaking changes. Based on these themes, a unique prophecy is unveiled.

## 🚀 Usage

To consult the Oracle, navigate to your Git repository's root directory in your terminal and run the script:

```bash
python src/oracle.py
```

You can also specify a path to a Git repository:

```bash
python src/oracle.py /path/to/your/repo
```

### Example Output

```
Consulting the Commit Prophecy Oracle for repository: /home/user/my-awesome-project

The winds of innovation blow strong! New lands are being charted, and bountiful harvests of functionality await. Ensure your maps are clear and your compass true.
```

## 🛠️ Development

### Requirements

*   Python 3.x
*   Git (must be installed and accessible in your PATH)

### Running Tests

To ensure the Oracle's divinations are always consistent and reliable, run the self-contained tests:

```bash
python -m unittest tests/test_oracle.py
```

The tests use mocking to simulate Git repository interactions, ensuring they are deterministic and do not require an actual Git repository to run.
