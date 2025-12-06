# Chronos-Sync Time Adjuster

## Aligning Your Clock with the Cosmic Rhythm

The universe is a vast, chaotic place, but even amidst the impending doom, there's a rhythm. The Chronos-Sync Time Adjuster is your essential tool for ensuring your system's internal chronometer is perfectly aligned with the 'Cosmic Alignment Time' (CAT) – a universally recognized, albeit hypothetical, epoch for all significant apocalyptic events.

Whether you're coordinating a last-ditch defense, scheduling critical data backups before the singularity, or simply want to know how far off your clock is from the true cosmic pulse, Chronos-Sync provides precise temporal drift calculations. It even allows for an 'Apocalypse Offset' to account for local variations in temporal distortion fields.

## Features

*   **Cosmic Alignment Time (CAT)**: A fixed, immutable UTC reference point for all temporal calculations.
*   **Temporal Drift Calculation**: Precisely measures the difference between your system's current UTC time and the target sync time.
*   **Apocalypse Offset**: Configure a custom offset (in hours) from CAT to fine-tune your temporal alignment.
*   **Clear Synchronization Guidance**: Provides actionable advice on how much to advance or rewind your clock.
*   **Self-contained & Whimsical**: A Python 3.11 utility, easy to integrate into any post-apocalyptic workflow.

## Installation

This utility is self-contained. Simply navigate to its directory:

```bash
cd utils/chronos-sync-time-adjuster/
```

## Usage

Run the `chronos_sync.py` script directly.

```bash
python3 src/chronos_sync.py
```

### Options

*   `--offset-hours <int>`: An optional integer representing the 'Apocalypse Offset' in hours. This value is added to the Cosmic Alignment Time to determine your target sync time. Can be positive or negative. Defaults to `0`.

### Examples

**1. Check drift against pure Cosmic Alignment Time:**

```bash
python3 src/chronos_sync.py
```

**2. Check drift with a +5 hour Apocalypse Offset:**

```bash
python3 src/chronos_sync.py --offset-hours 5
```

**3. Check drift with a -2 hour Apocalypse Offset:**

```bash
python3 src/chronos_sync.py --offset-hours -2
```

## Example Output

```
Current UTC Time: 2024-10-27 10:00:00
Cosmic Alignment Time: 2025-01-01 00:00:00
Apocalypse Offset: +0 hours
Target Sync Time: 2025-01-01 00:00:00

Temporal Drift: Your system clock is currently 65 days, 14:00:00 behind the Target Sync Time.
To synchronize, you need to advance your clock by 65 days, 14:00:00.
```

```
Current UTC Time: 2025-01-01 00:00:05
Cosmic Alignment Time: 2025-01-01 00:00:00
Apocalypse Offset: +0 hours
Target Sync Time: 2025-01-01 00:00:00

Temporal Drift: Your system clock is currently 0 days, 00:00:05 ahead of the Target Sync Time.
To synchronize, you need to rewind your clock by 0 days, 00:00:05.
```

```
Current UTC Time: 2025-01-01 00:00:00
Cosmic Alignment Time: 2025-01-01 00:00:00
Apocalypse Offset: +0 hours
Target Sync Time: 2025-01-01 00:00:00

Temporal Drift: Your system clock is perfectly aligned with the Target Sync Time. No adjustment needed.
```
