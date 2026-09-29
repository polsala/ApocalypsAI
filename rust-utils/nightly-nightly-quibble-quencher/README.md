# Nightly Quibble Quencher

## Overview

The `nightly-quibble-quencher` is a whimsical-yet-powerful command-line utility crafted in Rust to help you prioritize those small, nagging tasks or issues – affectionately dubbed "quibbles." By assigning "quantum factors" (urgency, complexity, and impact) to each quibble, this tool calculates a priority score and presents you with an optimized list, ensuring you tackle what truly matters first.

It's perfect for developers, project managers, or anyone overwhelmed by a growing list of minor but important items.

## Features

*   **Quibble Input:** Read quibbles from a file or standard input.
*   **Configurable Factors:** Adjust the weighting of urgency, complexity, and impact to suit your personal or team's prioritization philosophy.
*   **High Performance:** Built with Rust for speed and efficiency.
*   **Clear Output:** Get a neatly sorted list of quibbles, from most to least critical.

## Installation

To install `nightly-quibble-quencher`, you'll need Rust and Cargo installed on your system. If you don't have them, visit [rustup.rs](https://rustup.rs/) for instructions.

1.  Clone the repository (or navigate to this utility's directory if part of a larger project):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-quibble-quencher
    ```
2.  Build the project:
    ```bash
    cargo build --release
    ```
3.  The executable will be located at `./target/release/quibble-quencher`.
    You can add it to your system's PATH for easier access:
    ```bash
    sudo cp ./target/release/quibble-quencher /usr/local/bin/
    ```

## Usage

Quibbles are provided as lines, each containing a description and three numerical factors (urgency, complexity, impact) separated by pipes (`|`). Factors should be integers, typically from 1 to 10.

**Format:** `Description | Urgency | Complexity | Impact`

### Example Quibble File (`quibbles.txt`):

```
Fix typo in README | 2 | 1 | 3
Investigate strange log message | 7 | 5 | 8
Refactor legacy function | 5 | 8 | 6
Update dependency X | 3 | 2 | 4
```

### Running the Quencher

```bash
# From a file
quibble-quencher -f quibbles.txt

# From standard input
echo "Review PR #123 | 8 | 6 | 9" | quibble-quencher
echo -e "Prepare daily report | 6 | 3 | 7\nSchedule team sync | 4 | 2 | 5" | quibble-quencher

# With custom weights (default weights are 1 for all factors)
quibble-quencher -f quibbles.txt --weight-urgency 2 --weight-complexity 1 --weight-impact 3
```

### Command Line Arguments

*   `-f, --file <FILE>`: Path to a file containing quibbles. If not provided, reads from stdin.
*   `--weight-urgency <WEIGHT>`: Weight for the urgency factor (default: 1).
*   `--weight-complexity <WEIGHT>`: Weight for the complexity factor (default: 1).
*   `--weight-impact <WEIGHT>`: Weight for the impact factor (default: 1).
*   `-h, --help`: Print help information.
*   `-V, --version`: Print version information.

## Output

The tool will output a prioritized list of quibbles, showing their calculated score and original details.

```
Prioritized Quibbles:
--------------------
Score: 70 - Investigate strange log message | 7 | 5 | 8
Score: 49 - Refactor legacy function | 5 | 8 | 6
Score: 28 - Prepare daily report | 6 | 3 | 7
Score: 18 - Update dependency X | 3 | 2 | 4
Score: 15 - Fix typo in README | 2 | 1 | 3
Score: 11 - Schedule team sync | 4 | 2 | 5
```
*(Example output with default weights for `quibbles.txt` and stdin examples combined)*

## Development

To run tests:

```bash
cargo test
```
