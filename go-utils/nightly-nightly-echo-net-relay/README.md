# nightly-echo-net-relay

A Go CLI tool simulating a post-apocalyptic whisper network relay, applying temporal echoes and slight distortions to messages before forwarding them to the next simulated hop.

## Purpose

In the desolate future, reliable communication is a luxury. The `nightly-echo-net-relay` utility provides a whimsical-yet-functional simulation of a resilient, albeit imperfect, message relay system. It's designed for short, critical bursts of information that might need to "echo" through the network to ensure delivery, even if slightly altered by the temporal distortions of the wasteland.

## How it Works

When a message is passed to the relay:
1.  **Distortion**: The first two words of the message are deterministically swapped (if present), simulating a minor "temporal ripple" or "network noise."
2.  **Echo**: The message is then appended with ` (echo)` a configurable number of times, representing the message reverberating through the network or being re-transmitted for redundancy.
3.  **Forwarding**: The processed message is then "forwarded" to a specified next hop, simulating its journey across the whisper network.

This tool is useful for:
-   Testing message resilience in a simulated noisy environment.
-   Understanding basic message processing and forwarding logic.
-   Adding a touch of post-apocalyptic flavor to your CLI interactions.

## Build and Run

### Prerequisites

-   Go (version 1.18 or higher recommended)

### Building the Executable

Navigate to the `src` directory and build the Go program:

```bash
cd src
go build -o ../nightly-echo-net-relay main.go
cd ..
```

This will create an executable named `nightly-echo-net-relay` in the root of the utility's directory.

### Running the Utility

Execute the compiled binary with the required `-message` flag and optional parameters:

```bash
./nightly-echo-net-relay -message "Urgent: Supplies low at Sector 7" -level 2 -next-hop "Whisper Node Delta"
```

#### Arguments:

-   `-message <string>` (Required): The message to be processed and relayed.
-   `-level <int>` (Optional, default: `1`): The "echo level." Determines how many times ` (echo)` is appended to the message. A level of `0` means no echoes.
-   `-next-hop <string>` (Optional, default: `"Unknown Relay"`): The simulated destination or next relay node for the message.

### Examples

1.  **Basic Message with Default Echo:**
    ```bash
    ./nightly-echo-net-relay -message "Hello World"
    # Expected Output:
    # Relaying message: "World Hello (echo)"
    # Next hop: Unknown Relay
    ```

2.  **Message with Higher Echo Level and Specific Next Hop:**
    ```bash
    ./nightly-echo-net-relay -message "Rendezvous Point Gamma confirmed" -level 3 -next-hop "Scavenger Outpost 5"
    # Expected Output:
    # Relaying message: "Point Rendezvous Gamma confirmed (echo) (echo) (echo)"
    # Next hop: Scavenger Outpost 5
    ```

3.  **Message with No Echo (only distortion):**
    ```bash
    ./nightly-echo-net-relay -message "Secure the perimeter" -level 0
    # Expected Output:
    # Relaying message: "the Secure perimeter"
    # Next hop: Unknown Relay
    ```

4.  **Error: Missing Message:**
    ```bash
    ./nightly-echo-net-relay
    # Expected Output:
    # Error: A message is required. Use -message "Your message here".
    # Usage of nightly-echo-net-relay:
    #   -level int
    #         The echo level (integer, 0 for no echo, 1 for basic, etc.). (default 1)
    #   -message string
    #         The message to send through the echo network.
    #   -next-hop string
    #         The simulated next relay node or final recipient. (default "Unknown Relay")
    ```

## Testing

To run the automated tests, navigate to the `src` directory and execute:

```bash
cd src
go test -v ./...
```

The tests are deterministic and offline, verifying the message transformation logic and output formatting without external dependencies.
