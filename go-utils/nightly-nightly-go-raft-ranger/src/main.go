package main

import (
	"bufio"
	"fmt"
	"log"
	"math/rand"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"sync"
	"time"
)

// Node represents a Raft node
type Node struct {
	ID       int
	Name     string
	Status   string // "leader", "follower", "candidate", "dead"
	Term     int
	Log      []string
	VoteFor  int
	Alive    bool
	Mutex    sync.RWMutex
}

// RaftCluster represents the entire cluster
type RaftCluster struct {
	Nodes        []*Node
	LeaderID     int
	CurrentTerm  int
	Mutex        sync.RWMutex
	Running      bool
	Animation    *Animation
}

// Animation handles the ASCII art display
type Animation struct {
	Cluster *RaftCluster
	Running bool
	Mutex   sync.RWMutex
}

// Post-apocalyptic node names
var postApocNames = []string{
	"RustyGear", "ByteBender", "CircuitSlinger", "KernelCruncher",
	"MemoryMarauder", "CacheBandit", "ThreadTwister", "SocketSlinger",
	"PacketPirate", "ProtocolNomad", "FirewallFury", "RouterReaper",
	"SwitchSlayer", "HubHavoc", "BridgeBandit", "GatewayGhoul",
}

// NewRaftCluster creates a new Raft cluster
func NewRaftCluster(nodeCount int) *RaftCluster {
	nodes := make([]*Node, nodeCount)
	for i := 0; i < nodeCount; i++ {
		nameIndex := i % len(postApocNames)
		nodes[i] = &Node{
			ID:     i,
			Name:   postApocNames[nameIndex],
			Status: "follower",
			Term:   0,
			Alive:  true,
		}
	}

	cluster := &RaftCluster{
		Nodes:       nodes,
		LeaderID:    -1,
		CurrentTerm: 0,
		Running:     true,
	}
	cluster.Animation = &Animation{Cluster: cluster, Running: true}

	return cluster
}

// StartElection starts an election for a specific node
func (c *RaftCluster) StartElection(nodeID int) {
	c.Mutex.Lock()
	defer c.Mutex.Unlock()

	if nodeID < 0 || nodeID >= len(c.Nodes) {
		return
	}

	node := c.Nodes[nodeID]
	node.Mutex.Lock()
	if !node.Alive || node.Status == "leader" {
		node.Mutex.Unlock()
		return
	}

	c.CurrentTerm++
	node.Status = "candidate"
	node.Term = c.CurrentTerm
	node.VoteFor = node.ID

	votes := 1
	totalNodes := 0

	// Request votes from other nodes
	for i, otherNode := range c.Nodes {
		if i == nodeID {
			continue
		}
		otherNode.Mutex.Lock()
		if otherNode.Alive {
			totalNodes++
			if otherNode.VoteFor == -1 || otherNode.Term < node.Term {
				otherNode.VoteFor = node.ID
				votes++
			}
		}
		otherNode.Mutex.Unlock()
	}

	// Check if candidate won
	if votes > totalNodes/2 {
		c.LeaderID = node.ID
		node.Status = "leader"
		for _, otherNode := range c.Nodes {
			otherNode.Mutex.Lock()
			otherNode.VoteFor = node.ID
			otherNode.Mutex.Unlock()
		}
	} else {
		node.Status = "follower"
	}
}

// KillNode simulates killing a node
func (c *RaftCluster) KillNode(nodeID int) {
	c.Mutex.Lock()
	defer c.Mutex.Unlock()

	if nodeID < 0 || nodeID >= len(c.Nodes) {
		return
	}

	node := c.Nodes[nodeID]
	node.Mutex.Lock()
	defer node.Mutex.Unlock()

	node.Alive = false
	node.Status = "dead"

	// If leader died, trigger new election
	if c.LeaderID == nodeID {
		c.LeaderID = -1
		go c.TriggerElection()
	}
}

// ReviveNode revives a dead node
func (c *RaftCluster) ReviveNode(nodeID int) {
	c.Mutex.Lock()
	defer c.Mutex.Unlock()

	if nodeID < 0 || nodeID >= len(c.Nodes) {
		return
	}

	node := c.Nodes[nodeID]
	node.Mutex.Lock()
	defer node.Mutex.Unlock()

	node.Alive = true
	node.Status = "follower"
	node.VoteFor = -1
}

// TriggerElection triggers an election after a random delay
func (c *RaftCluster) TriggerElection() {
	time.Sleep(time.Duration(rand.Intn(1000)+500) * time.Millisecond)
	c.Mutex.RLock()
	if c.LeaderID != -1 {
		c.Mutex.RUnlock()
		return
	}
	c.Mutex.RUnlock()

	// Start election for a random alive node
	aliveNodes := []int{}
	for i, node := range c.Nodes {
		node.Mutex.RLock()
		if node.Alive {
			aliveNodes = append(aliveNodes, i)
		}
		node.Mutex.RUnlock()
	}

	if len(aliveNodes) > 0 {
		randNode := aliveNodes[rand.Intn(len(aliveNodes))]
		c.StartElection(randNode)
	}
}

// AddNode adds a new node to the cluster
func (c *RaftCluster) AddNode() {
	c.Mutex.Lock()
	defer c.Mutex.Unlock()

	newNodeID := len(c.Nodes)
	nameIndex := newNodeID % len(postApocNames)
	newNode := &Node{
		ID:     newNodeID,
		Name:   postApocNames[nameIndex],
		Status: "follower",
		Term:   0,
		Alive:  true,
	}

	c.Nodes = append(c.Nodes, newNode)
}

// RemoveNode removes a node from the cluster
func (c *RaftCluster) RemoveNode(nodeID int) {
	c.Mutex.Lock()
	defer c.Mutex.Unlock()

	if nodeID < 0 || nodeID >= len(c.Nodes) {
		return
	}

	// If removing leader, trigger election
	if c.LeaderID == nodeID {
		c.LeaderID = -1
		go c.TriggerElection()
	}

	// Remove node from slice
	c.Nodes = append(c.Nodes[:nodeID], c.Nodes[nodeID+1:]...)

	// Update IDs of remaining nodes
	for i := nodeID; i < len(c.Nodes); i++ {
		c.Nodes[i].ID = i
	}
}

// GetStatus returns cluster status
func (c *RaftCluster) GetStatus() string {
	c.Mutex.RLock()
	defer c.Mutex.RUnlock()

	status := fmt.Sprintf("Cluster Status (Term: %d, Leader: %d)\n", c.CurrentTerm, c.LeaderID)
	for _, node := range c.Nodes {
		node.Mutex.RLock()
		status += fmt.Sprintf("  Node %d (%s): %s (Term: %d, Alive: %v)\n",
			node.ID, node.Name, node.Status, node.Term, node.Alive)
		node.Mutex.RUnlock()
	}
	return status
}

// StartAnimation starts the ASCII animation
func (a *Animation) Start() {
	go func() {
		for a.Running {
			time.Sleep(500 * time.Millisecond)
			a.Render()
		}
	}()
}

// StopAnimation stops the ASCII animation
func (a *Animation) Stop() {
	a.Mutex.Lock()
	a.Running = false
	a.Mutex.Unlock()
}

// Render renders the ASCII raft animation
func (a *Animation) Render() {
	clearScreen()

	fmt.Println("  🌊  🌊  🌊  🌊  🌊  🌊  🌊  🌊  🌊  🌊")
	fmt.Println("  🌊  🌊  🌊  🌊  🌊  🌊  🌊  🌊  🌊  🌊")
	fmt.Println("  🌊  🌊  🌊  🌊  🌊  🌊  🌊  🌊  🌊  🌊")
	fmt.Println()

	// Draw the raft
	fmt.Println("  +-------------------------------+")
	fmt.Println("  |                               |")
	fmt.Println("  |    RAFT CLUSTER STATUS        |")
	fmt.Println("  |                               |")
	fmt.Println("  +-------------------------------+")
	fmt.Println()

	a.Mutex.RLock()
	cluster := a.Cluster
	nodeLine := "  |"
	for _, node := range cluster.Nodes {
		node.Mutex.RLock()
		if node.Alive {
			if node.Status == "leader" {
				nodeLine += " 🏆 "
			} else {
				nodeLine += " 🛠️  "
			}
		} else {
			nodeLine += " 💀 "
		}
		node.Mutex.RUnlock()
	}
	nodeLine += "|"
	fmt.Println(nodeLine)
	fmt.Println()

	// Node details
	for _, node := range cluster.Nodes {
		node.Mutex.RLock()
		statusEmoji := ""
		if node.Status == "leader" {
			statusEmoji = "👑"
		} else if node.Status == "candidate" {
			statusEmoji = "竞选"
		} else if !node.Alive {
			statusEmoji = "💀"
		} else {
			statusEmoji = "👤"
		}
		fmt.Printf("  Node %d (%s): %s %s (Term: %d)\n",
			node.ID, node.Name, statusEmoji, node.Status, node.Term)
		node.Mutex.RUnlock()
	}

	fmt.Println()
	fmt.Printf("  Current Term: %d\n", cluster.CurrentTerm)
	if cluster.LeaderID >= 0 {
		fmt.Printf("  Leader: Node %d (%s)\n", cluster.LeaderID, cluster.Nodes[cluster.LeaderID].Name)
	} else {
		fmt.Println("  Leader: None (Election in progress...)")
	}

	fmt.Println()
	fmt.Println("  Commands:")
	fmt.Println("    kill <id>    - Kill a node")
	fmt.Println("    revive <id>  - Revive a node")
	fmt.Println("    add          - Add a new node")
	fmt.Println("    remove <id>  - Remove a node")
	fmt.Println("    status       - Show cluster status")
	fmt.Println("    quit         - Exit")

	a.Mutex.RUnlock()
}

// clearScreen clears the terminal screen
func clearScreen() {
	cmd := exec.Command("clear")
	if os.Getenv("GOOS") == "windows" {
		cmd = exec.Command("cmd", "/c", "cls")
	}
	cmd.Stdout = os.Stdout
	cmd.Run()
}

// CLI commands
func handleCommand(cluster *RaftCluster, cmd string) {
	parts := strings.Fields(cmd)
	if len(parts) == 0 {
		return
	}

	switch parts[0] {
	case "kill":
		if len(parts) < 2 {
			fmt.Println("Usage: kill <node_id>")
			return
		}
		nodeID, err := strconv.Atoi(parts[1])
		if err != nil {
			fmt.Println("Invalid node ID")
			return
		}
		cluster.KillNode(nodeID)
		fmt.Printf("Node %d killed! 💀\n", nodeID)

	case "revive":
		if len(parts) < 2 {
			fmt.Println("Usage: revive <node_id>")
			return
		}
		nodeID, err := strconv.Atoi(parts[1])
		if err != nil {
			fmt.Println("Invalid node ID")
			return
		}
		cluster.ReviveNode(nodeID)
		fmt.Printf("Node %d revived! 🔄\n", nodeID)

	case "add":
		cluster.AddNode()
		fmt.Println("New node added! ➕")
		go cluster.TriggerElection()

	case "remove":
		if len(parts) < 2 {
			fmt.Println("Usage: remove <node_id>")
			return
		}
		nodeID, err := strconv.Atoi(parts[1])
		if err != nil {
			fmt.Println("Invalid node ID")
			return
		}
		cluster.RemoveNode(nodeID)
		fmt.Printf("Node %d removed! ➖\n", nodeID)
		go cluster.TriggerElection()

	case "status":
		fmt.Println(cluster.GetStatus())

	case "quit", "exit":
		cluster.Animation.Stop()
		cluster.Running = false
		os.Exit(0)

	default:
		fmt.Println("Unknown command. Try: kill, revive, add, remove, status, quit")
	}
}

func main() {
	rand.Seed(time.Now().UnixNano())

	// Default to 5 nodes
	nodeCount := 5
	if len(os.Args) > 1 {
		if os.Args[1] == "start" && len(os.Args) > 2 {
			n, err := strconv.Atoi(os.Args[2])
			if err == nil {
				nodeCount = n
			}
		}
	}

	cluster := NewRaftCluster(nodeCount)
	cluster.Animation.Start()

	fmt.Printf("Starting Raft cluster with %d nodes...\n", nodeCount)
	time.Sleep(1 * time.Second)

	// Start initial election
	go cluster.TriggerElection()

	// Interactive CLI
	scanner := bufio.NewScanner(os.Stdin)
	for cluster.Running {
		fmt.Print("raft> ")
		if scanner.Scan() {
			handleCommand(cluster, scanner.Text())
		}
		time.Sleep(100 * time.Millisecond)
	}
}
