# Chronos-Chime Time-Warp Tracker

## "Coordinating Across Temporal Anomalies"

In the chaotic aftermath, coordinating with your fellow survivors (or AI agents) across disparate temporal zones can be a challenge. The `chronos-chime-time-tracker` is your whimsical yet essential utility for peering into the present moment across various 'pocket dimensions' (time zones).

This tool allows you to quickly see the current time in UTC and any specified timezones, helping you schedule your next scavenging run or critical system integration without accidentally waking up a sleeping agent.

## Usage

Run the script with a list of IANA timezone names as arguments. If no timezones are provided, it will default to a few common ones.

```bash
python src/chronos_chime.py [TIMEZONE_1] [TIMEZONE_2] ...
```

### Examples

To check times in New York, London, and Tokyo:

```bash
python src/chronos_chime.py America/New_York Europe/London Asia/Tokyo
```

To check default timezones:

```bash
python src/chronos_chime.py
```

## Requirements

*   Python 3.9+ (for `zoneinfo` module)

## Output Example

```
--- Chronos-Chime Temporal Scan ---
UTC: 2023-10-27T10:30+00:00

America/New_York: 2023-10-27T06:30-04:00 (Offset: -04:00)
Asia/Tokyo:       2023-10-27T19:30+09:00 (Offset: +09:00)
Australia/Sydney: 2023-10-27T21:30+11:00 (Offset: +11:00)
Europe/London:    2023-10-27T11:30+01:00 (Offset: +01:00)
```
