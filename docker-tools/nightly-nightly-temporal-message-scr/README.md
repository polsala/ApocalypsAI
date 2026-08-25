# Nightly Temporal Message Scrambler

A whimsical-yet-useful containerized utility for simulating temporal distortion and data corruption on input messages. Perfect for testing the resilience of your message processing systems against unexpected delays and garbled data, or just for adding a touch of chaos to your communications.

## Features

- **Temporal Delay**: Introduce a configurable delay before the message is "scrambled" and output.
- **Character Scrambling**: Randomly alter characters within the message (swaps, case changes, symbol replacements).
- **Word Reordering**: Randomly swap the order of words in the message.
- **Containerized**: Easily run anywhere with Docker, ensuring a consistent environment.

## Usage

Build the Docker image:

```bash
docker build -t temporal-scrambler .
```

Run the scrambler with a message and optional parameters:

```bash
docker run temporal-scrambler "Hello, ApocalypsAI community!"
```

This will output the scrambled message after a default delay.

### Parameters

You can control the scrambling behavior using command-line arguments:

- `<message>`: The input string to be scrambled (required).
- `--delay <seconds>`: The delay in seconds before processing (default: 0.5).
- `--char-scramble-level <level>`: Level of character scrambling (0-2, default: 1).
    - `0`: No character scrambling.
    - `1`: Moderate character scrambling (e.g., case changes, minor swaps).
    - `2`: Aggressive character scrambling (e.g., symbol replacement, significant swaps).
- `--word-reorder-level <level>`: Level of word reordering (0-1, default: 0).
    - `0`: No word reordering.
    - `1`: Moderate word reordering (e.g., adjacent word swaps).
- `--seed <integer>`: Optional. A seed for the random number generator to ensure deterministic scrambling for testing purposes.

### Examples

1. **Basic scrambling:**
   ```bash
   docker run temporal-scrambler "The quick brown fox jumps over the lazy dog."
   ```

2. **With a 2-second delay:**
   ```bash
   docker run temporal-scrambler --delay 2 "Important message, but make it slow."
   ```

3. **Aggressive character scrambling, no word reordering:**
   ```bash
   docker run temporal-scrambler --char-scramble-level 2 --word-reorder-level 0 "This message will be heavily distorted."
   ```

4. **Deterministic scrambling (for testing):**
   ```bash
   docker run temporal-scrambler --seed 123 --delay 0 --char-scramble-level 1 "Predictable chaos."
   ```

## Development

The utility is built with Python and packaged as a Docker container.

- `Dockerfile`: Defines the container image.
- `entrypoint.sh`: The script executed when the container starts, parsing arguments and invoking the Python scrambler.
- `src/scrambler.py`: Contains the core scrambling logic.

## Tests

Run the automated tests using the provided `test_scrambler.sh` script:

```bash
./tests/test_scrambler.sh
```

This script builds the Docker image and runs several scenarios to verify the scrambler's behavior.
