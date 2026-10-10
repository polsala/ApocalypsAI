package main_test

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	main "nightly-chrono-ping-dispatcher/src" // Import the main package
)

// TestPingURLSuccess tests a successful HTTP GET request.
func TestPingURLSuccess(t *testing.T) {
	// # Mock rationale: httptest.NewServer is used to create a local, deterministic HTTP server,
	// avoiding external network calls and ensuring test isolation.
	tc := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "OK")
	}))
	defer tc.Close()

	result := main.PingURL(tc.URL, 5*time.Second)

	if result.Error != nil {
		t.Errorf("Expected no error, got: %v", result.Error)
	}
	if result.StatusCode != http.StatusOK {
		t.Errorf("Expected status %d, got %d", http.StatusOK, result.StatusCode)
	}
	if result.Latency <= 0 {
		t.Errorf("Expected positive latency, got %s", result.Latency)
	}
	if result.URL != tc.URL {
		t.Errorf("Expected URL %s, got %s", tc.URL, result.URL)
	}
}

// TestPingURLNotFound tests an HTTP GET request resulting in a 404.
func TestPingURLNotFound(t *testing.T) {
	// # Mock rationale: httptest.NewServer is used to simulate a server responding with a 404,
	// ensuring deterministic error handling for non-2xx responses.
	tnfs := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		fmt.Fprintln(w, "Not Found")
	}))
	defer tnfs.Close()

	result := main.PingURL(tnfs.URL, 5*time.Second)

	if result.Error != nil {
		t.Errorf("Expected no error, got: %v", result.Error)
	}
	if result.StatusCode != http.StatusNotFound {
		t.Errorf("Expected status %d, got %d", http.StatusNotFound, result.StatusCode)
	}
	if result.Latency <= 0 {
		t.Errorf("Expected positive latency, got %s", result.Latency)
	}
}

// TestPingURLTimeout tests an HTTP GET request that times out.
func TestPingURLTimeout(t *testing.T) {
	// # Mock rationale: httptest.NewServer is used to simulate a slow server that exceeds the timeout,
	// ensuring deterministic timeout handling without relying on actual network conditions.
	timeoutServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(200 * time.Millisecond) // Simulate a slow response
		// We don't write anything back, so the client will time out
	}))
	defer timeoutServer.Close()

	// Use a timeout shorter than the server's delay
	timeoutDuration := 50 * time.Millisecond
	result := main.PingURL(timeoutServer.URL, timeoutDuration)

	if result.Error == nil {
		t.Errorf("Expected a timeout error, got nil")
	}
	// Check for common timeout error messages
	if !strings.Contains(result.Error.Error(), "timeout") && !strings.Contains(result.Error.Error(), "context deadline exceeded") {
		t.Errorf("Expected timeout error message, got: %v", result.Error)
	}
	// Status code should be 0 on timeout because no response was received
	if result.StatusCode != 0 {
		t.Errorf("Expected status code 0 on timeout, got %d", result.StatusCode)
	}
	// Latency should be approximately the timeout duration. Allow some buffer.
	if result.Latency < timeoutDuration || result.Latency > timeoutDuration*2 {
		t.Errorf("Expected latency around %s, got %s", timeoutDuration, result.Latency)
	}
}

// TestPingURLInvalid tests an HTTP GET request with an invalid URL.
func TestPingURLInvalid(t *testing.T) {
	// # Mock rationale: Directly testing with an invalid URL string to ensure the `http.Get` error handling
	// path is covered without needing a network call or a mock server.
	invalidURL := "invalid-url-format"
	result := main.PingURL(invalidURL, 5*time.Second)

	if result.Error == nil {
		t.Errorf("Expected an error for invalid URL, got nil")
	}
	// Check for common invalid URL error messages
	if !strings.Contains(result.Error.Error(), "unsupported protocol scheme") && !strings.Contains(result.Error.Error(), "no such host") {
		t.Errorf("Expected 'unsupported protocol scheme' or 'no such host' error, got: %v", result.Error)
	}
	if result.URL != invalidURL {
		t.Errorf("Expected URL %s, got %s", invalidURL, result.URL)
	}
}
