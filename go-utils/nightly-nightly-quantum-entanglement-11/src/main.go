package main

import (
	"flag"
	"fmt"
	"math/rand"
	"sync"
	"time"

	"github.com/fatih/color"
)

// QuantumNode represents a simulated quantum node
type QuantumNode struct {
	ID           int
	State        string
	EntangledWith *QuantumNode
	mu           sync.Mutex
	ch           chan string
}

// QuantumMetrics tracks simulation statistics
type QuantumMetrics struct {
	mu               sync.Mutex
	TotalNodes       int
	EntangledPairs   int
	IndependentNodes int
	CoherenceScore   float64
	SpookyActions    int
}

// String returns a formatted representation of the node
func (n *QuantumNode) String() string {
	if n.EntangledWith != nil {
		return fmt.Sprintf("⚛️  Node %d (entangled with %d)", n.ID, n.EntangledWith.ID)
	}
	return fmt.Sprintf("⚛️  Node %d (independent)", n.ID)
}

// NewQuantumNode creates a new quantum node
func NewQuantumNode(id int) *QuantumNode {
	return &QuantumNode{
		ID:  id,
		ch:  make(chan string, 100),
		mu:  sync.Mutex{},
	}
}

// SpinState simulates quantum state spinning
func (n *QuantumNode) SpinState(metrics *QuantumMetrics, wg *sync.WaitGroup) {
	defer wg.Done()
	for {
		select {
		case newState := <-n.ch:
			n.mu.Lock()
			n.State = newState
			n.mu.Unlock()
			if n.EntangledWith != nil {
				// Spooky action at a distance!
				n.EntangledWith.ch <- newState
				metrics.mu.Lock()
				metrics.SpookyActions++
				metrics.mu.Unlock()
			}
		case <-time.After(100 * time.Millisecond):
			// Random quantum fluctuation
			n.mu.Lock()
			n.State = fmt.Sprintf("quantum_state_%d", rand.Intn(1000))
			n.mu.Unlock()
		}
	}
}

// Entangle attempts to entangle with another node
func (n *QuantumNode) Entangle(other *QuantumNode, factor float64) bool {
	if rand.Float64() < factor {
		n.mu.Lock()
		n.EntangledWith = other
		n.mu.Unlock()
		return true
	}
	return false
}

// QuantumEntanglementChecker orchestrates the simulation
type QuantumEntanglementChecker struct {
	nodes    []*QuantumNode
	metrics  *QuantumMetrics
	factor   float64
	duration time.Duration
	verbose  bool
}

// NewQuantumEntanglementChecker creates a new checker
func NewQuantumEntanglementChecker(nodeCount int, factor float64, duration time.Duration, verbose bool) *QuantumEntanglementChecker {
	nodes := make([]*QuantumNode, nodeCount)
	for i := 0; i < nodeCount; i++ {
		nodes[i] = NewQuantumNode(i + 1)
	}

	return &QuantumEntanglementChecker{
		nodes:    nodes,
		metrics:  &QuantumMetrics{},
		factor:   factor,
		duration: duration,
		verbose:  verbose,
	}
}

// Initialize sets up quantum entanglement
func (qec *QuantumEntanglementChecker) Initialize() {
	cyan := color.New(color.FgCyan).SprintFunc()
	magenta := color.New(color.FgMagenta).SprintFunc()
	green := color.New(color.FgGreen).SprintFunc()

	fmt.Println(cyan("🔮 Initializing Quantum Entanglement Checker...") + "\n")
	fmt.Printf("📍 Creating %d quantum nodes...\n", len(qec.nodes))

	// Spin up all nodes
	var wg sync.WaitGroup
	for _, node := range qec.nodes {
		wg.Add(1)
		go node.SpinState(qec.metrics, &wg)
	}

	// Wait a moment for nodes to initialize
	time.Sleep(100 * time.Millisecond)

	fmt.Println(magenta("\n🔗 Establishing quantum entanglement...") + "\n")

	// Attempt entanglement
	entangledCount := 0
	for i, node := range qec.nodes {
		for j := i + 1; j < len(qec.nodes); j++ {
			other := qec.nodes[j]
			if node.Entangle(other, qec.factor) {
				if qec.verbose {
					fmt.Printf("✨ %s entangled with %s (spooky action!)\n", node, other)
				}
				entangledCount++
				break // Each node can only be entangled with one other
			}
		}
		if node.EntangledWith == nil {
			if qec.verbose {
				fmt.Printf("✨ %s remains independent (quantum solitude)\n", node)
			}
		}
	}

	// Update metrics
	qec.metrics.TotalNodes = len(qec.nodes)
	qec.metrics.EntangledPairs = entangledCount
	qec.metrics.IndependentNodes = len(qec.nodes) - (entangledCount * 2)

	fmt.Printf("\n⏱️  Running entanglement verification for %v...\n\n", qec.duration)

	// Let the simulation run
	time.Sleep(qec.duration)

	// Calculate coherence score
	qec.calculateCoherence()
}

// calculateCoherence computes the quantum coherence score
func (qec *QuantumEntanglementChecker) calculateCoherence() {
	totalActions := qec.metrics.SpookyActions
	if totalActions == 0 {
		qec.metrics.CoherenceScore = 0
		return
	}

	// Calculate based on entanglement efficiency
	entanglementEfficiency := float64(qec.metrics.EntangledPairs) / float64(qec.metrics.TotalNodes/2)
	spookyEfficiency := float64(qec.metrics.SpookyActions) / float64(qec.metrics.TotalNodes*10)

	if spookyEfficiency > 1.0 {
		spookyEfficiency = 1.0
	}

	qec.metrics.CoherenceScore = (entanglementEfficiency * 0.6 + spookyEfficiency * 0.4) * 100
}

// PrintResults displays the simulation results
func (qec *QuantumEntanglementChecker) PrintResults() {
	cyan := color.New(color.FgCyan).SprintFunc()
	green := color.New(color.FgGreen).SprintFunc()
	yellow := color.New(color.FgYellow).SprintFunc()
	magenta := color.New(color.FgMagenta).SprintFunc()

	fmt.Println(cyan("📊 Entanglement Metrics:"))
	fmt.Printf("   - Total nodes: %d\n", qec.metrics.TotalNodes)
	fmt.Printf("   - Entangled pairs: %d\n", qec.metrics.EntangledPairs)
	fmt.Printf("   - Independent nodes: %d\n", qec.metrics.IndependentNodes)
	fmt.Printf("   - Entanglement factor: %.2f\n", qec.factor)
	fmt.Printf("   - Quantum coherence: %.1f%%\n", qec.metrics.CoherenceScore)
	fmt.Printf("   - Spooky action detected: %d%%\n", int((float64(qec.metrics.SpookyActions)/float64(qec.metrics.TotalNodes*10))*100))

	if qec.metrics.CoherenceScore > 80 {
		fmt.Println(green("\n🎉 Quantum verification complete!") + " " + yellow("High coherence detected!"))
	} else if qec.metrics.CoherenceScore > 50 {
		fmt.Println(yellow("\n⚠️  Quantum verification complete.") + " " + magenta("Moderate coherence detected."))
	} else {
		fmt.Println(magenta("\n🔬 Quantum verification complete.") + " " + yellow("Low coherence detected - check your quantum states!"))
	}
}

func main() {
	rand.Seed(time.Now().UnixNano())

	// Command line flags
	nodeCount := flag.Int("nodes", 5, "Number of quantum nodes to simulate")
	factor := flag.Float64("entanglement-factor", 0.75, "Probability of entanglement (0.0-1.0)")
	durationStr := flag.String("duration", "10s", "Simulation duration")
	verbose := flag.Bool("verbose", false, "Enable detailed output")
	flag.Parse()

	// Parse duration
	duration, err := time.ParseDuration(*durationStr)
	if err != nil {
		fmt.Printf("Error parsing duration: %v\n", err)
		return
	}

	// Validate entanglement factor
	if *factor < 0.0 || *factor > 1.0 {
		fmt.Println("Error: entanglement-factor must be between 0.0 and 1.0")
		return
	}

	// Create and run the quantum entanglement checker
	checker := NewQuantumEntanglementChecker(*nodeCount, *factor, duration, *verbose)
	checker.Initialize()
	checker.PrintResults()
}
