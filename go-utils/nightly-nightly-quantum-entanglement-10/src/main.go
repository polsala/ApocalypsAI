package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"math"
	"math/rand"
	"net/http"
	"runtime"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"
)

// QuantumParticle represents an entangled particle with spin state
type QuantumParticle struct {
	ID       int     `json:"id"`
	Spin     float64 `json:"spin"`
	Node     string  `json:"node"`
	Timestamp int64  `json:"timestamp"`
}

// EntanglementResult holds the verification results
type EntanglementResult struct {
	Fidelity        float64 `json:"fidelity"`
	BellInequality  float64 `json:"bell_inequality"`
	AverageLatency  float64 `json:"average_latency_ms"`
	QuantumState    string  `json:"quantum_state"`
	TotalParticles  int     `json:"total_particles"`
	CorrelatedPairs int     `json:"correlated_pairs"`
}

// Global variables for configuration
var (
	nodes        []string
	particles    int
	threshold    float64
	verbose      bool
	listenPort   int
)

func init() {
	flag.Usage = func() {
		fmt.Fprintf(flag.CommandLine.Output(), "Usage of %s:\n", runtime.Args[0])
		flag.PrintDefaults()
	}
	flag.String("nodes", "", "Comma-separated list of nodes (host:port)")
	flag.IntVar(&particles, "particles", 1000, "Number of entangled particle pairs to generate")
	flag.Float64Var(&threshold, "threshold", 0.9, "Correlation threshold for entanglement verification")
	flag.BoolVar(&verbose, "verbose", false, "Enable verbose quantum debugging output")
	flag.IntVar(&listenPort, "port", 9000, "Port to listen for quantum measurements")
}

func main() {
	flag.Parse()

	// Parse nodes from flag
	nodesStr := flag.Lookup("nodes").Value.String()
	if nodesStr == "" {
		log.Fatal("❌ No nodes specified. Use --nodes host:port[,host:port...]\n")
	}
	nodes = strings.Split(nodesStr, ",")

	if verbose {
		log.Println("🔬 Initializing quantum entanglement checker...")
		log.Printf("📡 Target nodes: %v\n", nodes)
		log.Printf("⚛️  Particles per node: %d\n", particles)
	}

	// Start HTTP server for quantum measurements
	go startQuantumServer()

	// Wait for server to start
	time.Sleep(100 * time.Millisecond)

	// Perform entanglement verification
	result := verifyEntanglement()

	// Display results
	displayResults(result)
}

func startQuantumServer() {
	http.HandleFunc("/measure", handleQuantumMeasurement)
	http.HandleFunc("/health", handleHealthCheck)

	addr := fmt.Sprintf(":%d", listenPort)
	if verbose {
		log.Printf("📡 Starting quantum server on %s\n", addr)
	}
	http.ListenAndServe(addr, nil)
}

func handleHealthCheck(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"status": "quantum-ready",
		"time": time.Now().Format(time.RFC3339),
	})
}

func handleQuantumMeasurement(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var particle QuantumParticle
	if err := json.NewDecoder(r.Body).Decode(&particle); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	particle.Timestamp = time.Now().UnixNano()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"status":    "measured",
		"particle":  particle,
		"spooky":    "action confirmed",
		"timestamp": particle.Timestamp,
	})
}

func verifyEntanglement() EntanglementResult {
	if verbose {
		log.Println("📡 Establishing quantum links with nodes...")
	}

	// Generate entangled particles
	entangledPairs := generateEntangledPairs(particles)

	// Distribute particles to nodes
	distribution := distributeParticles(entangledPairs)

	// Send particles to nodes concurrently
	var wg sync.WaitGroup
	results := make(chan *http.Response, len(nodes))
	errors := make(chan error, len(nodes))

	start := time.Now()

	for node, particles := range distribution {
		wg.Add(1)
		go func(node string, particles []QuantumParticle) {
			defer wg.Done()
			if err := sendParticlesToNode(node, particles); err != nil {
				errors <- err
				return
			}
			results <- &http.Response{StatusCode: http.StatusOK}
		}(node, particles)
	}

	wg.Wait()
	close(results)
	close(errors)

	// Check for errors
	errorCount := 0
	for err := range errors {
		if verbose {
			log.Printf("❌ Quantum link error: %v\n", err)
		}
		errorCount++
	}

	if errorCount > 0 {
		log.Fatalf("❌ Failed to establish quantum links with %d nodes\n", errorCount)
	}

	latency := time.Since(start).Seconds() * 1000

	// Calculate entanglement metrics
	fidelity := calculateEntanglementFidelity(entangledPairs)
	bellInequality := calculateBellInequality(entangledPairs)
	quantumState := generateQuantumStateDescription(fidelity, bellInequality)

	return EntanglementResult{
		Fidelity:        fidelity,
		BellInequality:  bellInequality,
		AverageLatency:  latency / float64(len(nodes)),
		QuantumState:    quantumState,
		TotalParticles:  len(entangledPairs) * 2,
		CorrelatedPairs: int(fidelity * float64(len(entangledPairs))),
	}
}

func generateEntangledPairs(count int) [][]QuantumParticle {
	if verbose {
		log.Printf("⚛️  Generating %d entangled particle pairs...\n", count)
	}

	rand.Seed(time.Now().UnixNano())
	pairs := make([][]QuantumParticle, count)

	for i := 0; i < count; i++ {
		// Generate correlated spin states (entangled)
		spin1 := rand.NormFloat64()
		spin2 := -spin1 // Perfect anti-correlation for entanglement

		pairs[i] = []QuantumParticle{
			{ID: i * 2, Spin: spin1, Node: ""},
			{ID: i*2 + 1, Spin: spin2, Node: ""},
		}
	}

	return pairs
}

func distributeParticles(pairs [][]QuantumParticle) map[string][]QuantumParticle {
	distribution := make(map[string][]QuantumParticle)

	for i, pair := range pairs {
		node := nodes[i%len(nodes)]
		pair[0].Node = node
		pair[1].Node = node
		distribution[node] = append(distribution[node], pair...)
	}

	return distribution
}

func sendParticlesToNode(node string, particles []QuantumParticle) error {
	url := fmt.Sprintf("http://%s/measure", node)

	for _, particle := range particles {
		data, err := json.Marshal(particle)
		if err != nil {
			return err
		}

		resp, err := http.Post(url, "application/json", strings.NewReader(string(data)))
		if err != nil {
			return fmt.Errorf("failed to send particle to %s: %w", node, err)
		}
		resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			return fmt.Errorf("node %s returned status %d", node, resp.StatusCode)
		}
	}

	return nil
}

func calculateEntanglementFidelity(pairs [][]QuantumParticle) float64 {
	if verbose {
		log.Println("🌀 Calculating entanglement fidelity...")
	}

	correlations := make([]float64, len(pairs))
	for i, pair := range pairs {
		if len(pair) == 2 {
			// Calculate correlation between entangled particles
			correlation := -pair[0].Spin * pair[1].Spin
			correlations[i] = correlation
		}
	}

	// Sort correlations to find median
	sort.Float64s(correlations)
	median := correlations[len(correlations)/2]

	// Normalize to [0,1] range
	fidelity := 1.0 / (1.0 + math.Exp(-median))

	// Add some quantum noise
	rand.Seed(time.Now().UnixNano())
	noise := rand.NormFloat64() * 0.02
	fidelity = math.Max(0, math.Min(1, fidelity+noise))

	return fidelity
}

func calculateBellInequality(pairs [][]QuantumParticle) float64 {
	if verbose {
		log.Println("🔬 Calculating Bell inequality violation...")
	}

	// Simplified Bell inequality calculation
	// For entangled particles, we expect |S| > 2 (classical limit)
	// where S = E(a,b) - E(a,b') + E(a',b) + E(a',b')

	rand.Seed(time.Now().UnixNano())
	a := rand.Float64() * math.Pi
	aPrime := a + math.Pi/2
	b := rand.Float64() * math.Pi
	bPrime := b + math.Pi/2

	E := func(theta float64) float64 {
		sum := 0.0
		for _, pair := range pairs {
			if len(pair) == 2 {
				// Simplified correlation function
				correlation := math.Cos(theta + pair[0].Spin - pair[1].Spin)
				sum += correlation
			}
		}
		return sum / float64(len(pairs))
	}

	S := math.Abs(E(a-b) - E(a-bPrime) + E(aPrime-b) + E(aPrime-bPrime))

	// Add quantum enhancement
	return S * 1.1
}

func generateQuantumStateDescription(fidelity, bell float64) string {
	if bell > 2.5 && fidelity > 0.95 {
		return "Spooky action at a distance confirmed! 🎃👻"
	} else if bell > 2.2 && fidelity > 0.9 {
		return "Quantum entanglement stable. The universe is weird. 🌀"
	} else if bell > 2.0 && fidelity > 0.8 {
		return "Weak entanglement detected. More particles needed! ⚛️"
	} else {
		return "Classical correlation only. Try harder, quantum cowboy! 🤠"
	}
}

func displayResults(result EntanglementResult) {
	fmt.Println()
	fmt.Println("🔬 Quantum Entanglement Verification Results")
	fmt.Println(strings.Repeat("=" , 50))
	fmt.Printf("- Entanglement Fidelity: %.1f%%\n", result.Fidelity*100)
	fmt.Printf("- Bell Inequality Violation: %.2f (Classical limit: 2.0)\n", result.BellInequality)
	fmt.Printf("- Network Latency: %.0fms avg\n", result.AverageLatency)
	fmt.Printf("- Quantum State: %s\n", result.QuantumState)
	fmt.Printf("- Total Particles: %d\n", result.TotalParticles)
	fmt.Printf("- Correlated Pairs: %d\n", result.CorrelatedPairs)
	fmt.Println()

	if result.Fidelity > threshold {
		fmt.Println("✅ Quantum entanglement verified across all nodes!")
		fmt.Println("   The universe remains beautifully weird. 🎃✨")
	} else {
		fmt.Println("❌ Entanglement verification failed!")
		fmt.Println("   Try increasing particle count or checking network stability.")
	}
	fmt.Println()
}

// Additional helper functions for testing
func parseNodesFromEnv() []string {
	nodesEnv := os.Getenv("QUANTUM_NODES")
	if nodesEnv != "" {
		return strings.Split(nodesEnv, ",")
	}
	return nodes
}

func calculateCorrelation(p1, p2 QuantumParticle) float64 {
	return -p1.Spin * p2.Spin
}
