package main

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

// MockHTTPClient for testing HTTP interactions
type MockHTTPClient struct {
	DoFunc func(req *http.Request) (*http.Response, error)
}

func (m *MockHTTPClient) Do(req *http.Request) (*http.Response, error) {
	if m.DoFunc != nil {
		return m.DoFunc(req)
	}
	return nil, nil
}

func TestGenerateEntangledPairs(t *testing.T) {
	// Mock rationale: Test that entangled pairs are generated with perfect anti-correlation
	pairs := generateEntangledPairs(10)

	if len(pairs) != 10 {
		t.Errorf("Expected 10 pairs, got %d", len(pairs))
	}

	for i, pair := range pairs {
		if len(pair) != 2 {
			t.Errorf("Pair %d should have 2 particles, got %d", i, len(pair))
		}

		// Check anti-correlation (entanglement)
		correlation := pair[0].Spin * pair[1].Spin
		if correlation > 0 {
			t.Errorf("Pair %d particles should be anti-correlated, got correlation %.2f", i, correlation)
		}
	}
}

func TestCalculateEntanglementFidelity(t *testing.T) {
	// Mock rationale: Test fidelity calculation with known entangled pairs
	pairs := [][]QuantumParticle{
		{{Spin: 1.0}, {Spin: -1.0}},
		{{Spin: 0.5}, {Spin: -0.5}},
		{{Spin: 2.0}, {Spin: -2.0}},
	}

	fidelity := calculateEntanglementFidelity(pairs)

	// With perfect anti-correlation, fidelity should be high
	if fidelity < 0.5 {
		t.Errorf("Expected high fidelity for entangled pairs, got %.2f", fidelity)
	}
}

func TestCalculateBellInequality(t *testing.T) {
	// Mock rationale: Test Bell inequality calculation
	pairs := [][]QuantumParticle{
		{{Spin: 1.0}, {Spin: -1.0}},
		{{Spin: 0.5}, {Spin: -0.5}},
	}

	bell := calculateBellInequality(pairs)

	// Bell inequality should be > 2 for quantum entanglement
	if bell <= 2.0 {
		t.Errorf("Expected Bell inequality > 2.0 for entangled pairs, got %.2f", bell)
	}
}

func TestGenerateQuantumStateDescription(t *testing.T) {
	// Mock rationale: Test quantum state descriptions
	tests := []struct {
		fidelity float64
		bell     float64
		expected string
	}{
		{0.98, 2.8, "Spooky action at a distance confirmed!"},
		{0.92, 2.3, "Quantum entanglement stable"},
		{0.85, 2.1, "Weak entanglement detected"},
		{0.7, 1.9, "Classical correlation only"},
	}

	for _, tt := range tests {
		result := generateQuantumStateDescription(tt.fidelity, tt.bell)
		if !strings.Contains(result, tt.expected) {
			t.Errorf("Expected description containing '%s', got '%s'", tt.expected, result)
		}
	}
}

func TestHandleQuantumMeasurement(t *testing.T) {
	// Mock rationale: Test HTTP endpoint for quantum measurements
	reqBody := QuantumParticle{ID: 1, Spin: 0.5, Node: "test-node"}
	jsonBody, _ := json.Marshal(reqBody)

	req := httptest.NewRequest(http.MethodPost, "/measure", bytes.NewBuffer(jsonBody))
	req.Header.Set("Content-Type", "application/json")

	w := httptest.NewRecorder()
	handleQuantumMeasurement(w, req)

	resp := w.Result()
	body, _ := io.ReadAll(resp.Body)

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}

	if !strings.Contains(string(body), "measured") {
		t.Errorf("Expected response to contain 'measured', got %s", string(body))
	}
}

func TestHandleHealthCheck(t *testing.T) {
	// Mock rationale: Test health check endpoint
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	w := httptest.NewRecorder()
	handleHealthCheck(w, req)

	resp := w.Result()
	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}
}

func TestSendParticlesToNode(t *testing.T) {
	// Mock rationale: Test sending particles to a mock server
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/measure" {
			http.Error(w, "Not Found", http.StatusNotFound)
			return
		}
		w.WriteHeader(http.StatusOK)
	}))
	defer server.Close()

	particles := []QuantumParticle{
		{ID: 1, Spin: 0.5, Node: server.URL},
		{ID: 2, Spin: -0.5, Node: server.URL},
	}

	err := sendParticlesToNode(strings.TrimPrefix(server.URL, "http://"), particles)
	if err != nil {
		t.Errorf("Expected no error, got %v", err)
	}
}

func TestDistributeParticles(t *testing.T) {
	// Mock rationale: Test particle distribution across nodes
	nodes = []string{"node1:8080", "node2:8080"}
	pairs := [][]QuantumParticle{
		{{ID: 0}, {ID: 1}},
		{{ID: 2}, {ID: 3}},
		{{ID: 4}, {ID: 5}},
	}

	distribution := distributeParticles(pairs)

	// Check that particles are distributed
	totalParticles := 0
	for _, particles := range distribution {
		totalParticles += len(particles)
	}

	if totalParticles != 6 {
		t.Errorf("Expected 6 particles distributed, got %d", totalParticles)
	}

	// Check that each node has particles
	if len(distribution) != 2 {
		t.Errorf("Expected 2 nodes in distribution, got %d", len(distribution))
	}
}

func TestCalculateCorrelation(t *testing.T) {
	// Mock rationale: Test correlation calculation between particles
	p1 := QuantumParticle{Spin: 1.0}
	p2 := QuantumParticle{Spin: -1.0}

	correlation := calculateCorrelation(p1, p2)

	// For perfectly anti-correlated particles, correlation should be positive
	if correlation <= 0 {
		t.Errorf("Expected positive correlation for anti-correlated particles, got %.2f", correlation)
	}
}

func TestEntanglementResultSerialization(t *testing.T) {
	// Mock rationale: Test that results can be serialized to JSON
	result := EntanglementResult{
		Fidelity:        0.95,
		BellInequality:  2.71,
		AverageLatency:  42.5,
		QuantumState:    "Test state",
		TotalParticles:  1000,
		CorrelatedPairs: 950,
	}

	data, err := json.Marshal(result)
	if err != nil {
		t.Errorf("Expected successful serialization, got error: %v", err)
	}

	if !strings.Contains(string(data), "Fidelity") {
		t.Errorf("Expected serialized data to contain 'Fidelity', got %s", string(data))
	}
}

func TestConcurrentParticleDistribution(t *testing.T) {
	// Mock rationale: Test that particles can be distributed concurrently without race conditions
	nodes = []string{"localhost:9001"}
	pairs := generateEntangledPairs(100)
	distribution := distributeParticles(pairs)

	var wg sync.WaitGroup
	var mu sync.Mutex
	distributedCount := 0

	for node, particles := range distribution {
		wg.Add(1)
		go func(node string, particles []QuantumParticle) {
			defer wg.Done()
			mu.Lock()
			distributedCount += len(particles)
			mu.Unlock()
		}(node, particles)
	}

	wg.Wait()

	if distributedCount != 200 {
		t.Errorf("Expected 200 particles distributed, got %d", distributedCount)
	}
}

func TestBellInequalityWithNoise(t *testing.T) {
	// Mock rationale: Test Bell inequality calculation with quantum noise
	pairs := generateEntangledPairs(50)
	bell1 := calculateBellInequality(pairs)
	time.Sleep(1 * time.Millisecond) // Ensure different seed
	pairs2 := generateEntangledPairs(50)
	bell2 := calculateBellInequality(pairs2)

	// Results should be similar but not identical due to randomness
	if math.Abs(bell1-bell2) > 0.5 {
		t.Errorf("Bell inequality should be consistent, got %.2f vs %.2f", bell1, bell2)
	}
}

func BenchmarkGenerateEntangledPairs(b *testing.B) {
	// Mock rationale: Benchmark particle generation performance
	for i := 0; i < b.N; i++ {
		generateEntangledPairs(1000)
	}
}

func BenchmarkCalculateEntanglementFidelity(b *testing.B) {
	// Mock rationale: Benchmark fidelity calculation
	pairs := generateEntangledPairs(1000)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		calculateEntanglementFidelity(pairs)
	}
}
