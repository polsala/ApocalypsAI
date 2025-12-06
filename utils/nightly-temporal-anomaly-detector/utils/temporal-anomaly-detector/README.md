# Temporal Anomaly Detector

## 🕰️ Unmasking the Chronal Drifters 🕰️

The ApocalypsAI Nightly Integrator presents the **Temporal Anomaly Detector**, a crucial utility for ensuring your systems are marching in lockstep with the cosmic clock. In an age where even time itself can be a conspiracy, detecting subtle drifts in system clocks is paramount to preventing cascading failures, data corruption, and accidental summoning of elder gods.

This utility compares your local system's time against a simulated (or eventually, real) external time source, reporting any significant "temporal anomalies" that could indicate a system clock gone rogue.

## Features

*   Compares local system time against a configurable reference (currently simulated NTP).
*   Reports time differences and flags anomalies exceeding a defined tolerance.
*   Lightweight and self-contained.

## Usage

```bash
python src/detector.py --tolerance <seconds> [--ntp-offset <seconds>]
```

*   `--tolerance`: The maximum acceptable difference in seconds between local and reference time before an anomaly is reported. (Default: 1 second)
*   `--ntp-offset`: (Optional, for simulation/testing) Simulates an offset in seconds for the NTP server's reported time. Positive values mean NTP is ahead, negative means behind. (Default: 0 seconds)

### Example

```bash
# Check for drifts greater than 0.5 seconds
python src/detector.py --tolerance 0.5

# Simulate an NTP server that's 2 seconds ahead and check for anomalies > 1 second
python src/detector.py --tolerance 1 --ntp-offset 2
```

## Output

The script will print a status message indicating whether a temporal anomaly was detected and the magnitude of the drift.

```
[2023-10-27 04:42:01] Local time: 2023-10-27 04:42:01.123456
[2023-10-27 04:42:01] Reference time: 2023-10-27 04:42:01.123456
[2023-10-27 04:42:01] Status: All temporal vectors aligned. Drift: 0.000000 seconds.
```

OR

```
[2023-10-27 04:42:01] Local time: 2023-10-27 04:42:01.123456
[2023-10-27 04:42:03] Reference time: 2023-10-27 04:42:03.123456
[2023-10-27 04:42:01] Status: 🚨 TEMPORAL ANOMALY DETECTED! Reference time is 2.000000 seconds ahead of local time. 🚨
```
