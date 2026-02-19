# Nightly Chrono-Task Prioritizer

In the ever-shifting sands of the temporal wasteland, knowing what to do first can mean the difference between survival and becoming a historical anomaly. The `nightly-chrono-task-prioritizer` is a blazing-fast Rust CLI utility designed to help you prioritize your survival tasks based on their 'temporal decay rate' (how quickly they become irrelevant or impossible) and their 'survival impact' (how critical they are to your continued existence).

## Features

*   **High Performance**: Written in Rust for speed and efficiency.
*   **Simple Input**: Takes a CSV-like file or standard input with task details.
*   **Intelligent Prioritization**: Calculates a priority score based on decay and impact.
*   **Clear Output**: Presents a sorted list of tasks, highest priority first.

## Installation

To install `nightly-chrono-task-prioritizer`, you'll need Rust and Cargo installed. If you don't have them, visit [rust-lang.org](https://www.rust-lang.org/tools/install).

```bash
cargo install nightly-chrono-task-prioritizer
```

## Usage

The utility expects input in a simple CSV-like format: `Task Name,Decay Rate (0-10),Survival Impact (0-10)`.

*   **Decay Rate**: A numerical value from 0 (never decays/becomes irrelevant) to 10 (decays almost instantly/becomes irrelevant very quickly).
*   **Survival Impact**: A numerical value from 0 (minimal impact on survival) to 10 (absolutely critical for survival).

### From a file:

```bash
nightly-chrono-task-prioritizer <path_to_tasks_file.txt>
```

### From standard input:

```bash
cat <path_to_tasks_file.txt> | nightly-chrono-task-prioritizer
# Or type directly:
nightly-chrono-task-prioritizer
# Then enter tasks, press Ctrl+D when done.
```

### Example `tasks.txt`:

```
Repair temporal flux capacitor,1,10
Scavenge for temporal dust,8,5
Polish time-travel boots,0,1
Stabilize local time bubble,10,10
Calibrate chronometer,3,7
Gather paradox-proof berries,5,6
```

### Example Output:

```bash
$ nightly-chrono-task-prioritizer tasks.txt
Prioritized Tasks:
------------------
1. Repair temporal flux capacitor (Priority: 5.50)
2. Calibrate chronometer (Priority: 2.67)
3. Polish time-travel boots (Priority: 2.00)
4. Gather paradox-proof berries (Priority: 1.17)
5. Stabilize local time bubble (Priority: 1.00)
6. Scavenge for temporal dust (Priority: 0.67)
```

## How it Works

The priority score is calculated as `(Survival Impact + 1) / (Decay Rate + 1)`. Adding 1 to both values prevents division by zero and ensures that even tasks with 0 decay or 0 impact still contribute to the score, albeit minimally. A higher score indicates higher priority.
