# Nightly Temporal Anomaly Detector

## 🕰️ Unearthing Time Paradoxes in Your Filesystem 🕰️

Welcome, intrepid explorer of the digital realm! The ApocalypsAI Nightly Integrator proudly presents the **Temporal Anomaly Detector**. In the chaotic dance of development, files can sometimes get... out of sync. This utility is your trusty chronometer, designed to pinpoint files that seem to exist outside the normal flow of time within your repository.

Are some files modified in the future? Are others ancient relics, long forgotten but still lurking? The Temporal Anomaly Detector will expose these temporal paradoxes, helping you maintain a pristine and time-consistent codebase.

### ✨ Features

*   **Future File Detection**: Identifies files whose modification timestamp (`mtime`) is set to a time *after* the current moment. A common symptom of misconfigured clocks, build system glitches, or time-traveling developers.
*   **Stale File Identification**: Flags files whose `mtime` is older than a specified threshold (default: 365 days). Perfect for uncovering forgotten assets, deprecated documentation, or code that's simply gathering digital dust.
*   **Whimsical Reporting**: Presents anomalies in a clear, actionable format, allowing you to address temporal inconsistencies before they unravel the fabric of your project.

### 🚀 How to Use

1.  Navigate to the `utils/nightly-temporal-anomaly-detector/` directory.
2.  Run the `detector.py` script with the path to the directory you wish to scan.

```bash
python3 src/detector.py /path/to/your/repository
```

### ⚙️ Arguments

*   `<path>`: The root directory to scan for temporal anomalies (required).
*   `--stale-days <int>`: (Optional) Number of days after which a file is considered stale. Default is `365` days.

    ```bash
    python3 src/detector.py . --stale-days 180
    ```

### 📊 Example Output

```
Scanning '/home/user/my_project' for temporal anomalies...
Current time: 2023-10-27 10:00:00.123456
Stale threshold: 365 days

--- Temporal Anomaly Report ---

Future Modified Files (mtime > current time):
- /home/user/my_project/build/future_log.txt (mtime: 2023-10-27 10:05:30)

Stale Files (mtime older than 365 days):
- /home/user/my_project/docs/old_spec.pdf (mtime: 2021-05-15 14:22:01)
- /home/user/my_project/legacy/old_script.py (mtime: 2022-01-01 09:00:00)

--- End Report ---
```

If no anomalies are found, you'll be greeted with a reassuring message: `No temporal anomalies detected. All clear!`

### 🤝 How it Helps the ApocalypsAI Community

This utility ensures the integrity of our shared digital archives. By identifying files that are out of sync with the present or have overstayed their welcome, we can:

*   **Prevent Build Failures**: Future-dated files can confuse build systems and caching mechanisms.
*   **Reduce Technical Debt**: Stale files often indicate forgotten code or documentation that can be removed or updated.
*   **Improve Repository Health**: A clean, time-consistent repository is easier to navigate, maintain, and ultimately, survive the digital apocalypse with.
*   **Foster Awareness**: Encourages developers to be mindful of file timestamps and their implications.

May your files always be in the correct temporal alignment!
