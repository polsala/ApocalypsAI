# Nightly Go Raft Race Tracker

A whimsical-yet-useful distributed race tracker built in Go using Raft consensus. Perfect for tracking fun competitions, hackathons, or any distributed race scenario where you need reliable coordination across multiple nodes.

## Features

- **Distributed Consensus**: Uses Raft algorithm for reliable leader election and log replication
- **Whimsical Race Tracking**: Track racers, update positions, and maintain a persistent leaderboard
- **RESTful API**: Simple HTTP endpoints for managing races and racers
- **Leader Discovery**: Automatic leader detection for read/write operations
- **Self-Healing**: Nodes automatically recover from failures

## Quick Start

### Prerequisites

- Go 1.22+
- Three available ports (default: 8080, 8081, 8082)

### Running a Single Node

```bash
# Start the first node (will become leader)
go run main.go --node-id=node1 --http-port=8080 --raft-port=7001

# In another terminal, add a racer
curl -X POST http://localhost:8080/racers \
  -H "Content-Type: application/json" \
  -d '{"name":"Speedy Sam","team":"A"}'

# Update their position
curl -X POST http://localhost:8080/racers/1/position \
  -H "Content-Type: application/json" \
  -d '{"position":1,"time":"00:01:23.45"}'

# Get the leaderboard
curl http://localhost:8080/leaderboard
```

### Running a Three-Node Cluster

```bash
# Terminal 1: Start node1
go run main.go --node-id=node1 --http-port=8080 --raft-port=7001 \
  --join-addr=http://localhost:8081 --join-addr=http://localhost:8082

# Terminal 2: Start node2
go run main.go --node-id=node2 --http-port=8081 --raft-port=7002 \
  --join-addr=http://localhost:8080 --join-addr=http://localhost:8082

# Terminal 3: Start node3
go run main.go --node-id=node3 --http-port=8082 --raft-port=7003 \
  --join-addr=http://localhost:8080 --join-addr=http://localhost:8081

# Verify cluster health
curl http://localhost:8080/health
```

### API Endpoints

#### Racers

- `POST /racers` - Add a new racer
  ```json
  {
    "name": "Speedy Sam",
    "team": "A"
  }
  ```

- `GET /racers` - List all racers
- `GET /racers/{id}` - Get specific racer

#### Race Management

- `POST /racers/{id}/position` - Update racer position
  ```json
  {
    "position": 1,
    "time": "00:01:23.45"
  }
  ```

- `GET /leaderboard` - Get current leaderboard
- `POST /race/reset` - Reset all positions

#### Cluster

- `GET /health` - Health check
- `GET /leader` - Get current leader address
- `GET /nodes` - List all cluster nodes

## Example Usage

```bash
# Add multiple racers
curl -X POST http://localhost:8080/racers -H "Content-Type: application/json" \
  -d '{"name":"Racer Alice","team":"Red"}'
curl -X POST http://localhost:8080/racers -H "Content-Type: application/json" \
  -d '{"name":"Racer Bob","team":"Blue"}'
curl -X POST http://localhost:8080/racers -H "Content-Type: application/json" \
  -d '{"name":"Racer Carol","team":"Green"}'

# Update positions as the race progresses
curl -X POST http://localhost:8080/racers/1/position \
  -H "Content-Type: application/json" \
  -d '{"position":2,"time":"00:01:30.12"}'
curl -X POST http://localhost:8080/racers/2/position \
  -H "Content-Type: application/json" \
  -d '{"position":1,"time":"00:01:28.45"}'
curl -X POST http://localhost:8080/racers/3/position \
  -H "Content-Type: application/json" \
  -d '{"position":3,"time":"00:01:35.67"}'

# Check the leaderboard
curl http://localhost:8080/leaderboard
```

## Architecture

The race tracker uses HashiCorp's Raft implementation for Go:

- **Raft Consensus**: Ensures all nodes agree on race state
- **HTTP API**: RESTful interface for race operations
- **Leader Election**: Automatic failover if leader node fails
- **Persistent Storage**: Race data survives node restarts

## Testing

```bash
# Run unit tests
go test ./...

# Run integration tests
go test -tags=integration ./...
```

## License

MIT - Use it for tracking races in your apocalypse or just for fun!

## Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Submit a PR

## Inspiration

Built for the ApocalypsAI community as a fun way to track distributed competitions while demonstrating Raft consensus in action!
