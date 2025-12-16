package main

import (
	"flag"
	"fmt"
	"math/rand"
	"os"
	"time"

	"github.com/fatih/color"
)

// Particle represents a quantum particle with spin state
type Particle struct {
	ID    int
	Spin  string
	Paired bool
}

// EntanglementResult represents the result of entanglement verification
type EntanglementResult struct {
	PairID    int
	Success   bool
	Message   string
	Timestamp time.Time
}

// QuantumEntanglementChecker manages the verification process
type QuantumEntanglementChecker struct {
	particles    []Particle
	pairs        map[int][]Particle
	resultChan   chan EntanglementResult
	timeout      time.Duration
	verbose      bool
	red          *color.Color
	green        *color.Color
	yellow       *color.Color
	blue         *color.Color
}

// NewQuantumEntanglementChecker creates a new checker instance
func NewQuantumEntanglementChecker(particleCount int, timeoutSeconds int, verbose bool) *QuantumEntanglementChecker {
	return &QuantumEntanglementChecker{
		particles:  make([]Particle, 0, particleCount*2),
		pairs:      make(map[int][]Particle),
		resultChan: make(chan EntanglementResult, particleCount),
		timeout:    time.Duration(timeoutSeconds) * time.Second,
		verbose:    verbose,
		red:        color.New(color.FgRed),
		green:      color.New(color.FgGreen),
		yellow:     color.New(color.FgYellow),
		blue:       color.New(color.FgBlue),
	}
}

// GenerateParticles creates entangled particle pairs
func (q *QuantumEntanglementChecker) GenerateParticles() {
	q.blue.Println("🔬 Initializing Quantum Entanglement Checker...")
	fmt.Println()

	q.yellow.Printf("Creating %d entangled particle pairs...\n", len(q.pairs))
	fmt.Println()

	for i := 0; i < cap(q.particles)/2; i++ {
		pairID := i + 1
		rand.Seed(time.Now().UnixNano())
		
		// Create entangled pair (opposite spins)
		spin1 := "↑"
		if rand.Float32() < 0.5 {
			spin1 = "↓"
		}
		spin2 := "↓"
		if spin1 == "↓" {
			spin2 = "↑"
		}
		
		p1 := Particle{ID: i*2 + 1, Spin: spin1, Paired: true}
		p2 := Particle{ID: i*2 + 2, Spin: spin2, Paired: true}
		
		q.particles = append(q.particles, p1, p2)
		q.pairs[pairID] = []Particle{p1, p2}
		
		if q.verbose {
			fmt.Printf("  Pair %d: Particle %d (%s) ↔ Particle %d (%s)\n",
				pairID, p1.ID, p1.Spin, p2.ID, p2.Spin)
		}
	}
	fmt.Println()
}

// VerifyEntanglement verifies entanglement using concurrent goroutines
func (q *QuantumEntanglementChecker) VerifyEntanglement() {
	q.yellow.Println("📡 Verifying entanglement states...")
	fmt.Println()
	
	startTime := time.Now()
	
	// Launch verification goroutines for each pair
	for pairID, particles := range q.pairs {
		go q.verifyPair(pairID, particles)
	}
	
	// Collect results with timeout
	verifiedPairs := 0
	successCount := 0
	
	for {
		select {
		case result := <-q.resultChan:
			verifiedPairs++
			
			if result.Success {
				successCount++
				q.green.Printf("Particle Pair %d: ✓ Entangled\n", result.PairID)
			} else {
				q.red.Printf("Particle Pair %d: ✗ Not Entangled - %s\n", result.PairID, result.Message)
			}
			
			if verifiedPairs == len(q.pairs) {
				elapsed := time.Since(startTime)
				fmt.Println()
				if successCount == len(q.pairs) {
					q.green.Printf("🎉 All %d particle pairs verified successfully!\n", successCount)
				} else {
					q.yellow.Printf("⚠️  %d/%d particle pairs verified successfully\n", successCount, len(q.pairs))
				}
				fmt.Printf("\nEntanglement verification complete in %.1fs\n", elapsed.Seconds())
				return
			}
			
		case <-time.After(q.timeout):
			q.red.Println("⏰ Verification timeout! Some particles may have decohered.")
			fmt.Printf("\nVerified %d/%d particle pairs before timeout\n", verifiedPairs, len(q.pairs))
			return
		}
	}
}

// verifyPair checks if a particle pair is properly entangled
func (q *QuantumEntanglementChecker) verifyPair(pairID int, particles []Particle) {
	rand.Seed(time.Now().UnixNano())
	
	// Simulate quantum measurement
	measurementDelay := time.Duration(rand.Intn(500)+100) * time.Millisecond
	time.Sleep(measurementDelay)
	
	if len(particles) != 2 {
		q.resultChan <- EntanglementResult{
			PairID:    pairID,
			Success:   false,
			Message:   "Invalid pair size",
			Timestamp: time.Now(),
		}
		return
	}
	
	p1, p2 := particles[0], particles[1]
	
	// Check if spins are opposite (entangled)
	if (p1.Spin == "↑" && p2.Spin == "↓") || (p1.Spin == "↓" && p2.Spin == "↑") {
		q.resultChan <- EntanglementResult{
			PairID:    pairID,
			Success:   true,
			Message:   "Perfect anti-correlation detected",
			Timestamp: time.Now(),
		}
	} else {
		q.resultChan <- EntanglementResult{
			PairID:    pairID,
			Success:   false,
			Message:   "Spins not properly correlated",
			Timestamp: time.Now(),
		}
	}
}

// PrintASCIIArt displays quantum-themed ASCII art
func (q *QuantumEntanglementChecker) PrintASCIIArt() {
	q.blue.Println("  ⚛️  Quantum Entanglement Visualization  ⚛️")
	fmt.Println()
	q.yellow.Println("    Particle 1         Particle 2")
	q.green.Println("      (↑)     ↔     (↓)")
	q.green.Println("      (↓)     ↔     (↑)")
	q.yellow.Println("    Entangled States")
	fmt.Println()
}

func main() {
	// Parse command line flags
	particleCount := flag.Int("particles", 50, "Number of particle pairs to simulate")
	timeoutSeconds := flag.Int("timeout", 3, "Verification timeout in seconds")
	verbose := flag.Bool("verbose", false, "Enable verbose output")
	helpFlag := flag.Bool("help", false, "Show help")
	
	flag.Parse()
	
	if *helpFlag {
		fmt.Println("Quantum Entanglement Checker")
		fmt.Println()
		fmt.Println("Usage:")
		flag.PrintDefaults()
		return
	}
	
	if *particleCount <= 0 {
		fmt.Fprintln(os.Stderr, "Error: particles must be a positive integer")
		os.Exit(1)
	}
	
	if *timeoutSeconds <= 0 {
		fmt.Fprintln(os.Stderr, "Error: timeout must be a positive integer")
		os.Exit(1)
	}
	
	// Create checker instance
	checker := NewQuantumEntanglementChecker(*particleCount, *timeoutSeconds, *verbose)
	
	// Generate particles
	checker.GenerateParticles()
	
	// Print ASCII art
	checker.PrintASCIIArt()
	
	// Verify entanglement
	checker.VerifyEntanglement()
}
