package main

import (
	"flag"
	"fmt"
	"math/rand"
	"os"
	"time"
)

// QuantumState represents a quantum particle's state
type QuantumState struct {
	Name      string
	State     string // |0⟩, |1⟩, |+⟩, |-⟩
	IsEntangled bool
	Partner   *QuantumState
}

// QuantumSystem manages multiple entangled particles
type QuantumSystem struct {
	Particles []*QuantumState
	Verbose   bool
}

// NewQuantumSystem creates a new quantum system with n particles
func NewQuantumSystem(n int, verbose bool) *QuantumSystem {
	particles := make([]*QuantumState, n)
	for i := 0; i < n; i++ {
		particles[i] = &QuantumState{
			Name:        fmt.Sprintf("Particle %d", i+1),
			State:       generateRandomState(),
			IsEntangled: false,
			Partner:     nil,
		}
	}

	// Create some entanglements
	createEntanglements(particles)

	return &QuantumSystem{
		Particles: particles,
		Verbose:   verbose,
	}
}

// generateRandomState returns a random quantum state
func generateRandomState() string {
	states := []string{"|0⟩", "|1⟩", "|+⟩", "|-⟩"}
	return states[rand.Intn(len(states))]
}

// createEntanglements randomly entangles some particles
func createEntanglements(particles []*QuantumState) {
	rand.Seed(time.Now().UnixNano())
	maxEntanglements := len(particles) / 2
	entanglements := 0

	for i := 0; i < len(particles) && entanglements < maxEntanglements; i++ {
		if !particles[i].IsEntangled {
			// Find a partner
			for j := i + 1; j < len(particles); j++ {
				if !particles[j].IsEntangled {
					particles[i].IsEntangled = true
					particles[j].IsEntangled = true
					particles[i].Partner = particles[j]
					particles[j].Partner = particles[i]
					entanglements++
					break
				}
			}
		}
	}
}

// Run executes the quantum simulation
func (qs *QuantumSystem) Run() {
	qs.printHeader()
	qs.printParticles()
	qs.printEntanglementNetwork()
	qs.simulateMeasurement()
	qs.printFooter()
}

// printHeader prints the simulation header
func (qs *QuantumSystem) printHeader() {
	fmt.Println("=== Quantum Entanglement Simulation ===\n")
}

// printParticles displays all particles and their states
func (qs *QuantumSystem) printParticles() {
	if len(qs.Particles) == 2 {
		// Special case for two-particle system
		fmt.Printf("Particle A: %s\n", qs.Particles[0].State)
		fmt.Printf("Particle B: %s\n\n", qs.Particles[1].State)
	} else {
		// Multi-particle system
		fmt.Println("=== Multi-Particle Quantum System ===\n")
		for _, p := range qs.Particles {
			fmt.Printf("%s: %s\n", p.Name, p.State)
		}
		fmt.Println()
	}
}

// printEntanglementNetwork shows entanglement relationships
func (qs *QuantumSystem) printEntanglementNetwork() {
	if len(qs.Particles) > 2 {
		fmt.Println("Entanglement Network:")
		for i, p1 := range qs.Particles {
			for j := i + 1; j < len(qs.Particles); j++ {
				p2 := qs.Particles[j]
				status := "✗ Not Entangled"
				if p1.IsEntangled && p1.Partner == p2 {
					status = "✓ Entangled"
				}
				fmt.Printf("%s ↔ %s: %s\n", p1.Name, p2.Name, status)
			}
		}
		fmt.Println()
	} else {
		// Two-particle system
		status := "✗ NOT ENTANGLED"
		correlation := "No correlation"
		if qs.Particles[0].IsEntangled {
			status = "✓ ENTANGLED"
			correlation = "Perfect Anti-Correlation"
		}
		fmt.Printf("Entanglement Status: %s\n", status)
		fmt.Printf("Measurement Correlation: %s\n\n", correlation)
	}
}

// simulateMeasurement simulates measuring the quantum system
func (qs *QuantumSystem) simulateMeasurement() {
	if qs.Verbose {
		fmt.Println("=== Measurement Simulation ===")
	}

	// Measure each particle
	for _, p := range qs.Particles {
		if qs.Verbose {
			fmt.Printf("Measuring %s...\n", p.Name)
		}
		measureParticle(p)
	}

	if qs.Verbose {
		fmt.Println("\nMeasurement complete!")
	}
}

// measureParticle collapses a particle's state upon measurement
func measureParticle(p *QuantumState) {
	// If in superposition, collapse to definite state
	if p.State == "|+⟩" || p.State == "|-⟩" {
		rand.Seed(time.Now().UnixNano())
		if rand.Float32() < 0.5 {
			p.State = "|0⟩"
		} else {
			p.State = "|1⟩"
		}
	}
}

// printFooter displays educational information
func (qs *QuantumSystem) printFooter() {
	fmt.Println("=== Quantum Concepts Explained ===")
	fmt.Println("Superposition: Particles can exist in multiple states until measured.")
	fmt.Println("Entanglement: Connected particles affect each other instantly.")
	fmt.Println("Measurement: Causes quantum collapse to definite states.")
	fmt.Println()
	fmt.Println("Remember: This is a simplified educational tool!")
}

// printExplanation displays quantum physics concepts
func printExplanation() {
	fmt.Println("=== Quantum Physics Concepts ===\n")
	fmt.Println("1. SUPERPOSITION")
	fmt.Println("   A quantum particle can exist in multiple states simultaneously")
	fmt.Println("   until it is measured. Think of it as being in a 'maybe'")
	fmt.Println("   state until observed.")
	fmt.Println()
	fmt.Println("2. ENTANGLEMENT")
	fmt.Println("   When particles become entangled, they share a quantum")
	fmt.Println("   connection. Measuring one instantly determines the state")
	fmt.Println("   of its partner, no matter how far apart they are.")
	fmt.Println()
	fmt.Println("3. MEASUREMENT")
	fmt.Println("   Observing a quantum system causes it to 'collapse' from")
	fmt.Println("   superposition to a definite state. The act of looking")
	fmt.Println("   changes the reality!")
	fmt.Println()
	fmt.Println("4. QUANTUM STATES")
	fmt.Println("   |0⟩ and |1⟩: Definite states (like classical bits)")
	fmt.Println("   |+⟩ and |-⟩: Superposition states (quantum superposition)")
	fmt.Println()
	fmt.Println("This simulator helps visualize these abstract concepts!")
}

func main() {
	// Parse command line flags
	particles := flag.Int("particles", 2, "Number of particles in the system")
	verbose := flag.Bool("verbose", false, "Enable verbose output")
	explain := flag.Bool("explain", false, "Show quantum physics explanations")
	flag.Parse()

	// Show explanation if requested
	if *explain {
		printExplanation()
		return
	}

	// Validate particle count
	if *particles < 1 {
		fmt.Println("Error: Number of particles must be at least 1")
		os.Exit(1)
	}

	// Seed random number generator
	rand.Seed(time.Now().UnixNano())

	// Create and run quantum system
	system := NewQuantumSystem(*particles, *verbose)
	system.Run()
}
