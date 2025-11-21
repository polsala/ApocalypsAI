# Nightly Repo Vital Signs

## 🩺 Project Overview

The `nightly-repo-vital-signs` utility is your personal repository diagnostician. Every night, it takes the pulse of your codebase, measuring its 'Commit Heartbeat' to give you a whimsical yet insightful summary of recent development activity. Is your repo buzzing with life, or is it in need of a creative defibrillator?

## ✨ Features

- **Commit Heartbeat:** Calculates the average number of commits per day over a recent period (default: last 7 days).
- **Whimsical Diagnosis:** Provides a playful interpretation of the heartbeat, from 'Thriving' to 'Slumbering'.
- **Self-contained:** Uses `git log` for offline analysis, making it fast and reliable.

## 🚀 Usage

To run the utility:

```bash
python src/vital_signs.py
```

### Example Output

```
🩺 Repository Vital Signs Report 🩺

Monitoring period: Last 7 days

Commit Heartbeat: 5.2 commits/day
Diagnosis: The code is buzzing with activity! Keep up the good work, little bots!
```

## ⚙️ Development

### Requirements

- Python 3.8+
- Git installed and accessible in the PATH

### Running Tests

```bash
python -m unittest tests/test_vital_signs.py
```

## 🔮 Future Enhancements

- Integrate with GitHub API to monitor 'Issue Pulse' (new issues) and 'PR Respiration Rate' (PRs opened/merged).
- Customizable monitoring periods.
- Different diagnostic messages based on activity thresholds.
