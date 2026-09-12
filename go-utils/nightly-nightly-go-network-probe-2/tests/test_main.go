package main

import (
	"net"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

// Mock rationale: These tests mock the HTTP server and use a simple TCP listener
// to simulate network responses without requiring actual network connectivity.
// This ensures deterministic and offline test execution.

func TestProbeEndpoint_SuccessHTTP(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	}))
	defer server.Close()

	result := probeEndpoint(server.URL, 5*time.Second)

	if !result.Success {
		t.Errorf("Expected success for %s, but got failure: %s", server.URL, result.Error)
	}
	if result.Latency == 0 {
		t.Errorf("Expected non-zero latency for %s, but got 0", server.URL)
	}
}

func TestProbeEndpoint_FailureHTTP(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Simulate a server that immediately closes the connection
		w.WriteHeader(http.StatusInternalServerError)
	}))
	defer server.Close()

	// To simulate a connection error, we'll try to probe a non-existent port on the server's host
	// This is a bit of a hack, but it simulates a dial error.
	// A more robust mock would involve mocking net.Dial directly, but this is simpler for demonstration.
	// For this test, we'll rely on the fact that if the server is down or unreachable, it will fail.
	// Let's simulate a failure by using a port that's unlikely to be open.
	// The actual probeEndpoint function will try to dial the server's host and port.
	// If the server is not responding as expected, it should fail.

	// Let's try to probe a different, likely unavailable port on the same host.
	// This is to simulate a dial error, not an HTTP error response.
	// The probeEndpoint function handles both URL parsing and dialing.
	// If the URL is valid but the dial fails, it should report an error.

	// A better approach for simulating a dial failure is to use a known unavailable port.
	// However, httptest.NewServer provides a URL that *should* be reachable.
	// Let's focus on simulating a scenario where the dial itself fails.

	// We'll use a very short timeout to ensure the test doesn't hang if the mock behaves unexpectedly.
	result := probeEndpoint(server.URL+":9999", 1*time.Millisecond) // Probe a non-existent port on the server's host

	if result.Success {
		t.Errorf("Expected failure for %s, but got success", server.URL+":9999")
	}
	if result.Error == "" {
		t.Errorf("Expected an error message for failure, but got none for %s", server.URL+":9999")
	}
}

func TestProbeEndpoint_SuccessTCP(t *testing.T) {
	listener, err := net.Listen("tcp", "127.0.0.1:0") // Listen on a random available port
	if err != nil {
		t.Fatalf("Failed to start mock TCP listener: %v", err)
	}
	defer listener.Close()

	go func() {
		conn, _ := listener.Accept()
		if conn != nil {
			conn.Close()
		}
	}()

	addr := listener.Addr().String()
	result := probeEndpoint(addr, 5*time.Second)

	if !result.Success {
		t.Errorf("Expected success for TCP endpoint %s, but got failure: %s", addr, result.Error)
	}
	if result.Latency == 0 {
		t.Errorf("Expected non-zero latency for TCP endpoint %s, but got 0", addr)
	}
}

func TestProbeEndpoint_FailureTCP(t *testing.T) {
	// Attempt to probe a port that is unlikely to be open
	addr := "127.0.0.1:65535"
	result := probeEndpoint(addr, 1*time.Second)

	if result.Success {
		t.Errorf("Expected failure for TCP endpoint %s, but got success", addr)
	}
	if result.Error == "" {
		t.Errorf("Expected an error message for failure, but got none for %s", addr)
	}
}

func TestProbeEndpoint_InvalidURL(t *testing.T) {
	result := probeEndpoint(":invalid-url", 5*time.Second)
	if result.Success {
		t.Errorf("Expected failure for invalid URL, but got success")
	}
	if !strings.Contains(result.Error, "invalid URL") {
		t.Errorf("Expected 'invalid URL' in error message, but got: %s", result.Error)
	}
}

func TestMainFunction(t *testing.T) {
	// This test primarily checks if the main function can be executed without panicking
	// and if it handles no arguments gracefully.

	// Save original os.Args and defer restore
	originalArgs := os.Args
	defer func() { os.Args = originalArgs }

	// Test with no arguments
	os.Args = []string{"network-probe"}
	// Redirect stdout to capture output
	oldStdout := os.Stdout
	// Create a pipe to capture stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	main()

	w.Close()
	
	// Restore stdout
	os.Stdout = oldStdout

	// We expect an exit code of 1 and a usage message when no arguments are provided.
	// Capturing exit codes directly in Go tests is tricky without external libraries or more complex setups.
	// For simplicity, we'll check for the usage message in stdout.

	output, _ := io.ReadAll(r)
	if !strings.Contains(string(output), "Usage:") {
		t.Errorf("Expected usage message when no arguments are provided, but got: %s", string(output))
	}
}

// Helper to simulate reading from a pipe for TestMainFunction
import "io"
