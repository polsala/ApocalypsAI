package main

import (
	"fmt"
	"io"
	"net"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock rationale: We need to test network operations (HTTP requests, TCP connections)
// without relying on external services or actual network availability.
// httptest provides a robust way to create an in-memory HTTP server for predictable responses.
// For TCP, we create a simple net.Listener to simulate a server that accepts/refuses connections.
// For the main function's integration test, stdout is captured to verify printed output.

func TestCheckHTTP_Success(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		_, _ = io.WriteString(w, "OK")
	}))
	defer ts.Close()

	result := checkHTTP(ts.URL, 1*time.Second)

	if result.Error != nil {
		t.Errorf("Expected no error, got %v", result.Error)
	}
	if result.Status != "Pulsing strongly!" {
		t.Errorf("Expected status 'Pulsing strongly!', got '%s'", result.Status)
	}
	if !strings.Contains(result.Message, "200 OK") {
		t.Errorf("Expected message to contain '200 OK', got '%s'", result.Message)
	}
	if result.Duration == 0 {
		t.Errorf("Expected non-zero duration")
	}
}

func TestCheckHTTP_NotFound(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		_, _ = io.WriteString(w, "Not Found")
	}))
	defer ts.Close()

	result := checkHTTP(ts.URL, 1*time.Second)

	if result.Error != nil {
		t.Errorf("Expected no error, got %v", result.Error)
	}
	if result.Status != "Faint signal..." {
		t.Errorf("Expected status 'Faint signal...', got '%s'", result.Status)
	}
	if !strings.Contains(result.Message, "404 Not Found") {
		t.Errorf("Expected message to contain '404 Not Found', got '%s'", result.Message)
	}
}

func TestCheckHTTP_Timeout(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(200 * time.Millisecond) // Longer than the test timeout
		w.WriteHeader(http.StatusOK)
	}))
	defer ts.Close()

	result := checkHTTP(ts.URL, 50*time.Millisecond) // Short timeout

	if result.Error == nil {
		t.Errorf("Expected an error for timeout, got none")
	}
	if !strings.Contains(result.Error.Error(), "timeout") && !strings.Contains(result.Error.Error(), "context deadline exceeded") {
		t.Errorf("Expected timeout error, got %v", result.Error)
	}
	if result.Status != "Flatlined!" {
		t.Errorf("Expected status 'Flatlined!', got '%s'", result.Status)
	}
}

func TestCheckTCP_Success(t *testing.T) {
	// Start a mock TCP server
	listener, err := net.Listen("tcp", "127.0.0.1:0") // Listen on a random available port
	if err != nil {
		t.Fatalf("Failed to start TCP listener: %v", err)
	}
	defer listener.Close()

	go func() {
		conn, err := listener.Accept()
		if err != nil {
			// Listener might be closed by defer, ignore error if so
			if !strings.Contains(err.Error(), "use of closed network connection") {
				t.Logf("Mock TCP server accept error: %v", err)
			}
			return
		}
		defer conn.Close()
		// Just accept and close, simulating a successful connection
	}()

	addr := listener.Addr().String()
	result := checkTCP(addr, 1*time.Second)

	if result.Error != nil {
		t.Errorf("Expected no error, got %v", result.Error)
	}
	if result.Status != "Pulsing strongly!" {
		t.Errorf("Expected status 'Pulsing strongly!', got '%s'", result.Status)
	}
	if !strings.Contains(result.Message, "Connection established") {
		t.Errorf("Expected message to contain 'Connection established', got '%s'", result.Message)
	}
	if result.Duration == 0 {
		t.Errorf("Expected non-zero duration")
	}
}

func TestCheckTCP_ConnectionRefused(t *testing.T) {
	// Choose a port that is highly unlikely to be in use and not listened to
	// This is inherently non-deterministic if a service *does* listen on it,
	// but for typical test environments, a high random port should work.
	// For better determinism, one could try to bind to a port and then close it immediately,
	// but that might still leave it in TIME_WAIT state.
	// A truly deterministic refusal would require OS-level network manipulation,
	// which is beyond a simple Go test.
	// For this context, picking a high, unused port is a reasonable mock.
	addr := "127.0.0.1:54321" // High port, unlikely to be in use

	result := checkTCP(addr, 100*time.Millisecond) // Short timeout to fail fast

	if result.Error == nil {
		t.Errorf("Expected an error for connection refused, got none")
	}
	if !strings.Contains(result.Error.Error(), "connection refused") {
		t.Errorf("Expected 'connection refused' error, got %v", result.Error)
	}
	if result.Status != "Flatlined!" {
		t.Errorf("Expected status 'Flatlined!', got '%s'", result.Status)
	}
}

func TestCheckTCP_Timeout(t *testing.T) {
	// Start a mock TCP server that accepts but then hangs
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("Failed to start TCP listener: %v", err)
	}
	defer listener.Close()

	go func() {
		conn, err := listener.Accept()
		if err != nil {
			if !strings.Contains(err.Error(), "use of closed network connection") {
				t.Logf("Mock TCP server accept error: %v", err)
			}
			return
		}
		defer conn.Close()
		time.Sleep(200 * time.Millisecond) // Hang longer than test timeout
	}()

	addr := listener.Addr().String()
	result := checkTCP(addr, 50*time.Millisecond) // Short timeout

	if result.Error == nil {
		t.Errorf("Expected an error for timeout, got none")
	}
	if !strings.Contains(result.Error.Error(), "timeout") && !strings.Contains(result.Error.Error(), "context deadline exceeded") {
		t.Errorf("Expected timeout error, got %v", result.Error)
	}
	if result.Status != "Flatlined!" {
		t.Errorf("Expected status 'Flatlined!', got '%s'", result.Status)
	}
}

func TestMonitorBeacon_UnsupportedTarget(t *testing.T) {
	var wg sync.WaitGroup
	results := make(chan BeaconResult, 1)
	wg.Add(1)

	monitorBeacon("ftp://example.com", 1*time.Second, results, &wg)
	wg.Wait()
	close(results)

	result := <-results
	if result.Error == nil {
		t.Errorf("Expected an error for unsupported target, got none")
	}
	if result.Status != "Unknown Protocol" {
		t.Errorf("Expected status 'Unknown Protocol', got '%s'", result.Status)
	}
	if !strings.Contains(result.Message, "unsupported target format") {
		t.Errorf("Expected message to contain 'unsupported target format', got '%s'", result.Message)
	}
}

func TestMainFunction_Integration(t *testing.T) {
	// This is a high-level integration test for the main function's logic.
	// It uses mock servers to ensure determinism.

	// Mock HTTP server for success
	httpSuccessServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	}))
	defer httpSuccessServer.Close()

	// Mock HTTP server for failure (404)
	httpFailServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
	}))
	defer httpFailServer.Close()

	// Mock TCP server for success
	tcpListener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("Failed to start TCP listener: %v", err)
	}
	defer tcpListener.Close()
	go func() {
		conn, err := tcpListener.Accept()
		if err != nil {
			if !strings.Contains(err.Error(), "use of closed network connection") {
				t.Logf("Mock TCP server accept error: %v", err)
			}
			return
		}
		defer conn.Close()
	}()
	tcpSuccessAddr := tcpListener.Addr().String()

	// Mock TCP server for timeout (hangs)
	tcpTimeoutListener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("Failed to start TCP timeout listener: %v", err)
	}
	defer tcpTimeoutListener.Close()
	go func() {
		conn, err := tcpTimeoutListener.Accept()
		if err != nil {
			if !strings.Contains(err.Error(), "use of closed network connection") {
				t.Logf("Mock TCP timeout server accept error: %v", err)
			}
			return
		}
		defer conn.Close()
		time.Sleep(500 * time.Millisecond) // Hang
	}()
	tcpTimeoutAddr := tcpTimeoutListener.Addr().String()

	// Simulate command-line arguments
	oldArgs := os.Args
	defer func() { os.Args = oldArgs }() // Restore original os.Args

	// Reset flags for testing main function
	flag.CommandLine = flag.NewFlagSet(os.Args[0], flag.ExitOnError)

	targets := fmt.Sprintf("%s,%s,tcp:%s,tcp:%s,invalid-target",
		httpSuccessServer.URL,
		httpFailServer.URL,
		tcpSuccessAddr,
		tcpTimeoutAddr,
	)
	timeout := "100ms" // Short timeout for tests

	// Set flags directly for testing
	_ = flag.String("targets", targets, "")
	_ = flag.String("timeout", timeout, "")
	flag.Parse()

	// Capture stdout
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Run main function
	main()

	w.Close()
	out, _ := io.ReadAll(r)
	os.Stdout = oldStdout // Restore stdout

	output := string(out)

	// Verify output contains expected messages
	if !strings.Contains(output, "Checking 5 beacons...") {
		t.Errorf("Expected 'Checking 5 beacons...' in output, got:\n%s", output)
	}
	if !strings.Contains(output, fmt.Sprintf("[HTTP] %s: Pulsing strongly! (200 OK", httpSuccessServer.URL)) {
		t.Errorf("Expected success HTTP message, got:\n%s", output)
	}
	if !strings.Contains(output, fmt.Sprintf("[HTTP] %s: Faint signal... (404 Not Found", httpFailServer.URL)) {
		t.Errorf("Expected fail HTTP message, got:\n%s", output)
	}
	if !strings.Contains(output, fmt.Sprintf("[TCP] tcp:%s: Pulsing strongly! (Connection established", tcpSuccessAddr)) {
		t.Errorf("Expected success TCP message, got:\n%s", output)
	}

	// Check for TCP timeout output
	tcpTimeoutOutputExpected := fmt.Sprintf("[TCP] tcp:%s: Flatlined!", tcpTimeoutAddr)
	if !strings.Contains(output, tcpTimeoutOutputExpected) {
		t.Errorf("Expected TCP timeout output '%s' not found. Got:\n%s", tcpTimeoutOutputExpected, output)
	}
	// Further check the error message for timeout or connection refused
	if !strings.Contains(output, "timeout") && !strings.Contains(output, "connection refused") {
		t.Errorf("Expected TCP timeout message to contain 'timeout' or 'connection refused', got:\n%s", output)
	}

	if !strings.Contains(output, "UNKNOWN] invalid-target: Unknown Protocol (Target must start with 'http://', 'https://', or 'tcp:'") {
		t.Errorf("Expected unsupported target message, got:\n%s", output)
	}
}
