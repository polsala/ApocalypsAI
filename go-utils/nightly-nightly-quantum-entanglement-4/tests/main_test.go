package main

import (
	"testing"
	"time"
)

// MockQuantumState creates a mock quantum state for testing
func MockQuantumState(nodeID string, spin, phase, fidelity float64) QuantumState {
	return QuantumState{
		NodeID:    nodeID,
		Spin:      spin,
		Phase:     phase,
		Fidelity:  fidelity,
		Timestamp: time.Now().Add(-time.Second), // Slightly in the past
	}
}

// TestGenerateQuantumStates tests quantum state generation
func TestGenerateQuantumStates(t *testing.T) {
	qc := NewQuantumChecker(false)
	nodes := []string{"node1", "node2", "node3"}

	states := qc.GenerateQuantumStates(nodes)

	// Verify we got the right number of states
	if len(states) != len(nodes) {
		t.Errorf("Expected %d states, got %d", len(nodes), len(states))
	}

	// Verify each state has correct node ID
	for i, state := range states {
		if state.NodeID != nodes[i] {
			t.Errorf("Expected node ID %s, got %s", nodes[i], state.NodeID)
		}
	}

	// Verify fidelity is within expected range (95-100%)
	for _, state := range states {
		if state.Fidelity < 0.95 || state.Fidelity > 1.0 {
			t.Errorf("Expected fidelity between 0.95 and 1.0, got %.3f", state.Fidelity)
		}
	}
}

// TestVerifyEntanglement tests entanglement verification
func TestVerifyEntanglement(t *testing.T) {
	qc := NewQuantumChecker(false)

	// Test with highly correlated states
	stateA := MockQuantumState("node1", 0.5, 1.0, 0.98)
	stateB := MockQuantumState("node2", 0.51, 1.02, 0.97)

	result := qc.VerifyEntanglement(stateA, stateB)

	// Verify basic properties
	if result.NodeA != "node1" {
		t.Errorf("Expected NodeA to be 'node1', got '%s'", result.NodeA)
	}
	if result.NodeB != "node2" {
		t.Errorf("Expected NodeB to be 'node2', got '%s'", result.NodeB)
	}

	// Verify correlation (should be high for similar states)
	if !result.Correlated {
		t.Errorf("Expected states to be correlated, but they were not")
	}

	// Verify fidelity is reasonable
	if result.Fidelity <= 0 || result.Fidelity > 1.0 {
		t.Errorf("Expected fidelity between 0 and 1, got %.3f", result.Fidelity)
	}

	// Verify spooky score is reasonable
	if result.SpookyScore <= 0 || result.SpookyScore > 10.0 {
		t.Errorf("Expected spooky score between 0 and 10, got %.3f", result.SpookyScore)
	}

	// Verify Bell inequality is violated for correlated states
	if result.BellInequality != "VIOLATED" {
		t.Errorf("Expected Bell inequality to be VIOLATED for correlated states, got '%s'", result.BellInequality)
	}
}

// TestVerifyEntanglementDecoherence tests decoherence effects
func TestVerifyEntanglementDecoherence(t *testing.T) {
	qc := NewQuantumChecker(false)

	// Create states with old timestamps to test decoherence
	oldTime := time.Now().Add(-time.Hour)
	stateA := QuantumState{NodeID: "node1", Spin: 0.5, Phase: 1.0, Fidelity: 0.98, Timestamp: oldTime}
	stateB := QuantumState{NodeID: "node2", Spin: 0.51, Phase: 1.02, Fidelity: 0.97, Timestamp: oldTime}

	result := qc.VerifyEntanglement(stateA, stateB)

	// With significant time difference, correlation should be lower
	// This tests the decoherence effect
	if result.Fidelity > 0.8 {
		t.Errorf("Expected significant decoherence effect with old timestamps, got fidelity %.3f", result.Fidelity)
	}
}

// TestVerifyEntanglementUncorrelated tests uncorrelated states
func TestVerifyEntanglementUncorrelated(t *testing.T) {
	qc := NewQuantumChecker(false)

	// Create states with very different spins and phases
	stateA := MockQuantumState("node1", 1.0, 0.0, 0.95)
	stateB := MockQuantumState("node2", -1.0, 3.14159, 0.95)

	result := qc.VerifyEntanglement(stateA, stateB)

	// These states should not be correlated
	if result.Correlated {
		t.Errorf("Expected states to be uncorrelated, but they were correlated")
	}

	// Bell inequality should be satisfied for uncorrelated states
	if result.BellInequality != "SATISFIED" {
		t.Errorf("Expected Bell inequality to be SATISFIED for uncorrelated states, got '%s'", result.BellInequality)
	}
}

// TestCalculateOverallEntanglement tests overall fidelity calculation
func TestCalculateOverallEntanglement(t *testing.T) {
	qc := NewQuantumChecker(false)

	// Create test results
	results := []EntanglementResult{
		{Fidelity: 0.95},
		{Fidelity: 0.90},
		{Fidelity: 0.85},
	}

	overall := qc.CalculateOverallEntanglement(results)

	// Expected: (0.95 + 0.90 + 0.85) / 3 = 0.90
	expected := 0.90
	diff := overall - expected
	if diff < 0 {
		diff = -diff
	}

	// Allow small floating point errors
	if diff > 0.001 {
		t.Errorf("Expected overall fidelity %.3f, got %.3f", expected, overall)
	}
}

// TestCalculateOverallEntanglementEmpty tests empty results
func TestCalculateOverallEntanglementEmpty(t *testing.T) {
	qc := NewQuantumChecker(false)
	results := []EntanglementResult{}

	overall := qc.CalculateOverallEntanglement(results)

	if overall != 0 {
		t.Errorf("Expected 0 for empty results, got %.3f", overall)
	}
}

// TestAbsFloat tests the absolute value function
func TestAbsFloat(t *testing.T) {
	testCases := []struct {
		input    float64
		expected float64
	}{
		{1.5, 1.5},
		{-1.5, 1.5},
		{0.0, 0.0},
		{-0.0, 0.0},
		{100.0, 100.0},
		{-100.0, 100.0},
	}

	for _, tc := range testCases {
		result := absFloat(tc.input)
		if result != tc.expected {
			t.Errorf("absFloat(%.3f) = %.3f, expected %.3f", tc.input, result, tc.expected)
		}
	}
}

// TestSplitNodes tests node string splitting
func TestSplitNodes(t *testing.T) {
	testCases := []struct {
		input    string
		expected []string
	}{
		{"node1,node2,node3", []string{"node1", "node2", "node3"}},
		{"single", []string{"single"}},
		{"", []string{}},
		{"node1,,node3", []string{"node1", "node3"}},
		{"node1, node2, node3", []string{"node1", " node2", " node3"}},
	}

	for _, tc := range testCases {
		result := splitNodes(tc.input)
		if len(result) != len(tc.expected) {
			t.Errorf("splitNodes('%s') returned %d elements, expected %d", tc.input, len(result), len(tc.expected))
			continue
		}
		for i := range result {
			if result[i] != tc.expected[i] {
				t.Errorf("splitNodes('%s')[%d] = '%s', expected '%s'", tc.input, i, result[i], tc.expected[i])
			}
		}
	}
}

// TestConcurrentEntanglementVerification tests concurrent verification
func TestConcurrentEntanglementVerification(t *testing.T) {
	qc := NewQuantumChecker(false)

	// Create multiple states
	states := []QuantumState{
		MockQuantumState("node1", 0.5, 1.0, 0.98),
		MockQuantumState("node2", 0.51, 1.02, 0.97),
		MockQuantumState("node3", 0.49, 0.98, 0.96),
		MockQuantumState("node4", 0.52, 1.01, 0.95),
	}

	results := qc.VerifyAllEntanglements(states)

	// For 4 nodes, we should have 6 pairs (4*3/2)
	expectedPairs := 6
	if len(results) != expectedPairs {
		t.Errorf("Expected %d entanglement results, got %d", expectedPairs, len(results))
	}

	// Verify all results are valid
	for _, result := range results {
		if result.Fidelity <= 0 || result.Fidelity > 1.0 {
			t.Errorf("Invalid fidelity in result: %.3f", result.Fidelity)
		}
		if result.SpookyScore <= 0 || result.SpookyScore > 10.0 {
			t.Errorf("Invalid spooky score in result: %.3f", result.SpookyScore)
		}
	}
}

// BenchmarkQuantumStateGeneration benchmarks quantum state generation
func BenchmarkQuantumStateGeneration(b *testing.B) {
	qc := NewQuantumChecker(false)
	nodes := []string{"node1", "node2", "node3", "node4", "node5"}

	for i := 0; i < b.N; i++ {
		qc.GenerateQuantumStates(nodes)
	}
}

// BenchmarkEntanglementVerification benchmarks entanglement verification
func BenchmarkEntanglementVerification(b *testing.B) {
	qc := NewQuantumChecker(false)
	states := []QuantumState{
		MockQuantumState("node1", 0.5, 1.0, 0.98),
		MockQuantumState("node2", 0.51, 1.02, 0.97),
		MockQuantumState("node3", 0.49, 0.98, 0.96),
		MockQuantumState("node4", 0.52, 1.01, 0.95),
		MockQuantumState("node5", 0.50, 1.00, 0.94),
	}

	for i := 0; i < b.N; i++ {
		qc.VerifyAllEntanglements(states)
	}
}
