# nightly-todo-prioritizer

**Utility:** Sort a plain‑text TODO list by priority tags.

## Overview

`nightly-todo-prioritizer` reads a TODO file (default `TODO.txt`) and reorders the lines so that tasks with explicit priority tags appear first, ordered from highest to lowest priority.  Priority tags are of the form `[P1]`, `[P2]`, … where a lower number means higher importance.  Lines without a tag are treated as lowest priority and appear at the end, preserving their original order relative to each other.

The script is pure Bash, has no external dependencies, and works offline – perfect for a quick daily run or as part of a larger automation pipeline.

## Installation

```bash
# Clone the repository (or copy the files into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/utils/nightly-todo-prioritizer

# Make the script executable
chmod +x src/priority_sort.sh
```

## Usage

```bash
# Sort the default TODO.txt in the current directory
./src/priority_sort.sh

# Or specify a custom file
./src/priority_sort.sh path/to/my_tasks.txt
```

The sorted list is printed to **stdout**.  Redirect it to a file if you want to overwrite the original list:

```bash
./src/priority_sort.sh TODO.txt > TODO.sorted.txt && mv TODO.sorted.txt TODO.txt
```

## Priority Tag Syntax

- `[P1]` – Highest priority
- `[P2]` – Next highest
- …
- Any line without a `[Px]` tag is considered lowest priority.

## Example

**Input (`TODO.txt`):**

```
Buy milk [P2]
Fix critical bug [P1]
Read book
Write documentation [P3]
```

**Command:**

```bash
./src/priority_sort.sh TODO.txt
```

**Output:**

```
Fix critical bug [P1]
Buy milk [P2]
Write documentation [P3]
Read book
```

## Testing

Run the bundled test suite with:

```bash
./tests/test_priority_sort.sh
```

The test creates a temporary TODO file, runs the sorter, and verifies the output matches the expected ordering.

## License

MIT © ApocalypsAI
