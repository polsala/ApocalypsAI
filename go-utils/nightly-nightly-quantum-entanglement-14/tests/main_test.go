package main

import (
	"testing"
	"time"
)

// TestQuantumSimulator_GenerateParticles tests particle generation
func TestQuantumSimulator_GenerateParticles(t *testing.T) {
	// Create simulator with fixed seed for deterministic tests
	simulator := &QuantumSimulator{
		particles:    make([]Particle, 0),
		pairs:        make([]EntanglementPair, 0),
		measurements: make(map[int]string),
		rand:         NewDeterministicRand(),
	}

	// Test generating particles
	particleCount := 4
	simulator.GenerateParticles(particleCount)

	if len(simulator.particles) != particleCount {
		t.Errorf("Expected %d particles, got %d", particleCount, len(simulator.particles))
	}

	// Verify all particles have valid spins
	for _, particle := range simulator.particles {
		if particle.Spin != "↑" && particle.Spin != "↓" {
			t.Errorf("Invalid spin for particle %d: %s", particle.ID, particle.Spin)
		}
	}
}

// TestQuantumSimulator_CreateEntanglementPairs tests entanglement pairing
func TestQuantumSimulator_CreateEntanglementPairs(t *testing.T) {
	simulator := &QuantumSimulator{
		particles:    make([]Particle, 0),
		pairs:        make([]EntanglementPair, 0),
		measurements: make(map[int]string),
		rand:         NewDeterministicRand(),
	}

	// Generate test particles
	simulator.GenerateParticles(6)
	simulator.CreateEntanglementPairs()

	// Should create 3 pairs from 6 particles
	expectedPairs := 3
	if len(simulator.pairs) != expectedPairs {
		t.Errorf("Expected %d pairs, got %d", expectedPairs, len(simulator.pairs))
	}

	// Verify all pairs are correlated (opposite spins)
	for i, pair := range simulator.pairs {
		if !pair.Correlated {
			t.Errorf("Pair %d should be correlated", i)
		}
		if pair.Particle1.Spin == pair.Particle2.Spin {
			t.Errorf("Pair %d particles have same spin: %s and %s", i, pair.Particle1.Spin, pair.Particle2.Spin)
		}
	}
}

// TestQuantumSimulator_OddParticleCount handles odd particle counts
func TestQuantumSimulator_OddParticleCount(t *testing.T) {
	simulator := &QuantumSimulator{
		particles:    make([]Particle, 0),
		pairs:        make([]EntanglementPair, 0),
		measurements: make(map[int]string),
		rand:         NewDeterministicRand(),
	}

	// Generate odd number of particles
	simulator.GenerateParticles(5)
	simulator.CreateEntanglementPairs()

	// Should create 2 pairs from 4 particles (ignoring the odd one out)
	expectedPairs := 2
	if len(simulator.pairs) != expectedPairs {
		t.Errorf("Expected %d pairs, got %d", expectedPairs, len(simulator.pairs))
	}
}

// TestQuantumSimulator_CalculateCorrelation tests correlation calculation
func TestQuantumSimulator_CalculateCorrelation(t *testing.T) {
	simulator := &QuantumSimulator{
		particles:    make([]Particle, 0),
		pairs:        make([]EntanglementPair, 0),
		measurements: make(map[int]string),
		rand:         NewDeterministicRand(),
	}

	// Test with no pairs
	correlation := simulator.CalculateCorrelation()
	if correlation != 0.0 {
		t.Errorf("Expected 0.0 correlation with no pairs, got %f", correlation)
	}

	// Create test pairs
	pair1 := EntanglementPair{
		Particle1:  Particle{ID: 1, Spin: "↑"},
		Particle2:  Particle{ID: 2, Spin: "↓"},
		Correlated: true,
	}
	pair2 := EntanglementPair{
		Particle1:  Particle{ID: 3, Spin: "↓"},
		Particle2:  Particle{ID: 4, Spin: "↑"},
		Correlated: true,
	}
	simulator.pairs = []EntanglementPair{pair1, pair2}

	// Should have 100% correlation
	correlation = simulator.CalculateCorrelation()
	if correlation != 100.0 {
		t.Errorf("Expected 100.0 correlation, got %f", correlation)
	}

	// Break correlation in one pair
	pair2.Correlated = false
	correlation = simulator.CalculateCorrelation()
	if correlation != 50.0 {
		t.Errorf("Expected 50.0 correlation, got %f", correlation)
	}
}

// TestQuantumSimulator_MeasureEntanglement tests concurrent measurement
func TestQuantumSimulator_MeasureEntanglement(t *testing.T) {
	simulator := &QuantumSimulator{
		particles:    make([]Particle, 0),
		pairs:        make([]EntanglementPair, 0),
		measurements: make(map[int]string),
		rand:         NewDeterministicRand(),
	}

	// Generate and pair particles
	simulator.GenerateParticles(4)
	simulator.CreateEntanglementPairs()

	// Measure entanglement
	simulator.MeasureEntanglement(false)

	// Verify all particles were measured
	totalParticles := len(simulator.particles)
	if len(simulator.measurements) != totalParticles {
		t.Errorf("Expected %d measurements, got %d", totalParticles, len(simulator.measurements))
	}

	// Verify measurements match particle spins
	for _, particle := range simulator.particles {
		measuredSpin, exists := simulator.measurements[particle.ID]
		if !exists {
			t.Errorf("Particle %d was not measured", particle.ID)
		} else if measuredSpin != particle.Spin {
			t.Errorf("Measurement mismatch for particle %d: expected %s, got %s", 
				particle.ID, particle.Spin, measuredSpin)
		}
	}
}

// TestQuantumSimulator_EndToEnd tests complete simulation workflow
func TestQuantumSimulator_EndToEnd(t *testing.T) {
	simulator := NewQuantumSimulator()

	// Use deterministic random for testing
	simulator.rand = NewDeterministicRand()

	// Generate particles
	particleCount := 8
	simulator.GenerateParticles(particleCount)

	// Verify particle generation
	if len(simulator.particles) != particleCount {
		t.Errorf("Expected %d particles, got %d", particleCount, len(simulator.particles))
	}

	// Create entanglement pairs
	simulator.CreateEntanglementPairs()

	// Should have 4 pairs
	expectedPairs := 4
	if len(simulator.pairs) != expectedPairs {
		t.Errorf("Expected %d pairs, got %d", expectedPairs, len(simulator.pairs))
	}

	// Measure entanglement
	simulator.MeasureEntanglement(false)

	// Calculate correlation
	correlation := simulator.CalculateCorrelation()
	if correlation != 100.0 {
		t.Errorf("Expected 100.0%% correlation, got %f%%", correlation)
	}
}

// DeterministicRand provides deterministic random behavior for testing
func NewDeterministicRand() *rand.Rand {
	// Use a fixed seed for deterministic behavior
	return rand.New(rand.NewSource(42))
}

// BenchmarkQuantumSimulator_MeasureEntanglement benchmarks concurrent measurement
func BenchmarkQuantumSimulator_MeasureEntanglement(b *testing.B) {
	simulator := &QuantumSimulator{
		particles:    make([]Particle, 0),
		pairs:        make([]EntanglementPair, 0),
		measurements: make(map[int]string),
		rand:         NewDeterministicRand(),
	}

	// Generate large number of particles for benchmarking
	particleCount := 1000
	simulator.GenerateParticles(particleCount)
	simulator.CreateEntanglementPairs()

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		// Reset measurements for each iteration
		simulator.measurements = make(map[int]string)
		simulator.MeasureEntanglement(false)
	}
}

// TestQuantumSimulator_ConcurrentSafety tests thread safety
func TestQuantumSimulator_ConcurrentSafety(t *testing.T) {
	simulator := &QuantumSimulator{
		particles:    make([]Particle, 0),
		pairs:        make([]EntanglementPair, 0),
		measurements: make(map[int]string),
		rand:         NewDeterministicRand(),
	}

	// Generate particles
	simulator.GenerateParticles(100)
	simulator.CreateEntanglementPairs()

	// Run multiple concurrent measurement operations
	var wg sync.WaitGroup
	concurrentOps := 10

	for i := 0; i < concurrentOps; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			simulator.MeasureEntanglement(false)
		}()
	}

	wg.Wait()

	// Verify final state is consistent
	totalParticles := len(simulator.particles)
	if len(simulator.measurements) != totalParticles {
		t.Errorf("Expected %d measurements, got %d", totalParticles, len(simulator.measurements))
	}
}

// Mock rationale: All tests use deterministic random number generation
// to ensure reproducible results. The NewDeterministicRand() function
// provides a fixed seed (42) for consistent test behavior across runs.
// Tests cover particle generation, entanglement pairing, correlation
// calculation, concurrent measurement, and thread safety scenarios.
