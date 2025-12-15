package main

import (
	"context"
	"fmt"
	"net/http"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/polsala/ApocalypsAI/go-utils/nightly-quantum-entanglement-checker/internal/config"
	"github.com/polsala/ApocalypsAI/go-utils/nightly-quantum-entanglement-checker/internal/server"
)

func TestServerIntegration(t *testing.T) {
	// Integration test for the complete server
	cfg := config.Default()
	cfg.Server.Port = 0 // Use any available port

	srv := server.New(cfg)

	// Start server in background
	go func() {
		err := srv.Start()
		if err != nil && err != http.ErrServerClosed {
			t.Errorf("Server error: %v", err)
		}
	}()

	// Wait for server to start
	time.Sleep(100 * time.Millisecond)

	// Get actual server address
	serverURL := fmt.Sprintf("http://localhost:%d", cfg.Server.Port)

	t.Run("Full Workflow", func(t *testing.T) {
		// Test complete workflow
		client := &http.Client{Timeout: 5 * time.Second}

		// 1. Health check
		healthResp, err := client.Get(serverURL + "/api/v1/health")
		require.NoError(t, err)
		healthResp.Body.Close()
		assert.Equal(t, http.StatusOK, healthResp.StatusCode)

		// 2. Generate pairs
		postResp, err := client.Post(
			serverURL+"/api/v1/entangle",
			"application/json",
			strings.NewReader(`{"pairs": 2, "fidelity": 0.9}`),
		)
		require.NoError(t, err)
		postResp.Body.Close()
		assert.Equal(t, http.StatusOK, postResp.StatusCode)

		// 3. Check coherence
		coherenceResp, err := client.Get(serverURL + "/api/v1/coherence")
		require.NoError(t, err)
		coherenceResp.Body.Close()
		assert.Equal(t, http.StatusOK, coherenceResp.StatusCode)
	})

	// Shutdown server
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(); err != nil {
		t.Errorf("Server shutdown error: %v", err)
	}

	<-ctx.Done()
}

func TestConcurrentAccess(t *testing.T) {
	// Test concurrent access to server
	cfg := config.Default()
	cfg.Server.Port = 0

	srv := server.New(cfg)

	// Start server
	go srv.Start()
	time.Sleep(100 * time.Millisecond)

	serverURL := fmt.Sprintf("http://localhost:%d", cfg.Server.Port)
	client := &http.Client{Timeout: 5 * time.Second}

	// Launch multiple concurrent requests
	concurrentRequests := 10
	results := make(chan error, concurrentRequests)

	for i := 0; i < concurrentRequests; i++ {
		go func() {
			resp, err := client.Get(serverURL + "/api/v1/health")
			if err != nil {
				results <- err
				return
			}
			resp.Body.Close()
			if resp.StatusCode != http.StatusOK {
				results <- fmt.Errorf("unexpected status: %d", resp.StatusCode)
				return
			}
			results <- nil
		}()
	}

	// Collect results
	errCount := 0
	for i := 0; i < concurrentRequests; i++ {
		if err := <-results; err != nil {
			errCount++
		}
	}

	assert.Equal(t, 0, errCount, "All concurrent requests should succeed")

	// Shutdown
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	srv.Shutdown()
	<-ctx.Done()
}

// Mock rationale: Using concurrent goroutines to test server thread safety
// and ability to handle multiple simultaneous requests.

// Mock rationale: Testing server shutdown to ensure graceful cleanup
// and proper resource management.
