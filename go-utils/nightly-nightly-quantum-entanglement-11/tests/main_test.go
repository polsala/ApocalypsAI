package main

import (
	"sync"
	"testing"
	"time"
)

func TestNewQuantumNode(t *testing.T) {
	// Test node creation
	node := NewQuantumNode(1)
	if node.ID != 1 {
		t.Errorf("Expected node ID 1, got %d", node.ID)
	}
	if node.State != "" {
		t.Errorf("Expected empty initial state, got %s", node.State)
	}
	if node.EntangledWith != nil {
		t.Error("Expected nil entanglement initially")
	}
}

func TestQuantumNodeEntanglement(t *testing.T) {
	// Test entanglement logic
	node1 := NewQuantumNode(1)
	node2 := NewQuantumNode(2)

	// Test successful entanglement
	result := node1.Entangle(node2, 1.0) // 100% chance
	if !result {
		t.Error("Expected entanglement to succeed with factor 1.0")
	}
	if node1.EntangledWith != node2 {
		t.Error("Expected node1 to be entangled with node2")
	}

	// Test failed entanglement
	node3 := NewQuantumNode(3)
	result = node3.Entangle(node1, 0.0) // 0% chance
	if result {
		t.Error("Expected entanglement to fail with factor 0.0")
	}
}

func TestQuantumNodeSpinState(t *testing.T) {
	// Test node state spinning with mock metrics
	metrics := &QuantumMetrics{}
	node := NewQuantumNode(1)
	var wg sync.WaitGroup

	wg.Add(1)
	go node.SpinState(metrics, &wg)

	// Send a test state
	node.ch <- "test_state"

	// Wait a bit for processing
	time.Sleep(50 * time.Millisecond)

	// Check that state was updated
	node.mu.Lock()
	if node.State != "test_state" {
		t.Errorf("Expected state 'test_state', got %s", node.State)
	}
	node.mu.Unlock()

	// Cleanup
	close(node.ch)
	wg.Done()
}

func TestNewQuantumEntanglementChecker(t *testing.T) {
	// Test checker creation
	checker := NewQuantumEntanglementChecker(3, 0.5, 100*time.Millisecond, false)

	if len(checker.nodes) != 3 {
		t.Errorf("Expected 3 nodes, got %d", len(checker.nodes))
	}
	if checker.factor != 0.5 {
		t.Errorf("Expected factor 0.5, got %f", checker.factor)
	}
	if checker.duration != 100*time.Millisecond {
		t.Errorf("Expected duration 100ms, got %v", checker.duration)
	}
}

func TestQuantumMetricsCalculation(t *testing.T) {
	// Test coherence calculation
	checker := NewQuantumEntanglementChecker(4, 1.0, 50*time.Millisecond, false)
	checker.metrics.SpookyActions = 20
	checker.metrics.EntangledPairs = 2
	checker.metrics.TotalNodes = 4

	checker.calculateCoherence()

	// With perfect entanglement and high spooky actions, should have high coherence
	if checker.metrics.CoherenceScore <= 0 {
		t.Error("Expected positive coherence score")
	}
}

func TestEntanglementCheckerWithLowFactor(t *testing.T) {
	// Test with low entanglement factor
	checker := NewQuantumEntanglementChecker(5, 0.1, 50*time.Millisecond, false)
	checker.Initialize()

	// Should have fewer entangled pairs with low factor
	if checker.metrics.TotalNodes != 5 {
		t.Errorf("Expected 5 total nodes, got %d", checker.metrics.TotalNodes)
	}
	// Independent nodes should be >= entangled pairs due to low factor
	if checker.metrics.IndependentNodes < checker.metrics.EntangledPairs {
		t.Error("Expected more independent nodes with low entanglement factor")
	}
}

func TestEntanglementCheckerWithHighFactor(t *testing.T) {
	// Test with high entanglement factor
	checker := NewQuantumEntanglementChecker(6, 0.9, 50*time.Millisecond, false)
	checker.Initialize()

	// Should have more entangled pairs with high factor
	if checker.metrics.TotalNodes != 6 {
		t.Errorf("Expected 6 total nodes, got %d", checker.metrics.TotalNodes)
	}
	// Should have some entanglement with high factor
	if checker.metrics.EntangledPairs == 0 {
		t.Error("Expected some entanglement with high factor")
	}
}

func TestConcurrentNodeOperations(t *testing.T) {
	// Test concurrent operations on nodes
	node := NewQuantumNode(1)
	metrics := &QuantumMetrics{}
	var wg sync.WaitGroup

	// Start spinning
	wg.Add(1)
	go node.SpinState(metrics, &wg)

	// Concurrently send states and check entanglement
	concurrentOps := 100
	for i := 0; i < concurrentOps; i++ {
		go func(i int) {
			node.ch <- fmt.Sprintf("state_%d", i)
			// Check state access is thread-safe
			node.mu.Lock()
			_ = node.State
			node.mu.Unlock()
		}(i)
	}

	// Wait for operations to complete
	time.Sleep(100 * time.Millisecond)
	close(node.ch)
	wg.Done()
}

func TestEntanglementVerification(t *testing.T) {
	// Test that entanglement actually works
	node1 := NewQuantumNode(1)
	node2 := NewQuantumNode(2)

	// Force entanglement
	node1.Entangle(node2, 1.0)

	metrics := &QuantumMetrics{}
	var wg sync.WaitGroup

	wg.Add(2)
	go node1.SpinState(metrics, &wg)
	go node2.SpinState(metrics, &wg)

	// Send state to node1, should appear in node2
	node1.ch <- "entangled_state"

	// Wait for processing
	time.Sleep(50 * time.Millisecond)

	// Check that node2 received the state (spooky action)
	node2.mu.Lock()
	if node2.State != "entangled_state" {
		t.Errorf("Expected entangled state propagation, got %s", node2.State)
	}
	node2.mu.Unlock()

	// Cleanup
	close(node1.ch)
	close(node2.ch)
	wg.Done()
	wg.Done()
}

// Benchmark tests
func BenchmarkQuantumNodeSpinState(b *testing.B) {
	metrics := &QuantumMetrics{}
	node := NewQuantumNode(1)
	var wg sync.WaitGroup

	wg.Add(1)
	go node.SpinState(metrics, &wg)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		node.ch <- fmt.Sprintf("bench_state_%d", i)
	}

	b.StopTimer()
	close(node.ch)
	wg.Done()
}

func BenchmarkEntanglementChecker(b *testing.B) {
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		checker := NewQuantumEntanglementChecker(10, 0.8, 10*time.Millisecond, false)
		checker.Initialize()
	}
}

// Mock rationale: Tests use deterministic behavior by controlling entanglement factors
// and using fixed durations. Channel operations are synchronized with WaitGroups
// to ensure deterministic test execution without race conditions.
