package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
	"github.com/polsala/ApocalypsAI/utils/nightly-go-concurrency-monitor/concurrencymonitor"
)

// Mock rationale: We are mocking the HTTP server and its responses to ensure deterministic testing.
// The actual runtime.NumGoroutine() is not mocked as it's part of the Go runtime and its behavior is predictable for testing purposes.

func TestConcurrencyMonitor(t *testing.T) {
	// Start the monitor in a goroutine so it doesn't block the test
	go concurrencymonitor.Start(":8082")

	// Give the server a moment to start up
	time.Sleep(100 * time.Millisecond)

	// Create a new HTTP request to the metrics endpoint
	req, err := http.NewRequest("GET", "/metrics", nil)
	if err != nil {
		t.Fatalf("Failed to create request: %v", err)
	}

	// Use httptest.NewRecorder to record the response
	recorder := httptest.NewRecorder()

	// Create a handler for the metrics endpoint
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		promhttp.Handler().ServeHTTP(w, r)
	})

	// Serve the request
	handler.ServeHTTP(recorder, req)

	// Check the status code
	if status := recorder.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	// Check if the response body contains the expected metric
	body := recorder.Body.String()
	if !strings.Contains(body, "go_goroutines_total") {
		t.Errorf("response body does not contain 'go_goroutines_total': %s", body)
	}

	// Optionally, check for a specific value if you can control the number of goroutines
	// For this general utility, checking for the presence of the metric is sufficient.
}

// Helper function to simulate a delay for server startup
func sleep(d time.Duration) {
	time.Sleep(d)
}
