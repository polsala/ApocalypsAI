# Nightly Glitch-Weaver Log Harmonizer

## 🌌 Weaving Harmony from Log Chaos 🌌

The digital wasteland is rife with fragmented data and discordant log entries. The Nightly Glitch-Weaver Log Harmonizer is your trusty companion for bringing order to this chaos. This utility sifts through your unstructured log files, identifies common patterns, and transforms them into a consistent, machine-readable JSON format. No more squinting at irregular timestamps or digging for error codes – let the Glitch-Weaver bring harmony to your data streams!

### ✨ Features

*   **Pattern-Based Parsing**: Utilizes a set of predefined regex patterns to intelligently extract meaningful fields from diverse log formats.
*   **JSON Output**: Converts each log line into a structured JSON object, perfect for downstream analysis, indexing, or visualization tools.
*   **Fallback Handling**: Gracefully handles unmatched lines by encapsulating them in a `raw_message` field, ensuring no data is lost.
*   **Self-Contained**: A single Python script with no external dependencies, ready to run in any post-apocalyptic environment.

### 🚀 Usage

```bash
python src/harmonizer.py <log_file_path>
```

If no file path is provided, the utility will read from standard input (`stdin`).

**Example:**

Given a `sample.log` file:

```
[2023-10-27 10:00:01] INFO: User 'Alice' logged in from 192.168.1.100
ERROR: Disk space critical on /dev/sda1 (95% full)
192.168.1.1 - - [27/Oct/2023:10:00:05 +0000] "GET /index.html HTTP/1.1" 200 1234
Unrecognized log line here.
```

Run the harmonizer:

```bash
python src/harmonizer.py sample.log
```

Output will be:

```json
{"timestamp": "2023-10-27 10:00:01", "level": "INFO", "user": "Alice", "ip": "192.168.1.100", "_pattern_name": "timestamped_message_with_user_ip"}
{"level": "ERROR", "message": "Disk space critical on /dev/sda1 (95% full)", "_pattern_name": "simple_level_message"}
{"ip": "192.168.1.1", "timestamp": "27/Oct/2023:10:00:05 +0000", "method": "GET", "path": "/index.html", "protocol": "HTTP/1.1", "status": "200", "size": "1234", "_pattern_name": "apache_access"}
{"raw_message": "Unrecognized log line here.", "_pattern_name": "unmatched"}
```

### 🛠️ Development

The `harmonizer.py` script contains a list of predefined regex patterns in the `LogHarmonizer.PATTERNS` class variable. You can extend or modify these patterns within the script to suit your specific log formats. Each pattern should be a dictionary with a `name` and a `regex` string. Named capture groups in the regex will become keys in the output JSON. The order of patterns matters; more specific patterns should generally come before more general ones.

### 🧪 Tests

To run the tests, navigate to the `utils/nightly-glitch-weaver-log-harmonizer` directory and execute:

```bash
python -m pytest tests/test_harmonizer.py
```
