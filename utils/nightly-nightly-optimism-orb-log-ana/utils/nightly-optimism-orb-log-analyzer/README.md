# 🔮 Nightly Optimism Orb Log Analyzer

The ApocalypsAI Nightly Integrator presents the Optimism Orb! In the face of impending digital doom, it's crucial to find the glimmers of hope and stability in our system logs. This utility scans your specified log directories, sifts through the digital dust, and provides a whimsical yet insightful summary of your system's "mood." Are we thriving, merely surviving, or teetering on the brink? The Orb will tell!

## ✨ Features

*   **Multi-file Scan**: Recursively scans directories for log files matching specified patterns.
*   **Sentiment Analysis**: Categorizes log entries into Critical, Warning, Positive, and Informative.
*   **Optimism Rating**: Generates a simple "Optimism Rating" based on the balance of log sentiments.
*   **Detailed Summary**: Provides counts for each category and highlights files with critical issues.

## 🚀 Usage

```bash
python src/analyzer.py --path /var/log --patterns "*.log" "*.txt" --exclude-patterns "access.log"
```

### Arguments:

*   `--path <directory>` (required): The root directory to start scanning for log files.
*   `--patterns <pattern1> [<pattern2> ...]`: Glob patterns for log files to include (e.g., `*.log`, `app_*.txt`).
*   `--exclude-patterns <pattern1> [<pattern2> ...]`: Glob patterns for log files to exclude (e.g., `debug.log`, `temp_*.log`).
*   `--max-lines <int>` (optional): Maximum lines to process per file to prevent excessive memory usage. Defaults to 10000.

## 📊 Example Output

```
🔮 Optimism Orb Log Analysis Report 🔮

Scanning directory: /var/log
Patterns: ['*.log', '*.txt']
Exclude Patterns: ['access.log']

---
✨ Orb's Glimmering Insights ✨
---

Total files scanned: 5
Total lines processed: 1250

Critical Messages: 3 (Found in: /var/log/app.log, /var/log/worker.log)
Warning Messages: 15
Positive Messages: 210
Informative Messages: 1022

---
🌟 Optimism Rating: 7.8/10 🌟
The digital winds whisper of minor turbulence, but the core systems hum with a steady, positive rhythm. Keep an eye on those critical spots, but overall, the Orb sees a bright horizon!
```
