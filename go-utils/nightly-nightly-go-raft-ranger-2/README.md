# Nightly Go Raft Ranger

A whimsical, interactive CLI for visualizing the Raft consensus algorithm elections and log replication with ASCII art.

## Features
- Simulate Raft elections with ASCII art nodes
- Visualize log replication across nodes
- Interactive CLI with color-coded states
- Educational tool for understanding distributed consensus

## Installation

```bash
# Clone the repository
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/go-utils/nightly-go-raft-ranger

# Build the binary
go build -o raft-ranger ./src

# Run the simulation
./raft-ranger
```

## Usage

```bash
# Start a simulation with 5 nodes
./raft-ranger --nodes 5

# Start with custom election timeout (ms)
./raft-ranger --nodes 3 --timeout 1000

# View help
./raft-ranger --help
```

## Example Output

```
Raft Ranger - Consensus Visualization
====================================

Nodes: 5 (Term: 1)

[0] Follower  [1] Follower  [2] Follower  [3] Follower  [4] Follower

Election timeout! Node 2 becomes Candidate...

[0] Follower  [1] Follower  [2] Candidate   [3] Follower  [4] Follower

Vote received from Node 0
Vote received from Node 1
Vote received from Node 2
Vote received from Node 3
Vote received from Node 4

🎉 Node 2 becomes Leader (Term 1)!

[0] Follower  [1] Follower  [2] Leader      [3] Follower  [4] Follower

Leader replicating log entry 1...
Log replicated to all followers!
```

## License

MIT
