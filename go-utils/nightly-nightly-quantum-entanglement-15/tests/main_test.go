package main

import (
	"math/cmplx"
	"testing"
)

func TestNewQuantumSystem(t *testing.T) {
	// Test system creation
	system := NewQuantumSystem(3)
	if len(system.Particles) != 3 {
		t.Errorf("Expected 3 particles, got %d", len(system.Particles))
	}
	if system.Entangled {
		t.Error("System should not be entangled initially")
	}
	if len(system.Operations) != 0 {
		t.Errorf("Expected 0 operations, got %d", len(system.Operations))
	}

	// Test initial state
	for i, particle := range system.Particles {
		if particle.IsMeasured {
			t.Errorf("Particle %d should not be measured initially", i)
		}
		if cmplx.Abs(particle.Amplitude0-1.0) > 1e-10 {
			t.Errorf("Particle %d amplitude0 should be 1.0, got %v", i, particle.Amplitude0)
		}
		if cmplx.Abs(particle.Amplitude1) > 1e-10 {
			t.Errorf("Particle %d amplitude1 should be 0.0, got %v", i, particle.Amplitude1)
		}
	}
}

func TestQuantumStateHadamard(t *testing.T) {
	particle := &QuantumState{
		Amplitude0: 1.0 + 0i,
		Amplitude1: 0.0 + 0i,
		IsMeasured: false,
	}

	particle.Hadamard()

	// After Hadamard, should be in superposition: (|0⟩ + |1⟩)/√2
	expected := complex(1/math.Sqrt(2), 0)
	if cmplx.Abs(particle.Amplitude0-expected) > 1e-10 {
		t.Errorf("Amplitude0 should be %v, got %v", expected, particle.Amplitude0)
	}
	if cmplx.Abs(particle.Amplitude1-expected) > 1e-10 {
		t.Errorf("Amplitude1 should be %v, got %v", expected, particle.Amplitude1)
	}
}

func TestQuantumStateHadamardOnMeasured(t *testing.T) {
	particle := &QuantumState{
		Amplitude0: 1.0 + 0i,
		Amplitude1: 0.0 + 0i,
		IsMeasured: true,
		Measurement: "0",
	}

	old0, old1 := particle.Amplitude0, particle.Amplitude1
	particle.Hadamard()

	// Should not change if already measured
	if particle.Amplitude0 != old0 || particle.Amplitude1 != old1 {
		t.Error("Hadamard should not change measured particle")
	}
}

func TestQuantumSystemCNOT(t *testing.T) {
	system := NewQuantumSystem(2)

	// Apply Hadamard to first particle to create superposition
	system.Particles[0].Hadamard()

	// Apply CNOT
	system.CNOT(0, 1)

	if !system.Entangled {
		t.Error("System should be entangled after CNOT")
	}
}

func TestQuantumStateMeasure(t *testing.T) {
	particle := &QuantumState{
		Amplitude0: complex(1/math.Sqrt(2), 0),
		Amplitude1: complex(1/math.Sqrt(2), 0),
		IsMeasured: false,
	}

	particle.Measure()

	if !particle.IsMeasured {
		t.Error("Particle should be measured after Measure()")
	}
	if particle.Measurement != "0" && particle.Measurement != "1" {
		t.Errorf("Measurement should be 0 or 1, got %s", particle.Measurement)
	}
}

func TestQuantumSystemVerifyEntanglement(t *testing.T) {
	// Test with unentangled system
	system := NewQuantumSystem(2)
	if system.VerifyEntanglement() {
		t.Error("Unentangled system should not pass entanglement verification")
	}

	// Test with entangled but unmeasured system
	system.Entangled = true
	if !system.VerifyEntanglement() {
		t.Error("Entangled unmeasured system should pass verification")
	}

	// Test with entangled and measured system
	for i := range system.Particles {
		system.Particles[i].Measure()
	}
	// Both should measure the same if properly entangled
	if system.Particles[0].Measurement == system.Particles[1].Measurement {
		if !system.VerifyEntanglement() {
			t.Error("Entangled measured system with same results should pass verification")
		}
	} else {
		if system.VerifyEntanglement() {
			t.Error("Entangled measured system with different results should fail verification")
		}
	}
}

func TestQuantumSystemGenerateRandomNumber(t *testing.T) {
	system := NewQuantumSystem(3)

	// Measure all particles
	for i := range system.Particles {
		system.Particles[i].Measure()
	}

	randNum := system.GenerateRandomNumber()

	if len(randNum) != 3 {
		t.Errorf("Random number should be 3 digits, got %d", len(randNum))
	}

	for _, char := range randNum {
		if char != '0' && char != '1' {
			t.Errorf("Random number should only contain 0 or 1, got %c", char)
		}
	}
}

func TestNormFunction(t *testing.T) {
	// Test norm of 1+0i should be 1
	result := norm(1.0 + 0i)
	if result != 1.0 {
		t.Errorf("Norm of 1+0i should be 1.0, got %f", result)
	}

	// Test norm of 0+1i should be 1
	result = norm(0.0 + 1i)
	if result != 1.0 {
		t.Errorf("Norm of 0+1i should be 1.0, got %f", result)
	}

	// Test norm of 1+1i should be 2
	result = norm(1.0 + 1i)
	if result != 2.0 {
		t.Errorf("Norm of 1+1i should be 2.0, got %f", result)
	}
}

func TestQuantumSystemSimulate(t *testing.T) {
	system := NewQuantumSystem(2)
	operations := []string{"hadamard", "cnot", "measure"}

	system.Simulate(operations)

	// Should have applied all operations
	if len(system.Operations) != 3 {
		t.Errorf("Expected 3 operations, got %d", len(system.Operations))
	}

	// All particles should be measured
	for i, particle := range system.Particles {
		if !particle.IsMeasured {
			t.Errorf("Particle %d should be measured", i)
		}
		if particle.Measurement != "0" && particle.Measurement != "1" {
			t.Errorf("Particle %d measurement should be 0 or 1, got %s", i, particle.Measurement)
		}
	}
}

func TestEdgeCases(t *testing.T) {
	// Test single particle system
	single := NewQuantumSystem(1)
	if len(single.Particles) != 1 {
		t.Error("Single particle system should have 1 particle")
	}

	// Test CNOT with insufficient particles
	single.CNOT(0, 1) // Should not panic
	if single.Entangled {
		t.Error("CNOT should not entangle with insufficient particles")
	}

	// Test operations on measured particles
	particle := &QuantumState{
		Amplitude0: 1.0 + 0i,
		Amplitude1: 0.0 + 0i,
		IsMeasured: true,
		Measurement: "0",
	}

	particle.Hadamard() // Should not change anything
	if particle.IsMeasured != true || particle.Measurement != "0" {
		t.Error("Measured particle should remain unchanged after Hadamard")
	}
}

func BenchmarkQuantumSystemCreation(b *testing.B) {
	for i := 0; i < b.N; i++ {
		NewQuantumSystem(8)
	}
}

func BenchmarkQuantumStateHadamard(b *testing.B) {
	particle := &QuantumState{
		Amplitude0: 1.0 + 0i,
		Amplitude1: 0.0 + 0i,
		IsMeasured: false,
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		particle.Hadamard()
	}
}

func BenchmarkQuantumSystemSimulate(b *testing.B) {
	system := NewQuantumSystem(4)
	operations := []string{"hadamard", "cnot", "measure"}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		system.Simulate(operations)
		// Reset for next iteration
		for j := range system.Particles {
			system.Particles[j] = QuantumState{
				Amplitude0: 1.0 + 0i,
				Amplitude1: 0.0 + 0i,
				IsMeasured: false,
				Measurement: "",
			}
		}
		system.Entangled = false
		system.Operations = []string{}
	}
}
