# Nightly Go Raft Ranger

A whimsical-yet-useful CLI tool for managing distributed consensus in a post-apocalyptic Raft cluster. Features animated ASCII raft status, simulated node failures, and leader election visualization.

## Features

- 🚢 Animated ASCII raft status display
- 🗺️ Leader election visualization
- 🌊 Simulated network partitions and node failures
- 📊 Real-time cluster health monitoring
- 🎲 Whimsical post-apocalyptic node names

## Installation

```bash
# Clone the repository
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI

# Build the tool
go build -o nightly-go-raft-ranger go-utils/nightly-go-raft-ranger/src/main.go

# Run it
./nightly-go-raft-ranger
```

## Usage

```bash
# Start a 5-node Raft cluster
./nightly-go-raft-ranger start --nodes 5

# Simulate a network partition
./nightly-go-raft-ranger partition --node 3 --duration 10s

# Kill a node (simulating zombie attack)
./nightly-go-raft-ranger kill --node 2

# Revive a node
./nightly-go-raft-ranger revive --node 2

# View cluster status
./nightly-go-raft-ranger status

# Add a new node
./nightly-go-raft-ranger add-node

# Remove a node
./nightly-go-raft-ranger remove-node --node 4

# View help
./nightly-go-raft-ranger --help
```

## Whimsical Node Names

Nodes are automatically assigned post-apocalyptic names:
- RustyGear
- ByteBender
- CircuitSlinger
- KernelCruncher
- MemoryMarauder
- CacheBandit
- ThreadTwister
- SocketSlinger
- PacketPirate
- ProtocolNomad

## ASCII Art

The tool displays animated ASCII art of a raft floating on waves, with nodes as barrels on the deck. When nodes fail, they fall off the raft into the digital sea!

## Testing

```bash
# Run all tests
go test ./go-utils/nightly-go-raft-ranger/tests/...

# Run specific test
./go-utils/nightly-go-raft-ranger/tests/run_tests.sh
```

## License

MIT - because even in the apocalypse, open source matters!
