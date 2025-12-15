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

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/polsala/ApocalypsAI/go-utils/nightly-quantum-entanglement-checker/internal/config"
	"github.com/polsala/ApocalypsAI/go-utils/nightly-quantum-entanglement-checker/internal/quantum"
	"github.com/polsala/ApocalypsAI/go-utils/nightly-quantum-entanglement-checker/internal/server"
)

func TestMain(t *testing.T) {
	// Test main package functions
	t.Run("GeneratePairs", testGeneratePairs)
	t.Run("VerifyEntanglement", testVerifyEntanglement)
	t.Run("MonitorCoherence", testMonitorCoherence)
}

func testGeneratePairs(t *testing.T) {
	// Test pair generation
	config := quantum.GeneratorConfig{
		DefaultFidelity: 0.95,
		MaxPairs:        100,
	}
	generator := quantum.NewPairGenerator(config)

	// Test valid generation
	pairs, err := generator.GeneratePairs(5)
	require.NoError(t, err)
	assert.Len(t, pairs, 5)

	for _, pair := range pairs {
		assert.NotEmpty(t, pair.ID)
		assert.Equal(t, "node-1", pair.NodeA)
		assert.Equal(t, "node-2", pair.NodeB)
		assert.Equal(t, 0.95, pair.Fidelity)
		assert.Equal(t, quantum.QuantumStateSuperposition, pair.StateA)
		assert.Equal(t, quantum.QuantumStateSuperposition, pair.StateB)
		assert.True(t, pair.IsEntangled())
	}

	// Test invalid count
	_, err = generator.GeneratePairs(0)
	assert.Error(t, err)

	// Test excessive count
	_, err = generator.GeneratePairs(2000)
	assert.Error(t, err)
}

func testVerifyEntanglement(t *testing.T) {
	verifier := quantum.NewEntanglementVerifier()

	// Test verification between different nodes
	result := verifier.VerifyEntanglement("node1", "node2")
	assert.False(t, result.Error != "")
	assert.GreaterOrEqual(t, result.Correlation, 0.2)
	assert.LessOrEqual(t, result.Correlation, 1.0)
	assert.GreaterOrEqual(t, result.MeasuredFidelity, 0.0)
	assert.LessOrEqual(t, result.MeasuredFidelity, 1.0)

	// Test verification between same nodes
	result = verifier.VerifyEntanglement("node1", "node1")
	assert.False(t, result.Entangled)
	assert.NotEmpty(t, result.Error)

	// Test batch verification
	batch := verifier.BatchVerify("node1", "node2", 10)
	assert.Len(t, batch, 10)

	// Test statistics
	avgFidelity := quantum.CalculateAverageFidelity(batch)
	assert.GreaterOrEqual(t, avgFidelity, 0.0)
	assert.LessOrEqual(t, avgFidelity, 1.0)

	entanglementRatio := quantum.CalculateEntanglementRatio(batch)
	assert.GreaterOrEqual(t, entanglementRatio, 0.0)
	assert.LessOrEqual(t, entanglementRatio, 1.0)
}

func testMonitorCoherence(t *testing.T) {
	monitor := quantum.NewCoherenceMonitor(0.8)

	// Test initial status
	status := monitor.GetStatus()
	assert.Equal(t, 1.0, status.Coherence)
	assert.True(t, status.Stable)
	assert.Equal(t, 0, status.Measurements)

	// Test measurement
	status = monitor.Measure()
	assert.GreaterOrEqual(t, status.Coherence, 0.0)
	assert.LessOrEqual(t, status.Coherence, 1.0)
	assert.Equal(t, 1, status.Measurements)

	// Test decoherence simulation
	status = monitor.SimulateDecoherence(10 * time.Second)
	assert.GreaterOrEqual(t, status.Coherence, 0.0)
	assert.LessOrEqual(t, status.Coherence, 1.0)
	assert.Equal(t, 2, status.Measurements)

	// Test reset
	monitor.Reset()
	status = monitor.GetStatus()
	assert.Equal(t, 1.0, status.Coherence)
	assert.True(t, status.Stable)
	assert.Equal(t, 0, status.Measurements)
}

func TestServer(t *testing.T) {
	// Test HTTP server
	cfg := config.Default()
	srv := server.New(cfg)

	// Create test server
	ts := httptest.NewServer(srv.srv.Handler)
	defer ts.Close()

	t.Run("Health Check", func(t *testing.T) {
		resp, err := http.Get(ts.URL + "/api/v1/health")
		require.NoError(t, err)
		defer resp.Body.Close()
		assert.Equal(t, http.StatusOK, resp.StatusCode)

		body, err := io.ReadAll(resp.Body)
		require.NoError(t, err)

		var health struct {
			Status    string `json:"status"`
			Timestamp string `json:"timestamp"`
			Version   string `json:"version"`
		}
		err = json.Unmarshal(body, &health)
		require.NoError(t, err)
		assert.Equal(t, "healthy", health.Status)
		assert.Equal(t, "1.0.0", health.Version)
	})

	t.Run("Generate Entangled Pairs", func(t *testing.T) {
		reqBody := `{"pairs": 3, "fidelity": 0.92}`
		resp, err := http.Post(ts.URL+"/api/v1/entangle", "application/json", bytes.NewBufferString(reqBody))
		require.NoError(t, err)
		defer resp.Body.Close()
		assert.Equal(t, http.StatusOK, resp.StatusCode)

		body, err := io.ReadAll(resp.Body)
		require.NoError(t, err)

		var result struct {
			Success bool                   `json:"success"`
			Pairs   []*quantum.QuantumPair `json:"pairs"`
			Count   int                    `json:"count"`
		}
		err = json.Unmarshal(body, &result)
		require.NoError(t, err)
		assert.True(t, result.Success)
		assert.Equal(t, 3, result.Count)
		assert.Len(t, result.Pairs, 3)
	})

	t.Run("Verify Entanglement", func(t *testing.T) {
		resp, err := http.Get(ts.URL + "/api/v1/verify?nodeA=node1&nodeB=node2")
		require.NoError(t, err)
		defer resp.Body.Close()
		assert.Equal(t, http.StatusOK, resp.StatusCode)

		body, err := io.ReadAll(resp.Body)
		require.NoError(t, err)

		var result quantum.VerificationResult
		err = json.Unmarshal(body, &result)
		require.NoError(t, err)
		assert.GreaterOrEqual(t, result.Correlation, 0.0)
		assert.LessOrEqual(t, result.Correlation, 1.0)
	})

	t.Run("Coherence Status", func(t *testing.T) {
		resp, err := http.Get(ts.URL + "/api/v1/coherence")
		require.NoError(t, err)
		defer resp.Body.Close()
		assert.Equal(t, http.StatusOK, resp.StatusCode)

		body, err := io.ReadAll(resp.Body)
		require.NoError(t, err)

		var status quantum.CoherenceStatus
		err = json.Unmarshal(body, &status)
		require.NoError(t, err)
		assert.Equal(t, 1.0, status.Coherence)
		assert.True(t, status.Stable)
	})

	t.Run("Monitor Decoherence", func(t *testing.T) {
		reqBody := `{"duration": 5}`
		resp, err := http.Post(ts.URL+"/api/v1/monitor", "application/json", bytes.NewBufferString(reqBody))
		require.NoError(t, err)
		defer resp.Body.Close()
		assert.Equal(t, http.StatusOK, resp.StatusCode)

		body, err := io.ReadAll(resp.Body)
		require.NoError(t, err)

		var status quantum.CoherenceStatus
		err = json.Unmarshal(body, &status)
		require.NoError(t, err)
		assert.GreaterOrEqual(t, status.Coherence, 0.0)
		assert.LessOrEqual(t, status.Coherence, 1.0)
	})
}

func TestConfig(t *testing.T) {
	// Test configuration loading and validation
	t.Run("Default Config", func(t *testing.T) {
		cfg := config.Default()
		assert.NoError(t, cfg.Validate())
		assert.Equal(t, 8080, cfg.Server.Port)
		assert.Equal(t, 0.95, cfg.Quantum.DefaultFidelity)
	})

	t.Run("Invalid Config", func(t *testing.T) {
		cfg := config.Default()
		cfg.Server.Port = 99999
		assert.Error(t, cfg.Validate())

		cfg.Server.Port = 8080
		cfg.Quantum.DefaultFidelity = 1.5
		assert.Error(t, cfg.Validate())
	})

	t.Run("Config Serialization", func(t *testing.T) {
		cfg := config.Default()
		jsonStr := cfg.String()
		assert.Contains(t, jsonStr, "8080")
		assert.Contains(t, jsonStr, "0.95")
	})
}

func TestQuantumPair(t *testing.T) {
	// Test quantum pair functionality
	t.Run("Pair Creation", func(t *testing.T) {
		pair := &quantum.QuantumPair{
			ID:        "test-id",
			NodeA:     "node1",
			NodeB:     "node2",
			Fidelity:  0.95,
			CreatedAt: time.Now(),
			StateA:    quantum.QuantumStateSuperposition,
			StateB:    quantum.QuantumStateSuperposition,
		}

		assert.True(t, pair.IsEntangled())
		assert.Contains(t, pair.String(), "test-id")
		assert.Contains(t, pair.String(), "node1-node2")
	})

	t.Run("Measurement", func(t *testing.T) {
		pair := &quantum.QuantumPair{
			StateA: quantum.QuantumStateSuperposition,
			StateB: quantum.QuantumStateSuperposition,
		}

		valueA, valueB := pair.Measure()
		assert.Equal(t, quantum.QuantumStateCollapsed, pair.StateA)
		assert.Equal(t, quantum.QuantumStateCollapsed, pair.StateB)
		assert.Equal(t, valueA, valueB) // Perfect correlation
	})

	t.Run("Decoherence", func(t *testing.T) {
		pair := &quantum.QuantumPair{
			Fidelity: 0.5,
			StateA:   quantum.QuantumStateSuperposition,
			StateB:   quantum.QuantumStateSuperposition,
		}

		pair.Decohere(10 * time.Minute)
		assert.Less(t, pair.Fidelity, 0.5)
		assert.Equal(t, quantum.QuantumStateDecohered, pair.StateA)
		assert.Equal(t, quantum.QuantumStateDecohered, pair.StateB)
	})
}

func TestIntegration(t *testing.T) {
	// Integration test: full workflow
	config := quantum.GeneratorConfig{DefaultFidelity: 0.9}
	generator := quantum.NewPairGenerator(config)
	verifier := quantum.NewEntanglementVerifier()
	monitor := quantum.NewCoherenceMonitor(0.8)

	// Generate pairs
	pairs, err := generator.GeneratePairs(3)
	require.NoError(t, err)
	assert.Len(t, pairs, 3)

	// Verify entanglement
	for _, pair := range pairs {
		result := verifier.VerifyEntanglement(pair.NodeA, pair.NodeB)
		assert.False(t, result.Error != "")
	}

	// Monitor coherence
	status := monitor.Measure()
	assert.Equal(t, 1, status.Measurements)
	assert.True(t, status.Stable)

	// Simulate decoherence
	status = monitor.SimulateDecoherence(60 * time.Second)
	assert.Less(t, status.Coherence, 1.0)
}

// Mock rationale: Using httptest.NewServer to create isolated HTTP tests
// without requiring actual network ports. This ensures deterministic, fast tests.

// Mock rationale: Using testify for assertions to provide clear, descriptive
// error messages and better test readability.

// Mock rationale: Testing both individual components and integration scenarios
// to ensure the system works correctly as a whole.
