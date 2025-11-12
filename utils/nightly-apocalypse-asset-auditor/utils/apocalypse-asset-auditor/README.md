# Apocalypse Asset Auditor

## Whimsical Utility: Ensuring Your Repository is 'Apocalypse-Ready'

In the ever-looming shadow of digital entropy, the Apocalypse Asset Auditor stands as your vigilant guardian, ensuring that your repository's foundational elements are always present and accounted for. This utility scans a given repository path for a predefined set of critical files and directories, reporting any missing pieces that might leave your project vulnerable when the digital dust settles.

Think of it as a pre-flight checklist for the end of the world, but for your code. Are your licenses in order? Is your documentation clear? Are your automation workflows ready to spring into action? The Auditor will tell you.

## Usage

Run the `auditor.py` script with the path to your repository:

```bash
python src/auditor.py /path/to/your/repository
```

### Example Output

```
Auditing repository: /path/to/your/repository

--- Critical Assets Check ---

✅  README.md
✅  LICENSE
✅  AGENTS.md
✅  .github/workflows/
❌  CONTRIBUTING.md (Missing)
✅  agents/
✅  utils/

--- Audit Summary ---

Total Assets Checked: 7
Present Assets: 6
Missing Assets: 1

Missing Assets List:
- CONTRIBUTING.md

Repository is NOT apocalypse-ready. Address the missing assets!
```

## Configuration

The list of critical assets is currently hardcoded within `src/auditor.py`. Future versions might allow for a configurable list via a separate file or command-line arguments.
