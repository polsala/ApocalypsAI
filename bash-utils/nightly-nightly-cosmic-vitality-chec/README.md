# Nightly Cosmic Vitality Check

## 🌌 Overview

The `nightly-cosmic-vitality-check` is a whimsical yet practical utility designed to scan your system's core resources (CPU, memory, and disk space) and report on its "cosmic vitality." Think of it as a friendly oracle peering into the energetic state of your machine, offering insights into potential temporal fluctuations or resource drains before they become critical anomalies.

It provides a quick, human-readable summary, categorizing your system's health into "OPTIMAL," "ATTENTIVE," or "CRITICAL" vitality states, accompanied by charmingly apocalyptic advice.

## ✨ Features

- **CPU Core Resonance Check**: Monitors CPU utilization to ensure your processing cores aren't over-exerting themselves.
- **Memory Flow Analysis**: Assesses memory consumption, warning if your system's cosmic consciousness is becoming overwhelmed.
- **Aetheric Storage Scan**: Checks disk space usage, advising when it's time to purge forgotten relics from the void.
- **Whimsical Status Messages**: Delivers status reports with a touch of post-apocalyptic charm.
- **Configurable Thresholds**: Easily adjust what constitutes "high" usage for each resource.

## 🚀 Usage

To perform a cosmic vitality scan, simply execute the script:

```bash
bash src/cosmic-vitality-check.sh
```

### Example Output (Optimal)

```
🌌 Initiating Cosmic Vitality Scan... 🌌
----------------------------------------
CPU Core Resonance: 5.00% utilized
Memory Flow: 10.00% consumed
Aetheric Storage: 10% occupied
----------------------------------------
Cosmic Vitality Status: OPTIMAL
All cosmic energies are in harmonious balance. Continue your journey through the temporal planes!
```

### Example Output (Critical)

```
🌌 Initiating Cosmic Vitality Scan... 🌌
----------------------------------------
CPU Core Resonance: 85.00% utilized
Memory Flow: 92.00% consumed
Aetheric Storage: 95% occupied
----------------------------------------
Cosmic Vitality Status: CRITICAL
Observations from the Void:
  - CPU Cores are humming a bit too intensely! Consider a moment of quiet contemplation.
  - Memory Streams are overflowing! Your system's cosmic consciousness might be overwhelmed.
  - Aetheric Storage is nearing capacity! Time to purge some forgotten relics from the void.
Urgent action required to restore cosmic balance!
```

## ⚙️ Configuration

The script uses default thresholds for determining vitality levels. You can override these by setting environment variables before running the script:

- `CPU_THRESHOLD_HIGH`: Percentage CPU utilization (default: `80`)
- `MEM_THRESHOLD_HIGH`: Percentage memory utilization (default: `85`)
- `DISK_THRESHOLD_HIGH`: Percentage disk utilization (default: `90`)

**Example:**

```bash
CPU_THRESHOLD_HIGH=70 MEM_THRESHOLD_HIGH=90 bash src/cosmic-vitality-check.sh
```

This would set the CPU high threshold to 70% and memory to 90% for that execution.

## 🧪 Testing

The utility includes a self-contained test script to ensure its cosmic sensors are functioning correctly.

To run the tests:

```bash
bash tests/test_cosmic-vitality-check.sh
```

The tests utilize mock commands (`top`, `free`, `df`) to simulate various system resource states, ensuring deterministic and isolated validation of the script's logic and output.
