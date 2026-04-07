package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"runtime"
	"strings"
	"testing"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/polsala/ApocalypsAI/utils/nightly-go-concurrency-monitor/src/concurrency_monitor"
)

func TestConcurrencyMonitor(t *testing.T) {
	// Mock runtime functions
	originalNumGoroutine := runtime.NumGoroutine
	originalReadMemStats := runtime.ReadMemStats

	defer func() {
		runtime.NumGoroutine = originalNumGoroutine
		runtime.ReadMemStats = originalReadMemStats
	}()

	// --- Test Case 1: Default Configuration --- 
	t.Run("default_config", func(t *testing.T) {
		// Reset global state for each test run
		concurrency_monitor.initOnce = sync.Once{}

		// Mock runtime.NumGoroutine to return a fixed value
		concurrency_monitor.SetRuntimeNumGoroutine(func() int { return 10 })
		// Mock runtime.ReadMemStats to do nothing (as it's not directly used for channel blocking in this simplified version)
		concurrency_monitor.SetRuntimeReadMemStats(func(m *runtime.MemStats) { /* no-op */ })
		// Explicitly set the channel blocked value for this test
		concurrency_monitor.SetChannelBlockedGoroutines(1.0)

		// Start the monitor with default port 8080 and interval
		concurrency_monitor.Start()

		// Give the server a moment to start
		time.Sleep(100 * time.Millisecond)

		// Make a request to the metrics endpoint
		req, err := http.NewRequest("GET", "/metrics", nil)
		if err != nil {
			t.Fatalf("Failed to create request: %v", err)
		}
		w := httptest.NewRecorder()
		http.DefaultServeMux.ServeHTTP(w, req)

		resp := w.Result()
		if resp.StatusCode != http.StatusOK {
			t.Errorf("Expected status OK, got %d", resp.StatusCode)
		}

		body := w.Body.String()
		if !strings.Contains(body, "go_goroutines_total 10") {
			t.Errorf("Expected 'go_goroutines_total 10' in response, got: %s", body)
		}
		if !strings.Contains(body, "go_channel_blocked_goroutines 1") {
			t.Errorf("Expected 'go_channel_blocked_goroutines 1' in response, got: %s", body)
		}
	})

	// --- Test Case 2: Custom Port and Interval --- 
	t.Run("custom_config", func(t *testing.T) {
		// Reset global state for each test run
		concurrency_monitor.initOnce = sync.Once{}

		// Mock runtime functions
		concurrency_monitor.SetRuntimeNumGoroutine(func() int { return 5 })
		concurrency_monitor.SetRuntimeReadMemStats(func(m *runtime.MemStats) { /* no-op */ })
		concurrency_monitor.SetChannelBlockedGoroutines(0.0)

		customPort := 9090
		customInterval := 1 * time.Second

		// Start the monitor with custom port and interval
		concurrency_monitor.Start(concurrency_monitor.WithPort(customPort), concurrency_monitor.WithInterval(customInterval))

		// Give the server a moment to start
		time.Sleep(100 * time.Millisecond)

		// Make a request to the metrics endpoint on the custom port
		metricsURL := fmt.Sprintf("http://localhost:%d/metrics", customPort)
		resp, err := http.Get(metricsURL)
		if err != nil {
			t.Fatalf("Failed to get metrics from %s: %v", metricsURL, err)
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			t.Errorf("Expected status OK, got %d", resp.StatusCode)
		}

		body := w.Body.String()
		if !strings.Contains(body, "go_goroutines_total 5") {
			t.Errorf("Expected 'go_goroutines_total 5' in response, got: %s", body)
		}
		if !strings.Contains(body, "go_channel_blocked_goroutines 0") {
			t.Errorf("Expected 'go_channel_blocked_goroutines 0' in response, got: %s", body)
		}
	})
}

// Helper function to reset the Prometheus registry for isolated tests.
func resetPrometheusRegistry() {
	// This is a bit of a hack, as Prometheus doesn't provide a public way to unregister metrics easily.
	// In a real-world scenario, you might want to manage the registry more explicitly.
	// For this example, we'll assume a fresh registry is created implicitly or that tests are run in isolation.
	// If running tests sequentially, this might need more robust handling.
}
