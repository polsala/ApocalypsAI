# ApocalypsAI Repository Vibe Checker

## 🌌 Overview

Ever wonder if your repository is feeling 'Serenely Doomed' or on the brink of 'Imminent Collapse'? The ApocalypsAI Repository Vibe Checker is here to tell you! This whimsical utility takes a few key health metrics and translates them into a fun, yet insightful, 'apocalypse mood' for your project.

It's designed to give maintainers a quick, at-a-glance understanding of the repository's current 'vibe' without diving deep into dashboards. Think of it as a mood ring for your code!

## ✨ Features

- **Metric-driven Moods**: Calculates a 'vibe score' based on configurable inputs: number of open issues, recent failed workflow runs, and days since the last commit.
- **Whimsical Output**: Translates scores into evocative moods like 'Serenely Doomed', 'Mildly Gloomy', 'Chaotic Neutral', and 'Imminent Collapse'.
- **Self-contained**: A pure Python script with no external dependencies, making it easy to integrate and test.

## 🚀 Usage

Run the `vibe_checker.py` script with the required arguments:

```bash
python src/vibe_checker.py \
  --open-issues <NUMBER_OF_OPEN_ISSUES> \
  --failed-workflows-24h <NUMBER_OF_FAILED_WORKFLOWS_IN_LAST_24H> \
  --days-since-last-commit <DAYS_SINCE_LAST_COMMIT>
```

**Example:**

```bash
python src/vibe_checker.py \
  --open-issues 5 \
  --failed-workflows-24h 1 \
  --days-since-last-commit 3
```

**Output:**

```
Repository Vibe: Mildly Gloomy 🌧️ (Score: 5.1)
```

## 🛠️ Configuration (Internal)

The scoring weights and mood thresholds are defined within `src/vibe_checker.py` and can be adjusted to better suit your project's specific 'vibe' interpretation.

## 🧪 Development & Testing

To run the tests for this utility:

```bash
python -m unittest tests/test_vibe_checker.py
```
