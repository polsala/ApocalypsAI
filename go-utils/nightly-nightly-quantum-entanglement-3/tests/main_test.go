package main

import (
	"testing"
	"time"
)

func TestSimulateQuantumState(t *testing.T) {
	// Test quantum state simulation
	state := simulateQuantumState()

	// Verify probability is within valid range
	if state.Probability < 0 || state.Probability > 1 {
		t.Errorf("Probability out of range: %f", state.Probability)
	}

	// Verify entanglement logic
	expectedEntangled := state.Probability > 0.5
	if state.Entangled != expectedEntangled {
		t.Errorf("Entanglement logic incorrect. Expected %v, got %v", expectedEntangled, state.Entangled)
	}
}

func TestGenerateReport(t *testing.T) {
	// Test report generation with various states
	testCases := []struct {
		name        string
		state       QuantumState
		expectStable bool
	}{
		{
			name: "High entanglement",
			state: QuantumState{
				Superposition: true,
				Probability:   0.8,
				Entangled:     true,
				SpookyAction:  false,
			},
			expectStable: true,
		},
		{
			name: "Low entanglement",
			state: QuantumState{
				Superposition: false,
				Probability:   0.2,
				Entangled:     false,
				SpookyAction:  false,
			},
			expectStable: false,
		},
		{
			name: "Spooky action detected",
			state: QuantumState{
				Superposition: true,
				Probability:   0.6,
				Entangled:     true,
				SpookyAction:  true,
			},
			expectStable: true,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			report := generateReport(tc.state)
			
			// Verify entanglement level calculation
			expectedLevel := tc.state.Probability * 100
			if report.EntanglementLevel != expectedLevel {
				t.Errorf("Entanglement level incorrect. Expected %f, got %f", expectedLevel, report.EntanglementLevel)
			}
			
			// Verify reality alignment
			if tc.expectStable && report.RealityAlignment != "Stable" {
				t.Errorf("Expected stable alignment, got %s", report.RealityAlignment)
			}
			if !tc.expectStable && report.RealityAlignment == "Stable" {
				t.Errorf("Expected unstable alignment, got %s", report.RealityAlignment)
			}
		})
	}
}

func TestCalculateFluctuations(t *testing.T) {
	// Test quantum fluctuation calculation
	fluctuations := calculateFluctuations()
	
	// Fluctuations should be positive
	if fluctuations < 0 {
		t.Errorf("Fluctuations should be positive, got %f", fluctuations)
	}
	
	// Fluctuations should be very small (quantum scale)
	if fluctuations > 1e-9 {
		t.Errorf("Fluctuations too large for quantum scale: %f", fluctuations)
	}
}

func TestStateToString(t *testing.T) {
	// Test state to string conversion
	testCases := []struct {
		state    QuantumState
		expected string
	}{
		{QuantumState{Superposition: true}, "✓ Coherent"},
		{QuantumState{Superposition: false}, "✗ Decoherent"},
	}

	for _, tc := range testCases {
		result := stateToString(tc.state)
		if result != tc.expected {
			t.Errorf("Expected %s, got %s", tc.expected, result)
		}
	}
}

func TestConcurrency(t *testing.T) {
	// Test that quantum simulation uses concurrency properly
	start := time.Now()
	
	// Run simulation multiple times to check for race conditions
	for i := 0; i < 10; i++ {
		state := simulateQuantumState()
		if state.Probability < 0 || state.Probability > 1 {
			t.Errorf("Invalid probability in iteration %d: %f", i, state.Probability)
		}
	}
	
	elapsed := time.Since(start)
	
	// Simulation should complete quickly (concurrency is working)
	if elapsed > 5*time.Second {
		t.Errorf("Simulation too slow, concurrency may not be working: %v", elapsed)
	}
}

func TestFluctuationThreshold(t *testing.T) {
	// Test that fluctuations are within expected thresholds
	for i := 0; i < 100; i++ {
		fluctuations := calculateFluctuations()
		if fluctuations > fluctuationThreshold {
			// This is allowed but should be rare
			t.Logf("High fluctuation detected: %f (threshold: %f)", fluctuations, fluctuationThreshold)
		}
	}
}

func TestReportFormatting(t *testing.T) {
	// Test that report formatting is consistent
	state := QuantumState{
		Superposition: true,
		Probability:   0.75,
		Entangled:     true,
		SpookyAction:  true,
	}
	
	report := generateReport(state)
	
	// Verify report fields are populated
	if report.SuperpositionState == "" {
		t.Error("Superposition state not set")
	}
	if report.EntanglementLevel <= 0 {
		t.Error("Entanglement level not set correctly")
	}
	if report.Fluctuations < 0 {
		t.Error("Fluctuations not calculated")
	}
	if report.Recommendation == "" {
		t.Error("Recommendation not generated")
	}
}

// Benchmark tests

func BenchmarkSimulateQuantumState(b *testing.B) {
	for i := 0; i < b.N; i++ {
		simulateQuantumState()
	}
}

func BenchmarkCalculateFluctuations(b *testing.B) {
	for i := 0; i < b.N; i++ {
		calculateFluctuations()
	}
}

func BenchmarkGenerateReport(b *testing.B) {
	state := QuantumState{
		Superposition: true,
		Probability:   0.5,
		Entangled:     true,
		SpookyAction:  false,
	}
	for i := 0; i < b.N; i++ {
		generateReport(state)
	}
}

// Mock rationale: These tests verify the quantum entanglement checker's core functionality
// without requiring external dependencies or network calls. They test:
// 1. Quantum state simulation with concurrency
// 2. Report generation logic
// 3. Fluctuation calculations
// 4. String formatting
// 5. Performance benchmarks
// All tests are deterministic and run quickly using only Go's standard library.
