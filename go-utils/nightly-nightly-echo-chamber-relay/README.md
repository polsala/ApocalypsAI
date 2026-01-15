# Nightly Echo Chamber Relay

## Summary

The `nightly-echo-chamber-relay` is a whimsical-yet-useful Go utility designed to simulate sending a "whisper" (a message) to multiple "echo chambers" (simulated network endpoints) concurrently. It then collects and reports on the "echoes" (responses), including their latency and any detected "temporal distortions" (errors).

This tool is useful for understanding concurrent operations, simulating distributed system message delivery, and basic network health checking in a fun, themed way.

## How it Works

1.  **Whisper Transmission**: The utility takes a message as a command-line argument.
2.  **Concurrent Relaying**: It defines a set of simulated `ListeningPost`s, each with configurable minimum/maximum latency and a failure rate.
3.  **Goroutines & Channels**: For each `ListeningPost`, a Go goroutine is launched to simulate sending the whisper. Results (success/failure, latency, error) are sent back via a Go channel.
4.  **Echo Report**: Once all whispers have been sent and echoes collected, a summary report is printed, detailing the status and latency for each post, and a final count of successful vs. failed echoes.

## Usage

### Prerequisites

*   Go (Golang) installed (version 1.16 or higher recommended).

### Build

Navigate to the `src` directory and build the executable:

```bash
cd go-utils/nightly-echo-chamber-relay/src
go build -o ../nightly-echo-chamber-relay .
```

### Run

Execute the compiled binary with your desired whisper message:

```bash
./nightly-echo-chamber-relay "Hello, void! Is anyone out there?"
```

Example Output:

```
Relaying whisper "Hello, void! Is anyone out there?" to 4 echo chambers...

--- Echo Report ---
✅ echo-chamber-alpha.void | Status: Success | Latency: 123ms
✅ echo-chamber-beta.void  | Status: Success | Latency: 287ms
❌ echo-chamber-gamma.void | Status: Failure | Latency: 55ms    | Error: Temporal distortion detected at echo-chamber-gamma.void
✅ echo-chamber-delta.void | Status: Success | Latency: 189ms

Summary: 3 successful echoes, 1 failed echoes.
```

## Tests

Tests are implemented using Go's built-in testing framework. They mock the network interaction (`sendWhisperFunc`) and `os.Exit` to ensure determinism and offline execution.

### Run Tests

Navigate to the `tests` directory and run the tests:

```bash
cd go-utils/nightly-echo-chamber-relay/tests
go test -v .
```

Expected Test Output (example):

```
go test -v .
=== RUN   TestSendWhisperSuccess
--- PASS: TestSendWhisperSuccess (0.00s)
=== RUN   TestSendWhisperFailure
--- PASS: TestSendWhisperFailure (0.00s)
=== RUN   TestMainFunctionWithAllSuccess
--- PASS: TestMainFunctionWithAllSuccess (0.00s)
=== RUN   TestMainFunctionWithMixedResults
--- PASS: TestMainFunctionWithMixedResults (0.00s)
=== RUN   TestMainFunctionNoArgs
--- PASS: TestMainFunctionNoArgs (0.00s)
PASS
ok      nightly-echo-chamber-relay/tests        0.004s
```
