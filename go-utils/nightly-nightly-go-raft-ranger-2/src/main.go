package main

import (
	"fmt"
	"log"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/urfave/cli/v2"
)

// Raft node states
type State int

const (
	Follower State = iota
	Candidate
	Leader
)

var stateColors = map[State]string{
	Follower:  "\033[36m", // Cyan
	Candidate: "\033[33m", // Yellow
	Leader:    "\033[32m", // Green
}

var stateNames = map[State]string{
	Follower:  "Follower",
	Candidate: "Candidate",
	Leader:    "Leader",
}

var resetColor = "\033[0m"

// Node represents a Raft node
type Node struct {
	ID       int
	State    State
	Term     int
	Votes    int
	LeaderID int
	Log      []int
	VoteFor  int
}

// String returns a colored representation of the node
func (n *Node) String() string {
	color := stateColors[n.State]
	stateName := stateNames[n.State]
	return fmt.Sprintf("%s[%d] %s%s", color, n.ID, stateName, resetColor)
}

// RaftSimulation represents the entire Raft cluster
type RaftSimulation struct {
	Nodes         []*Node
	CurrentTerm   int
	CurrentLeader int
	ElectionTimer *time.Timer
	ElectionTimeout time.Duration
	Running       bool
	LogIndex      int
}

// NewRaftSimulation creates a new Raft simulation
func NewRaftSimulation(numNodes int, electionTimeout time.Duration) *RaftSimulation {
	nodes := make([]*Node, numNodes)
	for i := 0; i < numNodes; i++ {
		nodes[i] = &Node{
			ID:       i,
			State:    Follower,
			Term:     0,
			LeaderID: -1,
			VoteFor:  -1,
			Log:      make([]int, 0),
		}
	}

	return &RaftSimulation{
		Nodes:           nodes,
		CurrentTerm:     0,
		CurrentLeader:   -1,
		ElectionTimeout: electionTimeout,
		Running:         true,
		LogIndex:        0,
	}
}

// Start begins the simulation
func (s *RaftSimulation) Start() {
	rand.Seed(time.Now().UnixNano())
	s.printHeader()
	s.printNodes()

	// Start election timer
	s.startElectionTimer()

	// Main simulation loop
	for s.Running {
		time.Sleep(100 * time.Millisecond)
	}
}

// startElectionTimer starts a random election timeout
func (s *RaftSimulation) startElectionTimer() {
	if s.ElectionTimer != nil {
		s.ElectionTimer.Stop()
	}

	// Random timeout between electionTimeout and electionTimeout*2
	randTimeout := s.ElectionTimeout + time.Duration(rand.Int63n(int64(s.ElectionTimeout)))

	s.ElectionTimer = time.AfterFunc(randTimeout, func() {
		if s.CurrentLeader == -1 {
			s.startElection()
		} else {
			s.startHeartbeat()
		}
	})
}

// startElection initiates a new election
func (s *RaftSimulation) startElection() {
	if !s.Running {
		return
	}

	// Choose a random candidate
	candidateID := rand.Intn(len(s.Nodes))
	candidate := s.Nodes[candidateID]

	// Reset all nodes to follower state
	for _, node := range s.Nodes {
		node.State = Follower
		node.VoteFor = -1
		node.Votes = 0
	}

	// Candidate becomes candidate
	candidate.State = Candidate
	candidate.Term++
	s.CurrentTerm = candidate.Term
	candidate.VoteFor = candidate.ID
	candidate.Votes = 1

	fmt.Printf("\nElection timeout! Node %d becomes Candidate...\n", candidate.ID)
	s.printNodes()

	// Simulate voting
	time.Sleep(500 * time.Millisecond)

	votesNeeded := len(s.Nodes)/2 + 1
	votesReceived := 1

	for i, node := range s.Nodes {
		if i == candidateID {
			continue
		}
		if s.simulateVote(node, candidate) {
			votesReceived++
			fmt.Printf("Vote received from Node %d\n", node.ID)
			time.Sleep(200 * time.Millisecond)
		}
	}

	if votesReceived >= votesNeeded {
		// Candidate wins
		candidate.State = Leader
		s.CurrentLeader = candidate.ID
		fmt.Printf("\n🎉 Node %d becomes Leader (Term %d)!\n", candidate.ID, candidate.Term)
		s.printNodes()

		// Start replicating logs
		s.replicateLogs(candidate)
	} else {
		fmt.Printf("\n❌ Election failed. Node %d did not receive enough votes.\n", candidate.ID)
		s.startElectionTimer()
	}
}

// simulateVote simulates a node voting for a candidate
func (s *RaftSimulation) simulateVote(node *Node, candidate *Node) bool {
	// In a real Raft implementation, we'd check log consistency
	// For this simulation, just vote randomly with 80% probability
	if rand.Float32() < 0.8 {
		node.VoteFor = candidate.ID
		candidate.Votes++
		return true
	}
	return false
}

// startHeartbeat simulates leader sending heartbeats
func (s *RaftSimulation) startHeartbeat() {
	if s.CurrentLeader == -1 || !s.Running {
		return
	}

	leader := s.Nodes[s.CurrentLeader]
	fmt.Printf("\n💓 Heartbeat from Leader %d (Term %d)\n", leader.ID, leader.Term)
	s.printNodes()

	// Occasionally add a new log entry
	if rand.Float32() < 0.3 {
		s.replicateLogs(leader)
	}

	s.startElectionTimer()
}

// replicateLogs simulates the leader replicating logs to followers
func (s *RaftSimulation) replicateLogs(leader *Node) {
	if !s.Running {
		return
	}

	s.LogIndex++
	newLogEntry := s.LogIndex
	fmt.Printf("\nLeader replicating log entry %d...\n", newLogEntry)

	// Replicate to followers
	allReplicated := true
	for i, node := range s.Nodes {
		if i == leader.ID {
			continue
		}
		if s.simulateReplication(node, newLogEntry) {
			fmt.Printf("✓ Log replicated to Node %d\n", node.ID)
		} else {
			fmt.Printf("✗ Failed to replicate to Node %d\n", node.ID)
			allReplicated = false
		}
		time.Sleep(100 * time.Millisecond)
	}

	if allReplicated {
		fmt.Printf("Log replicated to all followers!\n")
		leader.Log = append(leader.Log, newLogEntry)
	} else {
		fmt.Printf("Some replicas failed. Leader will retry.\n")
	}

	s.startElectionTimer()
}

// simulateReplication simulates log replication to a follower
func (s *RaftSimulation) simulateReplication(node *Node, entry int) bool {
	// Simulate network delay and potential failure
	time.Sleep(100 * time.Millisecond)
	if rand.Float32() < 0.05 {
		return false // 5% failure rate
	}
	node.Log = append(node.Log, entry)
	return true
}

// printHeader prints the simulation header
func (s *RaftSimulation) printHeader() {
	fmt.Println("Raft Ranger - Consensus Visualization")
	fmt.Println("====================================")
	fmt.Printf("\nNodes: %d (Term: %d)\n\n", len(s.Nodes), s.CurrentTerm)
}

// printNodes prints the current state of all nodes
func (s *RaftSimulation) printNodes() {
	var nodeStrings []string
	for _, node := range s.Nodes {
		nodeStrings = append(nodeStrings, node.String())
	}
	fmt.Println(strings.Join(nodeStrings, "  "))
}

func main() {
	app := &cli.App{
		Name:  "raft-ranger",
		Usage: "Visualize Raft consensus algorithm with ASCII art",
		Flags: []cli.Flag{
			&cli.IntFlag{
				Name:    "nodes",
				Aliases: []string{"n"},
				Value:   5,
				Usage:   "Number of Raft nodes",
			},
			&cli.IntFlag{
				Name:    "timeout",
				Aliases: []string{"t"},
				Value:   1000,
				Usage:   "Election timeout in milliseconds",
			},
		},
		Action: func(c *cli.Context) error {
			numNodes := c.Int("nodes")
			timeout := c.Int("timeout")

			if numNodes < 3 {
				return fmt.Errorf("number of nodes must be at least 3, got %d", numNodes)
			}

			simulation := NewRaftSimulation(numNodes, time.Duration(timeout)*time.Millisecond)
			simulation.Start()
			return nil
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}
