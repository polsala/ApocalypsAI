# Temporal Anomaly Detector

## Whimsical Purpose

Ever feel like time itself is... off? Like your computer is living in a slightly different epoch? The 'Temporal Anomaly Detector' is here to help! This whimsical utility checks your system's clock against a reliable external time source (NTP servers) to detect any significant drift. Is it a dying CMOS battery, a mischievous time-traveling squirrel, or a genuine temporal anomaly? This tool won't tell you *why*, but it will tell you *if* your clock is out of sync.

## Genuinely Useful Purpose

Accurate system time is crucial for many operations: secure communication (SSL/TLS), logging, cron jobs, and even some software licenses. A drifting clock can cause cryptic errors and security vulnerabilities. This utility provides a quick, self-contained check to ensure your system's time is synchronized, helping you diagnose underlying hardware or network issues before they become catastrophic.

## How it Works

1.  **Local Time**: Fetches your system's current Coordinated Universal Time (UTC).
2.  **NTP Time**: Queries a public NTP (Network Time Protocol) server (default: `pool.ntp.org`) for the current UTC.
3.  **Comparison**: Calculates the absolute difference between your local system time and the NTP server's time.
4.  **Anomaly Detection**: If the difference exceeds a predefined threshold (default: 5 seconds), it reports a 'Temporal Anomaly'.

## Usage

### Prerequisites

*   Python 3.8+ (tested with 3.11)
*   `ntplib` library (will be installed automatically if using `pip install -r requirements.txt`)

### Installation

```bash
cd utils/temporal-anomaly-detector
pip install -r requirements.txt
```

### Running the Detector

```bash
python src/detector.py
```

### Command-line Arguments

*   `--server <NTP_SERVER>`: Specify an alternative NTP server (e.g., `time.google.com`).
*   `--threshold <SECONDS>`: Set a custom drift threshold in seconds (default: 5).

### Exit Codes

*   `0`: No temporal anomaly detected. System time is synchronized.
*   `1`: Temporal anomaly detected. System time is significantly out of sync.
*   `2`: Error querying NTP server (e.g., network issue, server unreachable).

## Example Output

```bash
# No anomaly
python src/detector.py
# [Temporal Anomaly Detector] Local UTC: 2023-10-27T10:00:00.123456+00:00
# [Temporal Anomaly Detector] NTP UTC:   2023-10-27T10:00:00.000000+00:00
# [Temporal Anomaly Detector] Time difference: 0.12 seconds (threshold: 5.00s).
# [Temporal Anomaly Detector] Status: All clear. No temporal anomalies detected.

# Anomaly detected
python src/detector.py
# [Temporal Anomaly Detector] Local UTC: 2023-10-27T10:00:15.123456+00:00
# [Temporal Anomaly Detector] NTP UTC:   2023-10-27T10:00:00.000000+00:00
# [Temporal Anomaly Detector] Time difference: 15.12 seconds (threshold: 5.00s).
# [Temporal Anomaly Detector] Status: WARNING! Temporal Anomaly Detected! Your system clock is significantly out of sync.

# NTP server error
python src/detector.py --server invalid.ntp.server
# [Temporal Anomaly Detector] Attempting to query NTP server: invalid.ntp.server
# [Temporal Anomaly Detector] Error: Could not query NTP server 'invalid.ntp.server'. [Errno -2] Name or service not known
# [Temporal Anomaly Detector] Status: Failed to check for anomalies due to NTP server error.
```
