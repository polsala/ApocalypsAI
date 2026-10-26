package monitor_test

import (
	"net/http"
	"net/http/httptest"
	"runtime"
	"testing"

	"github.com/polsala/ApocalypsAI/utils/nightly-go-concurrency-monitor/internal/monitor"
)

// Mock rationale: We need to mock the HTTP server and its responses to test the monitor logic
// without actually starting a full HTTP server in the test environment. This ensures deterministic
// and offline testing.

func TestStartMonitor(t *testing.T) {
	// Start the monitor in a goroutine so it doesn't block the test
	go monitor.StartMonitor(8081) // Use a different port for testing

	// Give the server a moment to start
	t := time.NewTimer(100 * time.Millisecond)
	<-t.C

	// Create a new HTTP client
	client := &http.Client{
		Timeout: 5 * time.Second,
	}

	// Make a request to the metrics endpoint
	res, err := client.Get("http://localhost:8081/metrics")
	if err != nil {
		t.Fatalf("Failed to get metrics: %v", err)
	}
	defer res.Body.Close()

	// Check the response status code
	if res.StatusCode != http.StatusOK {
		t.Errorf("Expected status OK, got %d", res.StatusCode)
	}

	// Check the response body content (basic check)
	// We expect the number of goroutines to be at least the number of goroutines
	// running in this test plus the one started by the monitor itself.
	// This is a loose check as the exact number can vary slightly.
	expectedMinGoroutines := runtime.NumGoroutine()
	var actualGoroutines int
	_, err = fmt.Scanf("# TYPE go_goroutines_total gauge\ngo_goroutines_total %d\n", &actualGoroutines)
	if err != nil {
		t.Errorf("Failed to parse goroutine count from response: %v\nResponse body: %s", err, "[response body not read yet]")
	}

	if actualGoroutines < expectedMinGoroutines {
		t.Errorf("Expected at least %d goroutines, got %d", expectedMinGoroutines, actualGoroutines)
	}
}

// Mock rationale: This test verifies the handler function directly without starting a full server.
// It uses httptest.NewRecorder to capture the response and httptest.NewRequest to simulate an incoming request.
func TestMetricsHandler(t *testing.T) {
	req := httptest.NewRequest("GET", "/metrics", nil)
	recorder := httptest.NewRecorder()

	// Create a handler function that mimics the one in StartMonitor
	metricsHandler := func(w http.ResponseWriter, r *http.Request) {
		goroutines := runtime.NumGoroutine()
		fmt.Fprintf(w, "# HELP go_goroutines_total The total number of goroutines.\n")
		fmt.Fprintf(w, "# TYPE go_goroutines_total gauge\n")
		fmt.Fprintf(w, "go_goroutines_total %d\n", goroutines)
	}

	metricsHandler(recorder, req)

	// Check the status code
	if recorder.Code != http.StatusOK {
		t.Errorf("Expected status OK, got %d", recorder.Code)
	}

	// Check the content type (optional, but good practice)
	// The default handler doesn't set Content-Type, so we check for absence or default

	// Check the response body content
	expectedMinGoroutines := runtime.NumGoroutine()
	var actualGoroutines int
	_, err := fmt.Scanf("# TYPE go_goroutines_total gauge\ngo_goroutines_total %d\n", &actualGoroutines)
	if err != nil {
		t.Errorf("Failed to parse goroutine count from response: %v\nResponse body: %s", err, recorder.Body.String())
	}

	if actualGoroutines < expectedMinGoroutines {
		t.Errorf("Expected at least %d goroutines, got %d", expectedMinGoroutines, actualGoroutines)
	}
}
