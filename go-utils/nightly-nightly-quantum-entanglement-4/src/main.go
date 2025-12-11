package main

import (
	"flag"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

// QuantumState represents the quantum state of a node
type QuantumState struct {
	NodeID    string
	Spin      float64
	Phase     float64
	Fidelity  float64
	Timestamp time.Time
}

// EntanglementResult represents the result of entanglement verification
type EntanglementResult struct {
	NodeA         string
	NodeB         string
	Fidelity      float64
	SpookyScore   float64
	Correlated    bool
	BellInequality string
}

// QuantumChecker manages quantum entanglement verification
type QuantumChecker struct {
	Verbose bool
}

// NewQuantumChecker creates a new quantum checker
func NewQuantumChecker(verbose bool) *QuantumChecker {
	return &QuantumChecker{Verbose: verbose}
}

// GenerateQuantumStates generates quantum states for all nodes
func (qc *QuantumChecker) GenerateQuantumStates(nodes []string) []QuantumState {
	states := make([]QuantumState, len(nodes))
	baseSpin := rand.Float64() * 2.0 - 1.0 // Random spin between -1 and 1
	basePhase := rand.Float64() * 2.0 * 3.14159 // Random phase between 0 and 2π
timestamp := time.Now()

	for i, node := range nodes {
		// Create entangled states with slight variations
		spinVariation := (rand.Float64() - 0.5) * 0.1
		phaseVariation := (rand.Float64() - 0.5) * 0.2

		states[i] = QuantumState{
			NodeID:    node,
			Spin:      baseSpin + spinVariation,
			Phase:     basePhase + phaseVariation,
			Fidelity:  0.95 + rand.Float64()*0.05, // 95-100%
			Timestamp: timestamp,
		}

		if qc.Verbose {
			fmt.Printf("🔬 Generated quantum state for %s: spin=%.3f, phase=%.3f, fidelity=%.1f%%\n",
				node, states[i].Spin, states[i].Phase, states[i].Fidelity*100)
		}
	}

	return states
}

// VerifyEntanglement verifies entanglement between two quantum states
func (qc *QuantumChecker) VerifyEntanglement(stateA, stateB QuantumState) EntanglementResult {
	// Calculate correlation based on spin and phase differences
	spinDiff := stateA.Spin - stateB.Spin
	phaseDiff := stateA.Phase - stateB.Phase
	correlation := 1.0 - (absFloat(spinDiff)*0.5 + absFloat(phaseDiff)/(2*3.14159)*0.5)

	// Apply quantum decoherence effect
	timeDiff := time.Since(stateA.Timestamp).Seconds()
	decoherence := timeDiff * 0.01
	finalCorrelation := correlation - decoherence

	// Ensure correlation stays within bounds
	if finalCorrelation < 0 {
		finalCorrelation = 0
	}

	// Calculate entanglement fidelity
	baseFidelity := (stateA.Fidelity + stateB.Fidelity) / 2
	entanglementFidelity := baseFidelity * finalCorrelation

	// Calculate spooky action score
	spookyScore := finalCorrelation*10.0 + rand.Float64()*0.5
	if spookyScore > 10.0 {
		spookyScore = 10.0
	}

	// Determine if states are correlated
	correlated := finalCorrelation > 0.7

	// Determine Bell inequality status
	bellInequality := "VIOLATED"
	if !correlated {
		bellInequality = "SATISFIED"
	}

	return EntanglementResult{
		NodeA:         stateA.NodeID,
		NodeB:         stateB.NodeID,
		Fidelity:      entanglementFidelity,
		SpookyScore:   spookyScore,
		Correlated:    correlated,
		BellInequality: bellInequality,
	}
}

// VerifyAllEntanglements verifies entanglement between all pairs of nodes
func (qc *QuantumChecker) VerifyAllEntanglements(states []QuantumState) []EntanglementResult {
	n := len(states)
	results := make([]EntanglementResult, 0, n*(n-1)/2)
	var mu sync.Mutex
	var wg sync.WaitGroup

	// Use goroutines to verify entanglement concurrently
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			wg.Add(1)
			go func(i, j int) {
				defer wg.Done()
				result := qc.VerifyEntanglement(states[i], states[j])
				mu.Lock()
				results = append(results, result)
				mu.Unlock()
			}(i, j)
		}
	}

	wg.Wait()
	return results
}

// CalculateOverallEntanglement calculates the overall system entanglement
func (qc *QuantumChecker) CalculateOverallEntanglement(results []EntanglementResult) float64 {
	if len(results) == 0 {
		return 0
	}

	totalFidelity := 0.0
	for _, result := range results {
		totalFidelity += result.Fidelity
	}

	return totalFidelity / float64(len(results))
}

// GenerateReport generates a whimsical quantum report
func (qc *QuantumChecker) GenerateReport(nodes []string, results []EntanglementResult, overallFidelity float64) {
	fmt.Println("\n✨ Quantum Entanglement Report:\n")

	for _, result := range results {
		status := "❌ DECOHERED"
		if result.Correlated {
			status = "✅ CORRELATED"
		}

		fmt.Printf("Node A (%s) ↔ Node B (%s)\n", result.NodeA, result.NodeB)
		fmt.Printf("  • Entanglement Fidelity: %.1f%%\n", result.Fidelity*100)
		fmt.Printf("  • Spooky Action Score: %.1f/10\n", result.SpookyScore)
		fmt.Printf("  • Quantum State: %s\n", status)
		fmt.Printf("  • Bell Inequality: %s (as expected!)\n\n", result.BellInequality)
	}

	fmt.Printf("🎉 Overall System Entanglement: %.1f%%", overallFidelity*100)

	// Add whimsical rating
	if overallFidelity > 0.95 {
		fmt.Println(" (EXCELLENT)")
		fmt.Println("\n🔮 Quantum Recommendation: Your distributed system exhibits strong quantum correlations!")
	} else if overallFidelity > 0.85 {
		fmt.Println(" (GOOD)")
		fmt.Println("\n🔮 Quantum Recommendation: Your system shows promising quantum behavior!")
	} else if overallFidelity > 0.7 {
		fmt.Println(" (FAIR)")
		fmt.Println("\n🔮 Quantum Recommendation: Consider checking for quantum interference sources.")
	} else {
		fmt.Println(" (POOR)")
		fmt.Println("\n🔮 Quantum Recommendation: Your system may need quantum error correction.")
	}
}

// absFloat returns the absolute value of a float64
func absFloat(x float64) float64 {
	if x < 0 {
		return -x
	}
	return x
}

func main() {
	// Parse command line flags
	nodesFlag := flag.String("nodes", "node1,node2,node3", "comma-separated list of node names")
	verboseFlag := flag.Bool("verbose", false, "enable verbose quantum state output")
	flag.Parse()

	// Parse nodes
	nodes := []string{"node1", "node2", "node3"}
	if *nodesFlag != "" {
		nodes = []string{}
		for _, node := range splitNodes(*nodesFlag) {
			nodes = append(nodes, node)
		}
	}

	// Seed random number generator
	rand.Seed(time.Now().UnixNano())

	// Create quantum checker
	qc := NewQuantumChecker(*verboseFlag)

	fmt.Println("🔬 Initializing Quantum Entanglement Checker...")
	fmt.Printf("\n📡 Establishing quantum links between %d nodes...\n", len(nodes))

	// Generate quantum states
	states := qc.GenerateQuantumStates(nodes)

	// Verify entanglement
	results := qc.VerifyAllEntanglements(states)

	// Calculate overall entanglement
	overallFidelity := qc.CalculateOverallEntanglement(results)

	// Generate report
	qc.GenerateReport(nodes, results, overallFidelity)
}

// splitNodes splits a comma-separated string into a slice
func splitNodes(nodesStr string) []string {
	nodes := []string{}
	current := ""
	for _, char := range nodesStr {
		if char == ',' {
			if current != "" {
				nodes = append(nodes, current)
				current = ""
			}
		} else {
			current += string(char)
		}
	}
	if current != "" {
		nodes = append(nodes, current)
	}
	return nodes
}
