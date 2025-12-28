## Nightly Cosmic Drift Detector

This utility simulates a stream of 'cosmic data' and employs a simple anomaly detection algorithm to identify deviations, flagging them with whimsical, space-themed alerts. It's designed to be a fun, yet illustrative, example of real-time data monitoring.

### Philosophy

"Even in the void, patterns emerge, and deviations are cause for a little cosmic fanfare."

### Installation

```bash
npm install
```

### Usage

Run the detector with optional parameters for stream size and anomaly threshold:

```bash
node src/main.js --streamSize 1000 --anomalyThreshold 3
```

- `--streamSize`: The number of data points to generate in the simulation (default: 500).
- `--anomalyThreshold`: The number of standard deviations from the mean to consider an anomaly (default: 2).

### How it Works

1.  **Data Simulation**: Generates a stream of numbers, simulating 'cosmic energy readings'. Most readings will cluster around a mean, with some natural variation.
2.  **Drift Detection**: Calculates the running mean and standard deviation of the data stream. Any data point that falls outside a specified number of standard deviations from the mean is flagged as a 'cosmic anomaly'.
3.  **Whimsical Alerts**: Upon detecting an anomaly, it emits a unique, playful alert message.

### Example Output

```
Generating cosmic data stream...
Processing data point 100: Reading = 105.23, Mean = 100.12, StdDev = 5.01
Processing data point 101: Reading = 106.50, Mean = 100.20, StdDev = 5.05
Processing data point 102: Reading = 115.80, Mean = 100.35, StdDev = 5.10
✨ COSMIC ANOMALY DETECTED! ✨
  Reading: 115.80
  Mean: 100.35
  StdDev: 5.10
  Alert: "A rogue nebula just zipped through the data stream! Prepare for unexpected stardust!"
Processing data point 103: Reading = 98.76, Mean = 100.50, StdDev = 5.15
...
```

### Testing

Run the tests using:

```bash
npm test
```

### Contributing

Feel free to fork, modify, and submit pull requests. Let's explore the cosmos of data together!
