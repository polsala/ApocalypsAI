# Nightly Vibe Scanner

A high-performance CLI tool built with Rust to analyze text and classify its 'apocalyptic vibe'. In a world where communication can be cryptic and subtle, understanding the underlying emotional tone of messages, logs, or ancient texts is crucial. This tool helps you quickly discern if a message carries a 'Hopeful', 'Despairing', 'Chaotic', 'Resourceful', or 'Neutral' sentiment.

## Features

*   **Fast Text Analysis**: Leverages Rust's performance for quick processing.
*   **Vibe Classification**: Categorizes text into predefined 'apocalyptic vibes'.
*   **Keyword Detection**: Highlights keywords that contributed to the classification.
*   **CLI Interface**: Easy to use from the command line, supporting stdin or file input.

## Installation

To install `nightly-vibe-scanner`, you need to have Rust and Cargo installed. If you don't, visit [rustup.rs](https://rustup.rs/) for instructions.

1.  Clone the repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-vibe-scanner
    ```
2.  Build the project:
    ```bash
    cargo build --release
    ```
3.  The executable will be located at `./target/release/nightly-vibe-scanner`.
    You can also install it directly to your Cargo bin directory:
    ```bash
    cargo install --path .
    ```
    (Ensure `~/.cargo/bin` is in your PATH).

## Usage

### Scan text from standard input

```bash
echo "The last beacon of hope flickers, but we will rebuild." | nightly-vibe-scanner
# Output:
# Vibe: Hopeful
# Detected Keywords: hope, rebuild
```

```bash
echo "All is lost, the darkness consumes everything. There is no escape." | nightly-vibe-scanner
# Output:
# Vibe: Despairing
# Detected Keywords: lost, darkness, no escape
```

### Scan text from a file

Create a file named `message.txt`:

```
We must scavenge for parts to repair the comms array. Ingenuity will be our guide.
```

Then run:

```bash
nightly-vibe-scanner --file message.txt
# Output:
# Vibe: Resourceful
# Detected Keywords: scavenge, repair, ingenuity
```

### Help

```bash
nightly-vibe-scanner --help
```

## Vibe Categories

The tool classifies text into the following categories based on keyword analysis:

*   **Hopeful**: Indicates optimism, resilience, and a focus on the future.
*   **Despairing**: Suggests hopelessness, loss, and impending doom.
*   **Chaotic**: Reflects disorder, conflict, and instability.
*   **Resourceful**: Points to problem-solving, scavenging, crafting, and self-sufficiency.
*   **Neutral**: The default if no strong keywords from other categories are detected.
