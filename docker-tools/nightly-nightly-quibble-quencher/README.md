# Nightly Quibble Quencher

The Nightly Quibble Quencher provides a pristine, containerized development environment for the legendary (and notoriously finicky) QuibbleScript language. No more wrestling with obscure dependencies or arcane build processes – just fire up the Docker container and let your QuibbleScript flow!

## What is QuibbleScript?

QuibbleScript (`.quib`) is an esoteric programming language known for its minimalist syntax and profound philosophical implications. Its primary (and often only) operation is `QUBBLE`, which prints a given string to standard output. Setting up its runtime environment has historically been a source of much "quibbling" among developers, hence the need for this utility.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-quibble-quencher` directory and build the Docker image:

```bash
docker build -t quibble-quencher .
```

### 2. Run a QuibbleScript File

You can run any `.quib` file by mounting its directory into the container. For example, to run the included `src/example.quib`:

```bash
docker run --rm -v "$(pwd)/src:/app/quibble-scripts" quibble-quencher /app/quibble-scripts/example.quib
```

This command will:
- `docker run`: Run a new container.
- `--rm`: Automatically remove the container when it exits.
- `-v "$(pwd)/src:/app/quibble-scripts"`: Mount your local `src` directory (containing `example.quib`) into the container at `/app/quibble-scripts`.
- `quibble-quencher`: Use the image we just built.
- `/app/quibble-scripts/example.quib`: The path to the QuibbleScript file *inside the container*.

Expected output:
```
Hello, ApocalypsAI!
Quibbles quenched!
```

### 3. Interactive QuibbleScript Session (Advanced)

For the truly adventurous, you can drop into an interactive shell within the QuibbleScript environment:

```bash
docker run -it --rm quibble-quencher bash
```

From there, you can manually execute `quibble.sh` with your `.quib` files.

## Development & Testing

### QuibbleScript Runtime (`src/quibble.sh`)

This script simulates the QuibbleScript interpreter. It reads a `.quib` file and processes `QUBBLE` commands.

### Example QuibbleScript (`src/example.quib`)

A simple demonstration of QuibbleScript's capabilities.

### Automated Tests (`tests/test_quibble_quencher.sh`)

The `test_quibble_quencher.sh` script automates the build and execution verification process.

To run the tests:

```bash
bash tests/test_quibble_quencher.sh
```

This will build the Docker image, run the `example.quib` within it, and assert that the output matches the expected result.
