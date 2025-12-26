package main

import (
	"testing"
)

// TestNewQuantumSystem creates a system and validates basic properties
func TestNewQuantumSystem(t *testing.T) {
	system := NewQuantumSystem(4, false)

	// Check that we have the correct number of particles
	if len(system.Particles) != 4 {
		t.Errorf("Expected 4 particles, got %d", len(system.Particles))
	}

	// Check that all particles have names
	for i, p := range system.Particles {
		expectedName := fmt.Sprintf("Particle %d", i+1)
		if p.Name != expectedName {
			t.Errorf("Expected particle name '%s', got '%s'", expectedName, p.Name)
		}
	}
}

// TestGenerateRandomState validates state generation
func TestGenerateRandomState(t *testing.T) {
	validStates := []string{"|0⟩", "|1⟩", "|+⟩", "|-⟩"}

	// Generate many states to ensure we get valid ones
	for i := 0; i < 100; i++ {
		state := generateRandomState()
		valid := false
		for _, validState := range validStates {
			if state == validState {
				valid = true
				break
			}
		}
		if !valid {
			t.Errorf("Invalid state generated: %s", state)
		}
	}
}

// TestEntanglementCreation validates entanglement logic
func TestEntanglementCreation(t *testing.T) {
	particles := make([]*QuantumState, 4)
	for i := 0; i < 4; i++ {
		particles[i] = &QuantumState{
			Name:        fmt.Sprintf("Particle %d", i+1),
			State:       "|0⟩",
			IsEntangled: false,
			Partner:     nil,
		}
	}

	createEntanglements(particles)

	// Count entangled particles
	entangledCount := 0
	for _, p := range particles {
		if p.IsEntangled {
			entangledCount++
		}
	}

	// Should have exactly 2 entangled particles (1 pair)
	if entangledCount != 2 {
		t.Errorf("Expected 2 entangled particles, got %d", entangledCount)
	}

	// Check that entangled particles point to each other
	for _, p := range particles {
		if p.IsEntangled {
			if p.Partner == nil {
				t.Error("Entangled particle has no partner")
			} else if p.Partner.Partner != p {
				t.Error("Entanglement partnership is not bidirectional")
			}
		}
	}
}

// TestMeasurementCollapse validates state collapse
func TestMeasurementCollapse(t *testing.T) {
	// Test superposition collapse
	particle := &QuantumState{
		Name:        "Test Particle",
		State:       "|+⟩",
		IsEntangled: false,
		Partner:     nil,
	}

	// Measure the particle multiple times
	collapsedStates := make(map[string]int)
	for i := 0; i < 100; i++ {
		measureParticle(particle)
		collapsedStates[particle.State]++
		// Reset to superposition for next iteration
		particle.State = "|+⟩"
	}

	// Should have both |0⟩ and |1⟩ states (probabilistic)
	if collapsedStates["|0⟩"] == 0 || collapsedStates["|1⟩"] == 0 {
		t.Error("Measurement should produce both |0⟩ and |1⟩ states")
	}

	// Test that definite states don't change
	particle.State = "|0⟩"
	originalState := particle.State
	measureParticle(particle)
	if particle.State != originalState {
		t.Error("Definite state should not change upon measurement")
	}
}

// TestTwoParticleSystem validates two-particle entanglement
func TestTwoParticleSystem(t *testing.T) {
	system := NewQuantumSystem(2, false)

	// Should have exactly 2 particles
	if len(system.Particles) != 2 {
		t.Errorf("Expected 2 particles, got %d", len(system.Particles))
	}

	// In a 2-particle system, they should be entangled
	if !system.Particles[0].IsEntangled || !system.Particles[1].IsEntangled {
		t.Error("Two particles should be entangled")
	}

	// Partners should point to each other
	if system.Particles[0].Partner != system.Particles[1] || system.Particles[1].Partner != system.Particles[0] {
		t.Error("Two-particle entanglement should be bidirectional")
	}
}

// TestMultiParticleSystem validates multi-particle entanglement
func TestMultiParticleSystem(t *testing.T) {
	system := NewQuantumSystem(6, false)

	// Should have exactly 6 particles
	if len(system.Particles) != 6 {
		t.Errorf("Expected 6 particles, got %d", len(system.Particles))
	}

	// Should have at most 3 entangled pairs (6/2 = 3)
	entangledCount := 0
	for _, p := range system.Particles {
		if p.IsEntangled {
			entangledCount++
		}
	}

	if entangledCount > 6 {
		t.Errorf("Too many entangled particles: %d", entangledCount)
	}

	// Should be even number of entangled particles
	if entangledCount%2 != 0 {
		t.Errorf("Entangled particles should come in pairs, got %d", entangledCount)
	}
}

// BenchmarkQuantumSystemCreation benchmarks system creation
func BenchmarkQuantumSystemCreation(b *testing.B) {
	for i := 0; i < b.N; i++ {
		NewQuantumSystem(10, false)
	}
}

// BenchmarkMeasurement benchmarks particle measurement
func BenchmarkMeasurement(b *testing.B) {
	particle := &QuantumState{
		Name:        "Benchmark Particle",
		State:       "|+⟩",
		IsEntangled: false,
		Partner:     nil,
	}

	for i := 0; i < b.N; i++ {
		measureParticle(particle)
	}
}

// Example usage of the quantum simulator
func ExampleNewQuantumSystem() {
	system := NewQuantumSystem(2, false)
	system.Run()
	// Output: === Quantum Entanglement Simulation ===
	//
	// Particle A: |0⟩
	// Particle B: |1⟩
	//
	// Entanglement Status: ✓ ENTANGLED
	// Measurement Correlation: Perfect Anti-Correlation
	//
	// When Particle A is measured as 0, Particle B will be 1!
}

// Example of quantum explanation
func ExamplePrintExplanation() {
	printExplanation()
	// Output: === Quantum Physics Concepts ===
	//
	// 1. SUPERPOSITION
	//    A quantum particle can exist in multiple states simultaneously
	//    until it is measured. Think of it as being in a 'maybe'
	//    state until observed.
	//
	// 2. ENTANGLEMENT
	//    When particles become entangled, they share a quantum
	//    connection. Measuring one instantly determines the state
	//    of its partner, no matter how far apart they are.
	//
	// 3. MEASUREMENT
	//    Observing a quantum system causes it to 'collapse' from
	//    superposition to a definite state. The act of looking
	//    changes the reality!
	//
	// 4. QUANTUM STATES
	//    |0⟩ and |1⟩: Definite states (like classical bits)
	//    |+⟩ and |-⟩: Superposition states (quantum superposition)
	//
	// This simulator helps visualize these abstract concepts!
}
