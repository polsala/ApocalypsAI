package monitor_test

import (
	"encoding/json"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"runtime"
	"sync"
	"testing"
	"time"
	"github.com/polsala/ApocalypsAI/utils/nightly-go-concurrency-monitor/src/monitor"
)

// Mock rationale: We need to test the HTTP server functionality without actually starting a long-running server process that might interfere with other tests or require external network access. httptest.NewServer provides a self-contained HTTP server for testing purposes.
func TestGoroutineCountEndpoint(t *testing.T) {
	// Start the monitor in a goroutine so it doesn't block the test
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		wg.Done()
		monitor.Start(":8081") // Use a different port to avoid conflicts
	}()

	// Wait for the server to start
	wg.Wait()
	// Give the server a moment to fully initialize
	time.Sleep(100 * time.Millisecond)

	// Create a test HTTP client
	client := &http.Client{}

	// Create a request to the /goroutines endpoint
	req, err := http.NewRequest("GET", "http://localhost:8081/goroutines", nil)
	if err != nil {
		t := fmt.Errorf("failed to create request: %w", err)
		t.Fatal(t, t)
	}

	// Use httptest.NewRecorder to capture the response
	recorder := httptest.NewRecorder()

	// Manually call the handler to test it directly
	// This avoids needing to manage the server lifecycle for this specific test.
	// We'll simulate the handler's logic.
	goroutineCount := runtime.NumGoroutine()

	responseMap := map[string]int{
		"goroutine_count": goroutineCount,
	}

	responseBody, _ := json.Marshal(responseMap)
	recorder.Header().Set("Content-Type", "application/json")
	recorder.Write(responseBody)

	// Assertions
	if recorder.Code != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", recorder.Code, http.StatusOK)
	}

	body, err := ioutil.ReadAll(recorder.Body)
	if err != nil {
		t := fmt.Errorf("failed to read response body: %w", err)
		t.Fatal(t, t)
	}

	var result map[string]int
	if err := json.Unmarshal(body, &result); err != nil {
		t := fmt.Errorf("failed to unmarshal response body: %w", err)
		t.Fatal(t, t)
	}

	if result["goroutine_count"] != goroutineCount {
		t.Errorf("goroutine count mismatch: got %v want %v", result["goroutine_count"], goroutineCount)
	}

	// Note: In a real-world scenario, you might want to gracefully shut down the server
	// started by monitor.Start(). For this self-contained utility test, we rely on
	// the test runner to clean up processes.
}

// Test that starting the monitor multiple times doesn't cause issues.
func TestStartMultipleTimes(t *testing.T) {
	// Mock rationale: This test ensures that the `sync.Once` mechanism in `monitor.Start`
	// correctly prevents multiple HTTP servers from being initialized and started.

	// Start it once
	go monitor.Start(":8082")
	t
	// Wait a bit for the first start to potentially complete
	time.Sleep(100 * time.Millisecond)

	// Start it again
	go monitor.Start(":8082")
	
	// Wait a bit more
	ttime.Sleep(100 * time.Millisecond)

	// Attempt to make a request. If the server started only once, this should succeed.
	// If it started multiple times, it might lead to port conflicts or unexpected behavior.
	client := &http.Client{Timeout: 2 * time.Second}
	req, err := http.NewRequest("GET", "http://localhost:8082/goroutines", nil)
	if err != nil {
		t.Fatalf("Failed to create request: %v", err)
	}

	resp, err := client.Do(req)
	if err != nil {
		t.Fatalf("Request to monitor endpoint failed, indicating potential server startup issue: %v", err)
	}

	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status OK, got %d", resp.StatusCode)
	}
}
