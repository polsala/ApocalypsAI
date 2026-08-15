# Nightly Cosmic Choreographer

A whimsical CLI tool designed to bring a touch of cosmic guidance to your post-apocalyptic task management. Instead of rigid priorities, the Cosmic Choreographer consults the stars (or at least, a deterministic hashing algorithm) to give you a 'cosmic nudge' on which tasks might be most aligned with the universe's current whims.

## Features

*   **Cosmic Alignment Scoring**: Each task is assigned a unique 'cosmic score' based on its content and a user-provided (or default) seed, ensuring deterministic results for consistent cosmic guidance.
*   **Prioritized Nudges**: Tasks are presented in order of their cosmic alignment, with special 'nudges' for the most cosmically favored actions.
*   **Flexible Input**: Read tasks from a file or directly from standard input.
*   **High Performance**: Built with Rust for blazing-fast execution, even when aligning many tasks with the cosmos.

## Installation

To install the `nightly-cosmic-choreographer` utility, you'll need Rust and Cargo installed on your system. If you don't have them, you can get them from [rustup.rs](https://rustup.rs/).

1.  **Clone the repository (if not already done):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-cosmic-choreographer
    ```

2.  **Build and install:**
    ```bash
    cargo install --path .
    ```
    This will install the `nightly-cosmic-choreographer` executable to your Cargo bin directory (usually `~/.cargo/bin`), making it available in your PATH.

## Usage

```bash
nightly-cosmic-choreographer [OPTIONS]
```

### Arguments

*   `-f`, `--tasks-file <TASKS_FILE>`: Path to a file containing tasks, one per line. If not provided, the utility will read tasks from standard input.
*   `-s`, `--seed <SEED>`: A numerical seed for cosmic alignment. Using the same seed with the same tasks will always produce the same cosmic ordering. Defaults to `0` if not provided.

### Examples

**1. Align tasks from a file:**

First, create a `tasks.txt` file:

```
# tasks.txt
Scavenge for rations
Repair the water purifier
Decipher ancient star charts
Fortify the shelter
Barter with the Wasteland Nomads
```

Then run the choreographer:

```bash
nightly-cosmic-choreographer -f tasks.txt -s 12345
```

Example Output:

```
--- Cosmic Choreographer's Nudge (Seed: 12345) ---
[Score: 1234567890123456789] Fortify the shelter - The cosmos whispers: This is your destiny!
[Score: 2345678901234567890] Scavenge for rations - A faint starlight guides you here.
[Score: 3456789012345678901] Barter with the Wasteland Nomads - The void suggests this path.
[Score: 4567890123456789012] Repair the water purifier - A minor celestial alignment points this way.
[Score: 5678901234567890123] Decipher ancient star charts - A minor celestial alignment points this way.
```
*(Scores are illustrative and will vary based on task content and seed, but order is deterministic)*

**2. Align tasks from standard input:**

```bash
echo -e "Meditate on the void\nClean the temporal conduits" | nightly-cosmic-choreographer -s 789
```

**3. No tasks provided:**

```bash
nightly-cosmic-choreographer -f empty_tasks.txt
```

Output:

```
--- Cosmic Choreographer's Nudge (Seed: 0) ---
The cosmos is silent. Perhaps there are no tasks to align today?
```

## How it Works (The Cosmic Algorithm)

The 'cosmic score' for each task is generated using Rust's `DefaultHasher`. This hasher combines the task string and the provided numerical `seed` to produce a `u64` hash value. This ensures that for the same task and the same seed, the score will always be identical, making the cosmic guidance reliably deterministic. The tasks are then sorted by this score, presenting the lowest-scoring task as the most 'aligned' with the current cosmic energies.
