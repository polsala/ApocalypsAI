# Nightly Spectral Signal Scanner

## Overview

The `nightly-spectral-signal-scanner` is a whimsical utility designed to help survivors locate potential pre-apocalypse resources by 'listening' for faint, simulated spectral network echoes. It doesn't interact with real-world networks but rather processes a predefined 'spectral map' of forgotten data streams, power grid hums, and broadcast relics.

By simulating concurrent scans across various 'frequencies', the tool identifies 'points of interest' where valuable resources might still be found, based on the nature and strength of the detected spectral echoes.

## Features

*   **Simulated Concurrent Scanning**: Utilizes Go goroutines to 'scan' multiple spectral frequencies simultaneously.
*   **Echo Deciphering**: Interprets spectral echo types (e.g., Data Stream, Power Grid Hum, Broadcast Relic) to infer potential resources.
*   **Location Suggestion**: Provides whimsical location descriptions for detected points of interest.
*   **Configurable Scan Range**: Allows specifying a frequency range for the simulated scan.

## How to Run

1.  **Prerequisites**: Ensure you have Go (version 1.18 or higher) installed.

2.  **Clone the repository (if not already done)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/go-utils/nightly-spectral-signal-scanner
    ```

3.  **Run the scanner**:
    ```bash
    go run src/main.go
    ```

    The program will output a list of detected spectral echoes and their associated potential resources and locations.

## Example Output

```
Scanning for spectral echoes between 88.0 MHz and 108.0 MHz with 3 workers...

Detected Spectral Echoes:
-------------------------
ID: ECHO-001
  Frequency: 101.5 MHz, Strength: 0.85
  Type: Data Stream
  Location: Old Library Sector A-7
  Potential Resources: [Servers Archives Knowledge]

ID: ECHO-003
  Frequency: 98.1 MHz, Strength: 0.72
  Type: Power Grid Hum
  Location: Abandoned Substation Gamma
  Potential Resources: [Fuel Generators Electrical Components]

ID: ECHO-005
  Frequency: 105.9 MHz, Strength: 0.91
  Type: Broadcast Relic
  Location: Crumbling Radio Tower Peak
  Potential Resources: [Communication Gear Antennas Information]
-------------------------
Scan complete. May your journey be fruitful!
```

## How it Works (Under the Hood)

The scanner maintains an in-memory 'spectral map' of predefined `SpectralEcho` objects. When `go run src/main.go` is executed, it launches multiple goroutines to simulate scanning different parts of the frequency spectrum. Each goroutine checks if any known spectral echoes fall within its assigned frequency range and meet a minimum strength threshold. The results are then collected and presented.

## Development & Testing

To run the tests:

```bash
cd go-utils/nightly-spectral-signal-scanner
go test ./tests
```

The tests are deterministic and offline, operating on a predefined mock spectral map to ensure consistent results.
