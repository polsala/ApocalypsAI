package main

import (
	"flag"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

// Particle represents a quantum particle with spin state
type Particle struct {
	ID   int
	Spin string // "↑" (up) or "↓" (down)
}

// EntanglementPair represents two entangled particles
type EntanglementPair struct {
	Particle1 Particle
	Particle2 Particle
	Correlated bool
}

// QuantumSimulator manages the entanglement simulation
type QuantumSimulator struct {
	particles    []Particle
	pairs        []EntanglementPair
	measurements map[int]string
	mu           sync.RWMutex
	rand         *rand.Rand
}

// NewQuantumSimulator creates a new quantum simulator
func NewQuantumSimulator() *QuantumSimulator {
	return &QuantumSimulator{
		particles:    make([]Particle, 0),
		pairs:        make([]EntanglementPair, 0),
		measurements: make(map[int]string),
		rand:         rand.New(rand.NewSource(time.Now().UnixNano())),
	}
}

// GenerateParticles creates a specified number of quantum particles
func (qs *QuantumSimulator) GenerateParticles(count int) {
	for i := 0; i < count; i++ {
		spin := "↑"
		if qs.rand.Intn(2) == 1 {
			spin = "↓"
		}
		qs.particles = append(qs.particles, Particle{
			ID:   i + 1,
			Spin: spin,
		})
	}
}

// CreateEntanglementPairs creates entangled pairs from generated particles
func (qs *QuantumSimulator) CreateEntanglementPairs() {
	particleCount := len(qs.particles)
	// Ensure even number of particles for pairing
	if particleCount%2 != 0 {
		particleCount--
	}

	for i := 0; i < particleCount; i += 2 {
		p1 := qs.particles[i]
		p2 := qs.particles[i+1]

		// Create entangled pair (opposite spins)
		entangledPair := EntanglementPair{
			Particle1:  p1,
			Particle2:  p2,
			Correlated: true,
		}

		// Randomly flip one particle to ensure opposite spins
		if p1.Spin == p2.Spin {
			if p1.Spin == "↑" {
				entangledPair.Particle2.Spin = "↓"
			} else {
				entangledPair.Particle1.Spin = "↑"
			}
		}

		qs.pairs = append(qs.pairs, entangledPair)
	}
}

// MeasureEntanglement concurrently measures all entangled pairs
func (qs *QuantumSimulator) MeasureEntanglement(verbose bool) {
	var wg sync.WaitGroup
	measurementChan := make(chan EntanglementPair, len(qs.pairs))

	// Measure each entangled pair concurrently
	for _, pair := range qs.pairs {
		wg.Add(1)
		go func(p EntanglementPair) {
			defer wg.Done()
			qs.measurePair(p, measurementChan, verbose)
		}(pair)
	}

	// Wait for all measurements to complete
	wg.Wait()
	close(measurementChan)

	// Collect results
	for pair := range measurementChan {
		qs.mu.Lock()
		qs.measurements[pair.Particle1.ID] = pair.Particle1.Spin
		qs.measurements[pair.Particle2.ID] = pair.Particle2.Spin
		qs.mu.Unlock()

		if verbose {
			fmt.Printf("Particle %d (spin: %s) entangled with Particle %d (spin: %s)\n",
				pair.Particle1.ID, pair.Particle1.Spin,
				pair.Particle2.ID, pair.Particle2.Spin)
		}
	}
}

// measurePair measures a single entangled pair
func (qs *QuantumSimulator) measurePair(pair EntanglementPair, resultChan chan<- EntanglementPair, verbose bool) {
	// Simulate measurement delay
	delay := time.Duration(qs.rand.Intn(10)) * time.Millisecond
	time.Sleep(delay)

	// Verify entanglement correlation
	if pair.Particle1.Spin == pair.Particle2.Spin {
		pair.Correlated = false
		if verbose {
			fmt.Printf("⚠️  Warning: Particle %d and %d have same spin - entanglement broken!\n",
				pair.Particle1.ID, pair.Particle2.ID)
		}
	}

	resultChan <- pair
}

// CalculateCorrelation calculates the entanglement correlation percentage
func (qs *QuantumSimulator) CalculateCorrelation() float64 {
	if len(qs.pairs) == 0 {
		return 0.0
	}

	correlatedPairs := 0
	for _, pair := range qs.pairs {
		if pair.Correlated {
			correlatedPairs++
		}
	}

	return float64(correlatedPairs) / float64(len(qs.pairs)) * 100.0
}

// PrintResults displays the simulation results
func (qs *QuantumSimulator) PrintResults() {
	correlation := qs.CalculateCorrelation()

	fmt.Println("\n✅ Quantum entanglement verification complete!")
	fmt.Printf("📊 Entangled pairs: %d\n", len(qs.pairs))
	fmt.Printf("⚡ Total particles: %d\n", len(qs.particles))
	fmt.Printf("🔬 Measurement correlation: %.2f%%\n", correlation)
}

func main() {
	// Parse command line flags
	particleCount := flag.Int("particles", 10, "number of quantum particles to generate")
	verbose := flag.Bool("verbose", false, "enable verbose output")
	flag.Parse()

	// Validate input
	if *particleCount <= 0 {
		fmt.Println("Error: particle count must be positive")
		return
	}

	// Initialize simulator
	simulator := NewQuantumSimulator()

	fmt.Println("🔬 Initializing quantum entanglement verification...")
	fmt.Printf("Generating %d quantum particles...\n", *particleCount)

	// Generate particles
	simulator.GenerateParticles(*particleCount)

	// Create entanglement pairs
	simulator.CreateEntanglementPairs()

	// Measure entanglement
	simulator.MeasureEntanglement(*verbose)

	// Print results
	simulator.PrintResults()
}
