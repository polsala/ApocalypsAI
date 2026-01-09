package main

import (
	"flag"
	"fmt"
	"log"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"time"
)

// QuantumState represents a quantum particle's state
type QuantumState struct {
	Amplitude0 complex128
	Amplitude1 complex128
	IsMeasured  bool
	Measurement string
}

// QuantumSystem represents a collection of entangled particles
type QuantumSystem struct {
	Particles []QuantumState
	Entangled bool
	Operations []string
}

// NewQuantumSystem creates a new quantum system with specified particles
func NewQuantumSystem(particleCount int) *QuantumSystem {
	particles := make([]QuantumState, particleCount)
	for i := range particles {
		particles[i] = QuantumState{
			Amplitude0:  1.0 + 0i,
			Amplitude1:  0.0 + 0i,
			IsMeasured:  false,
			Measurement: "",
		}
	}

	return &QuantumSystem{
		Particles: particles,
		Entangled: false,
		Operations: []string{},
	}
}

// Hadamard applies Hadamard gate to create superposition
func (qs *QuantumState) Hadamard() {
	if qs.IsMeasured {
		return
	}
	// Hadamard matrix: H|0⟩ = (|0⟩ + |1⟩)/√2, H|1⟩ = (|0⟩ - |1⟩)/√2
	old0, old1 := qs.Amplitude0, qs.Amplitude1
	qs.Amplitude0 = (old0 + old1) / complex(math.Sqrt(2), 0)
	qs.Amplitude1 = (old0 - old1) / complex(math.Sqrt(2), 0)
}

// CNOT applies controlled-NOT gate for entanglement
func (qs *QuantumSystem) CNOT(control, target int) {
	if control >= len(qs.Particles) || target >= len(qs.Particles) {
		return
	}
	if qs.Particles[control].IsMeasured || qs.Particles[target].IsMeasured {
		return
	}
	// CNOT flips target if control is in |1⟩ state
	if imag(qs.Particles[control].Amplitude1) != 0 || real(qs.Particles[control].Amplitude1) != 0 {
		// Swap amplitudes for target particle
		qs.Particles[target].Amplitude0, qs.Particles[target].Amplitude1 = 
			qs.Particles[target].Amplitude1, qs.Particles[target].Amplitude0
	}
	qs.Entangled = true
}

// Measure collapses the quantum state
func (qs *QuantumState) Measure() {
	if qs.IsMeasured {
		return
	}
	// Calculate probabilities
	prob0 := norm(qs.Amplitude0)
	prob1 := norm(qs.Amplitude1)
	total := prob0 + prob1
	prob0 = prob0 / total

	// Random measurement
	r := rand.Float64()
	if r < prob0 {
		qs.Amplitude0 = 1.0 + 0i
		qs.Amplitude1 = 0.0 + 0i
		qs.Measurement = "0"
	} else {
		qs.Amplitude0 = 0.0 + 0i
		qs.Amplitude1 = 1.0 + 0i
		qs.Measurement = "1"
	}
	qs.IsMeasured = true
}

// norm calculates the squared magnitude of a complex number
func norm(c complex128) float64 {
	return real(c)*real(c) + imag(c)*imag(c)
}

// Visualize displays the quantum state as ASCII art
func (qs *QuantumSystem) Visualize() {
	fmt.Println("\n=== Quantum State Visualization ===")
	for i, particle := range qs.Particles {
		fmt.Printf("Particle %d: ", i)
		if particle.IsMeasured {
			fmt.Printf("| %s ⟩ (Measured)\n", particle.Measurement)
		} else {
			// Create ASCII representation of superposition
			prob0 := norm(particle.Amplitude0)
			prob1 := norm(particle.Amplitude1)
			total := prob0 + prob1
			prob0 = prob0 / total
			prob1 = prob1 / total

			bar0 := strings.Repeat("█", int(prob0*20))
			bar1 := strings.Repeat("░", int(prob1*20))
			fmt.Printf("| %s%s ⟩ (Superposition)\n", bar0, bar1)
			fmt.Printf("           Prob(0): %.2f  Prob(1): %.2f\n", prob0, prob1)
		}
	}
	if qs.Entangled {
		fmt.Println("\n🔗 Particles are entangled!")
	} else {
		fmt.Println("\n⚪ Particles are independent.")
	}
}

// Simulate runs quantum operations
func (qs *QuantumSystem) Simulate(operations []string) {
	for _, op := range operations {
		switch op {
		case "hadamard":
			for i := range qs.Particles {
				qs.Particles[i].Hadamard()
			}
		case "cnot":
			if len(qs.Particles) > 1 {
				qs.CNOT(0, 1)
			}
		case "measure":
			for i := range qs.Particles {
				qs.Particles[i].Measure()
			}
		case "phase":
			for i := range qs.Particles {
				if !qs.Particles[i].IsMeasured {
					// Apply phase shift
					qs.Particles[i].Amplitude1 *= complex(0, 1)
				}
			}
		case "swap":
			if len(qs.Particles) > 1 {
				qs.Particles[0].Amplitude0, qs.Particles[1].Amplitude0 = 
					qs.Particles[1].Amplitude0, qs.Particles[0].Amplitude0
				qs.Particles[0].Amplitude1, qs.Particles[1].Amplitude1 = 
					qs.Particles[1].Amplitude1, qs.Particles[0].Amplitude1
			}
		}
		qs.Operations = append(qs.Operations, op)
	}
}

// VerifyEntanglement checks if particles are properly entangled
func (qs *QuantumSystem) VerifyEntanglement() bool {
	if len(qs.Particles) < 2 {
		return false
	}
	if !qs.Entangled {
		return false
	}
	// For proper entanglement, measurements should be correlated
	if qs.Particles[0].IsMeasured && qs.Particles[1].IsMeasured {
		return qs.Particles[0].Measurement == qs.Particles[1].Measurement
	}
	return true
}

// GenerateRandomNumber creates a quantum random number
func (qs *QuantumSystem) GenerateRandomNumber() string {
	var result strings.Builder
	for i := range qs.Particles {
		qs.Particles[i].Measure()
		result.WriteString(qs.Particles[i].Measurement)
	}
	return result.String()
}

// InteractiveMode provides command-line interface
func InteractiveMode() {
	fmt.Println("\n🎮 Welcome to Quantum Entanglement Simulator!")
	fmt.Println("Commands: hadamard, cnot, measure, phase, swap, visualize, exit")

	system := NewQuantumSystem(2)
	scanner := bufio.NewScanner(os.Stdin)

	for {
		fmt.Print("\n> ")
		if !scanner.Scan() {
			break
		}
		input := strings.TrimSpace(scanner.Text())
		if input == "exit" {
			break
		}

		switch input {
		case "hadamard":
			system.Simulate([]string{"hadamard"})
			fmt.Println("Applied Hadamard gate (created superposition)")
		case "cnot":
			system.Simulate([]string{"cnot"})
			fmt.Println("Applied CNOT gate (created entanglement)")
		case "measure":
			system.Simulate([]string{"measure"})
			fmt.Println("Measured quantum states")
		case "phase":
			system.Simulate([]string{"phase"})
			fmt.Println("Applied phase shift")
		case "swap":
			system.Simulate([]string{"swap"})
			fmt.Println("Swapped quantum states")
		case "visualize":
			system.Visualize()
		case "verify":
			if system.VerifyEntanglement() {
				fmt.Println("✅ Entanglement verified!")
			} else {
				fmt.Println("❌ Entanglement failed!")
			}
		default:
			fmt.Println("Unknown command. Try: hadamard, cnot, measure, phase, swap, visualize, verify, exit")
		}
	}
}

func main() {
	// Command line flags
	particles := flag.Int("particles", 2, "Number of quantum particles (1-16)")
	duration := flag.Duration("duration", 5*time.Second, "Simulation duration")
	operations := flag.String("operations", "hadamard,cnot,measure", "Comma-separated quantum operations")
	visualize := flag.Bool("visualize", false, "Enable visualization")
	entangled := flag.Bool("entangled", false, "Start with entangled particles")
	interactive := flag.Bool("interactive", false, "Run in interactive mode")
	analyze := flag.Bool("analyze", false, "Run performance analysis")
	iterations := flag.Int("iterations", 100, "Number of iterations for analysis")

	flag.Parse()

	// Validate particle count
	if *particles < 1 || *particles > 16 {
		log.Fatal("Particle count must be between 1 and 16")
	}

	// Interactive mode
	if *interactive {
		InteractiveMode()
		return
	}

	// Performance analysis
	if *analyze {
		fmt.Printf("\n📊 Performance Analysis: %d particles, %d iterations\n", *particles, *iterations)
		start := time.Now()
		for i := 0; i < *iterations; i++ {
			system := NewQuantumSystem(*particles)
			ops := strings.Split(*operations, ",")
			system.Simulate(ops)
		}
		duration := time.Since(start)
		fmt.Printf("Total time: %v\n", duration)
		fmt.Printf("Average per iteration: %v\n", duration/time.Duration(*iterations))
		fmt.Printf("Operations per second: %.0f\n", float64(*iterations)/duration.Seconds())
		return
	}

	// Normal simulation
	fmt.Printf("\n🔬 Quantum Entanglement Simulator\n")
	fmt.Printf("Particles: %d\n", *particles)
	fmt.Printf("Operations: %s\n", *operations)
	fmt.Printf("Duration: %v\n", *duration)

	system := NewQuantumSystem(*particles)
	if *entangled {
		system.Entangled = true
	}

	ops := strings.Split(*operations, ",")
	start := time.Now()

	for time.Since(start) < *duration {
		system.Simulate(ops)
		if *visualize {
			system.Visualize()
		}
		time.Sleep(500 * time.Millisecond)
	}

	// Final measurement and results
	for i := range system.Particles {
		system.Particles[i].Measure()
	}

	fmt.Println("\n=== Final Results ===")
	for i, particle := range system.Particles {
		fmt.Printf("Particle %d: | %s ⟩\n", i, particle.Measurement)
	}

	if system.VerifyEntanglement() {
		fmt.Println("\n✅ Entanglement verified!")
	} else {
		fmt.Println("\n⚪ No entanglement detected.")
	}

	randNum := system.GenerateRandomNumber()
	fmt.Printf("\n🎲 Quantum Random Number: %s\n", randNum)
}
