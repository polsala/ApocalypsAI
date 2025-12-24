package main

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"net/http"
	"strings"
	"sync"
	"testing"
	"time"
)

// MockHTTPClient implements the HTTPClient interface for testing.
type MockHTTPClient struct {
	Responses map[string]*http.Response // URL -> Response
	Errors    map[string]error          // URL -> Error
	Delays    map[string]time.Duration  // URL -> Delay
	mu        sync.Mutex
}

// Mock rationale: We need to control HTTP responses (status, body, errors, latency)
// deterministically for testing the ChronoWatchdog's logic without making actual network calls.
// This mock allows us to simulate various scenarios like content changes, latency spikes, and network failures.
func (m *MockHTTPClient) Get(url string) (*http.Response, error) {
	m.mu.Lock()
	defer m.mu.Unlock()

	if delay, ok := m.Delays[url]; ok {
		time.Sleep(delay)
	}

	if err, ok := m.Errors[url]; ok {
		return nil, err
	}

	if resp, ok := m.Responses[url]; ok {
		// Create a new response to avoid modifying the original mock response
		// especially if the body is read. This ensures the body can be read multiple times if needed by tests.
		newResp := *resp
		if resp.Body != nil {
			bodyBytes, _ := io.ReadAll(resp.Body)
			// Reset the original body's reader for potential subsequent reads if the mock is reused
			// (though in this specific mock, we're creating a new response struct).
			// For safety, ensure the original body is closed if it was consumed.
			resp.Body.Close() 
			newResp.Body = io.NopCloser(bytes.NewReader(bodyBytes))
		}
		return &newResp, nil
	}

	return nil, fmt.Errorf("no mock response for %s", url)
}

func TestChronoWatchdog_InitialCheck(t *testing.T) {
	var logBuffer bytes.Buffer
	testLogger := log.New(&logBuffer, "", 0)

	mockClient := &MockHTTPClient{
		Responses: map[string]*http.Response{
			"http://test.com/page1": {
				StatusCode: http.StatusOK,
				Body:       io.NopCloser(strings.NewReader("initial content")),
			},
		},
	}

	watchdog := NewChronoWatchdog([]string{"http://test.com/page1"}, 1*time.Second, mockClient, testLogger)
	stopCh := make(chan struct{})
	defer close(stopCh)

	// Run checkAllURLs once
	watchdog.checkAllURLs()

	output := logBuffer.String()
	if !strings.Contains(output, "Initial check for http://test.com/page1") {
		t.Errorf("Expected initial check message, got:\n%s", output)
	}
	if !strings.Contains(output, "Hash=") {
		t.Errorf("Expected hash in output, got:\n%s", output)
	}
	if !strings.Contains(output, "Latency=") {
		t.Errorf("Expected latency in output, got:\n%s", output)
	}

	// Verify state was stored
	watchdog.mu.Lock()
	state, exists := watchdog.states["http://test.com/page1"]
	watchdog.mu.Unlock()
	if !exists || state.ContentHash == "" {
		t.Errorf("Expected state to be stored after initial check")
	}
}

func TestChronoWatchdog_ContentChange(t *testing.T) {
	var logBuffer bytes.Buffer
	testLogger := log.New(&logBuffer, "", 0)

	mockClient := &MockHTTPClient{
		Responses: map[string]*http.Response{
			"http://test.com/page1": {
				StatusCode: http.StatusOK,
				Body:       io.NopCloser(strings.NewReader("initial content")),
			},
		},
	}

	watchdog := NewChronoWatchdog([]string{"http://test.com/page1"}, 1*time.Second, mockClient, testLogger)
	stopCh := make(chan struct{})
	defer close(stopCh)

	// First check: initial content
	watchdog.checkAllURLs()
	logBuffer.Reset() // Clear buffer for next check

	// Update mock response for content change
	mockClient.mu.Lock()
	mockClient.Responses["http://test.com/page1"].Body = io.NopCloser(strings.NewReader("updated content"))
	mockClient.mu.Unlock()

	// Second check: content changed
	watchdog.checkAllURLs()

	output := logBuffer.String()
	if !strings.Contains(output, "[ANOMALY] Content change detected for http://test.com/page1!") {
		t.Errorf("Expected content change anomaly, got:\n%s", output)
	}
	if !strings.Contains(output, "Old Hash:") || !strings.Contains(output, "New Hash:") {
		t.Errorf("Expected old and new hashes in output, got:\n%s", output)
	}
}

func TestChronoWatchdog_LatencyAnomaly(t *testing.T) {
	var logBuffer bytes.Buffer
	testLogger := log.New(&logBuffer, "", 0)

	mockClient := &MockHTTPClient{
		Responses: map[string]*http.Response{
			"http://test.com/page1": {
				StatusCode: http.StatusOK,
				Body:       io.NopCloser(strings.NewReader("consistent content")),
			},
		},
		Delays: map[string]time.Duration{
			"http://test.com/page1": 10 * time.Millisecond, // Initial low latency
		},
	}

	watchdog := NewChronoWatchdog([]string{"http://test.com/page1"}, 1*time.Second, mockClient, testLogger)
	stopCh := make(chan struct{})
	defer close(stopCh)

	// First check: initial state with low latency
	watchdog.checkAllURLs()
	logBuffer.Reset() // Clear buffer for next check

	// Update mock response for higher latency (more than double)
	mockClient.mu.Lock()
	mockClient.Delays["http://test.com/page1"] = 50 * time.Millisecond // Increased latency
	mockClient.mu.Unlock()

	// Second check: latency anomaly
	watchdog.checkAllURLs()

	output := logBuffer.String()
	if !strings.Contains(output, "[ANOMALY] Significant latency increase for http://test.com/page1!") {
		t.Errorf("Expected latency anomaly, got:\n%s", output)
	}
	if !strings.Contains(output, "Old Latency:") || !strings.Contains(output, "New Latency:") {
		t.Errorf("Expected old and new latencies in output, got:\n%s", output)
	}
}

func TestChronoWatchdog_NoChange(t *testing.T) {
	var logBuffer bytes.Buffer
	testLogger := log.New(&logBuffer, "", 0)

	mockClient := &MockHTTPClient{
		Responses: map[string]*http.Response{
			"http://test.com/page1": {
				StatusCode: http.StatusOK,
				Body:       io.NopCloser(strings.NewReader("stable content")),
			},
		},
	}

	watchdog := NewChronoWatchdog([]string{"http://test.com/page1"}, 1*time.Second, mockClient, testLogger)
	stopCh := make(chan struct{})
	defer close(stopCh)

	// First check: initial state
	watchdog.checkAllURLs()
	logBuffer.Reset() // Clear buffer for next check

	// Second check: no changes
	watchdog.checkAllURLs()

	output := logBuffer.String()
	if !strings.Contains(output, "http://test.com/page1: No significant changes.") {
		t.Errorf("Expected no change message, got:\n%s", output)
	}
}

func TestChronoWatchdog_HTTPError(t *testing.T) {
	var logBuffer bytes.Buffer
	testLogger := log.New(&logBuffer, "", 0)

	mockClient := &MockHTTPClient{
		Errors: map[string]error{
			"http://test.com/error": fmt.Errorf("network unreachable"),
		},
	}

	watchdog := NewChronoWatchdog([]string{"http://test.com/error"}, 1*time.Second, mockClient, testLogger)
	stopCh := make(chan struct{})
	defer close(stopCh)

	watchdog.checkAllURLs()

	output := logBuffer.String()
	if !strings.Contains(output, "[ERROR] Failed to fetch http://test.com/error: network unreachable") {
		t.Errorf("Expected error message for network failure, got:\n%s", output)
	}
}

func TestChronoWatchdog_Non200Status(t *testing.T) {
	var logBuffer bytes.Buffer
	testLogger := log.New(&logBuffer, "", 0)

	mockClient := &MockHTTPClient{
		Responses: map[string]*http.Response{
			"http://test.com/404": {
				StatusCode: http.StatusNotFound,
				Body:       io.NopCloser(strings.NewReader("Not Found")),
			},
		},
	}

	watchdog := NewChronoWatchdog([]string{"http://test.com/404"}, 1*time.Second, mockClient, testLogger)
	stopCh := make(chan struct{})
	defer close(stopCh)

	watchdog.checkAllURLs()

	output := logBuffer.String()
	if !strings.Contains(output, "[WARNING] http://test.com/404 returned status 404") {
		t.Errorf("Expected warning for non-200 status, got:\n%s", output)
	}
}

func TestChronoWatchdog_MultipleURLs(t *testing.T) {
	var logBuffer bytes.Buffer
	testLogger := log.New(&logBuffer, "", 0)

	mockClient := &MockHTTPClient{
		Responses: map[string]*http.Response{
			"http://test.com/pageA": {StatusCode: http.StatusOK, Body: io.NopCloser(strings.NewReader("content A"))},
			"http://test.com/pageB": {StatusCode: http.StatusOK, Body: io.NopCloser(strings.NewReader("content B"))},
		},
	}

	watchdog := NewChronoWatchdog([]string{"http://test.com/pageA", "http://test.com/pageB"}, 1*time.Second, mockClient, testLogger)
	stopCh := make(chan struct{})
	defer close(stopCh)

	watchdog.checkAllURLs()

	output := logBuffer.String()
	if !strings.Contains(output, "Initial check for http://test.com/pageA") {
		t.Errorf("Expected initial check for pageA, got:\n%s", output)
	}
	if !strings.Contains(output, "Initial check for http://test.com/pageB") {
		t.Errorf("Expected initial check for pageB, got:\n%s", output)
	}
}

func TestChronoWatchdog_StartMonitoring(t *testing.T) {
	var logBuffer bytes.Buffer
	testLogger := log.New(&logBuffer, "", 0)

	mockClient := &MockHTTPClient{
		Responses: map[string]*http.Response{
			"http://test.com/page1": {
				StatusCode: http.StatusOK,
				Body:       io.NopCloser(strings.NewReader("initial content")),
			},
		},
	}

	watchdog := NewChronoWatchdog([]string{"http://test.com/page1"}, 100*time.Millisecond, mockClient, testLogger)
	stopCh := make(chan struct{})

	go watchdog.StartMonitoring(stopCh)

	// Wait for a few checks
	time.Sleep(350 * time.Millisecond) // Should allow for 1 initial check + 3 ticks (3-4 total checks)

	close(stopCh) // Signal to stop

	output := logBuffer.String()
	initialCount := strings.Count(output, "Initial check for http://test.com/page1")
	noChangeCount := strings.Count(output, "No significant changes.")

	// Expect one initial check and at least two "no change" checks
	if initialCount != 1 {
		t.Errorf("Expected 1 initial check, got %d", initialCount)
	}
	if noChangeCount < 2 {
		t.Errorf("Expected at least 2 'no change' checks, got %d", noChangeCount)
	}
	if !strings.Contains(output, "Chrono-Watchdog stopped.") {
		t.Errorf("Expected watchdog stopped message, got:\n%s", output)
	}
}
