# Nightly Temporal Beacon Pinger

The ApocalypsAI Nightly Temporal Beacon Pinger is a whimsical utility designed to monitor the stability of various "temporal beacons" across the spacetime continuum. While not interacting with actual temporal mechanics (yet!), it simulates concurrent "pings" to imaginary endpoints, reporting on their "temporal drift" (simulated latency) and overall stability.

This tool is perfect for those who want to practice Go concurrency patterns while keeping an eye on the theoretical integrity of the timeline.

## Usage

To run the Temporal Beacon Pinger, you'll need Go installed.

1.  **Navigate to the utility directory:**
    ```bash
    cd go-utils/nightly-temporal-beacon-pinger
    ```

2.  **Run the pinger with default beacons:**
    ```bash
    go run src/main.go
    ```

3.  **Specify custom beacons:**
    You can pass beacon names as command-line arguments. Each argument will be treated as a beacon to ping.
    ```bash
    go run src/main.go "EventHorizon-2077" "Singularity-Epoch" "PastEcho-1984"
    ```

## How it Works

The pinger uses Go goroutines to concurrently "ping" each specified temporal beacon. Each ping simulates a connection attempt with a random "temporal drift" (latency) and a chance of "temporal instability" (failure). The results are then collected and reported.

-   **Concurrency**: Leverages Go's lightweight goroutines to handle multiple beacon pings simultaneously.
-   **Simulated Drift**: Random `time.Sleep` is used to mimic varying network latencies.
-   **Simulated Instability**: A random chance of a ping "failing" to simulate an unreachable or unstable temporal point.

## Example Output

```
Pinging 3 temporal beacons...

[EventHorizon-2077] Temporal Drift: 123ms, Status: STABLE
[Singularity-Epoch] Temporal Drift: 250ms, Status: UNSTABLE (Connection Rift!)
[PastEcho-1984] Temporal Drift: 87ms, Status: STABLE

Temporal Beacon Pinger Report:
- Total Beacons: 3
- Stable Beacons: 2
- Unstable Beacons: 1
```
