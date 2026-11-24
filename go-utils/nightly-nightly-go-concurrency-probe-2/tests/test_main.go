package main

import (
	"net"
	"testing"
	"time"
	"net/http"
	"net/http/httptest"
	"os/exec"
	"runtime"
	"strings"
)

// Mock rationale: We are mocking the net.DialTimeout function to simulate network responses
// without actually making network calls. This ensures deterministic and offline tests.
var mockDialTimeout func(network, address string, timeout time.Duration) (net.Conn, error)

// MockConn is a dummy net.Conn implementation for testing.
type MockConn struct{}`

func (m MockConn) Read(b []byte) (n int, err error) { return 0, nil }
func (m MockConn) Write(b []byte) (n int, err error) { return 0, nil }
func (m MockConn) Close() error { return nil }
func (m MockConn) LocalAddr() net.Addr { return nil }
func (m MockConn) RemoteAddr() net.Addr { return nil }
func (m MockConn) SetDeadline(t time.Time) error { return nil }
func (m MockConn) SetReadDeadline(t time.Time) error { return nil }
func (m MockConn) SetWriteDeadline(t time.Time) error { return nil }

// Override net.DialTimeout with our mock
func init() {
	// This is a simplified approach. In a real-world scenario, you might use a
	// more sophisticated mocking library or technique.
	// For this example, we'll rely on a global variable that can be set by tests.
	// However, Go's standard library doesn't easily allow replacing built-in functions like DialTimeout directly.
	// A common pattern is to pass the dialing function as a parameter.
	// For this exercise, we'll simulate the effect by having tests control the outcome.
	// In a production Go project, you'd refactor `probeService` to accept a `dialer` function.

	// Since we can't directly mock `net.DialTimeout` easily without refactoring `probeService` to accept a dialer, 
	// we'll test the `probeService` function directly by controlling its behavior through a test helper.
	// The main function will be tested by running the compiled binary and capturing its output.
}

// TestProbeService_Success tests a successful connection.
func TestProbeService_Success(t *testing.T) {
	// Mock net.DialTimeout to return a successful connection.
	originalDialTimeout := net.DialTimeout
	defer func() { net.DialTimeout = originalDialTimeout }() // Restore original

	net.DialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return MockConn{}, nil // Simulate a successful connection
	}

	if !probeService("localhost:8080", 1*time.Second) {
		t.Errorf("probeService should return true for a successful connection")
	}
}

// TestProbeService_Failure tests a failed connection.
func TestProbeService_Failure(t *testing.T) {
	// Mock net.DialTimeout to return an error.
	originalDialTimeout := net.DialTimeout
	defer func() { net.DialTimeout = originalDialTimeout }() // Restore original

	net.DialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return nil, fmt.Errorf("connection refused") // Simulate a failed connection
	}

	if probeService("localhost:9999", 1*time.Second) {
		t.Errorf("probeService should return false for a failed connection")
	}
}

// TestMainFunction_Output tests the output of the main function.
// This test compiles and runs the binary, then checks its stdout.
func TestMainFunction_Output(t *testing.T) {
	// Create a dummy server to simulate a reachable service
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(200)
	}))
	defer server.Close()

	// Extract the port from the dummy server's URL
	serverAddr := strings.TrimPrefix(server.URL, "http://")

	// Create a dummy unreachable address
	unreachableAddr := "localhost:9999"

	// Build the Go program
	buildCmd := exec.Command("go", "build", "-o", "concurrency_probe", "../src/main.go")
	if runtime.GOOS == "windows" {
		buildCmd.Path = "go.exe"
	}
	buildCmd.Dir = "../"
	_, err := buildCmd.CombinedOutput()
	if err != nil {
		t.Fatalf("Failed to build Go program: %v", err)
	}

	// Run the compiled program with test arguments
	// We need to pass the server address and an unreachable address
	runCmd := exec.Command("./concurrency_probe", serverAddr, unreachableAddr)
	if runtime.GOOS == "windows" {
		runCmd.Path = ".\concurrency_probe.exe"
	}

	out, err := runCmd.CombinedOutput()
	if err != nil {
		// It's okay if the command exits with an error if it's due to the program's logic (e.g., no args)
		// but for this test, we expect it to run and produce output.
		t.Logf("Command output (may contain errors if expected): %s", string(out))
		t.Fatalf("Failed to run Go program: %v", err)
	}

	output := string(out)

	// Check if the output contains the expected status messages
	if !strings.Contains(output, "Service "+serverAddr+" is UP") {
		t.Errorf("Expected output to contain 'Service %s is UP', but got:\n%s", serverAddr, output)
	}

	if !strings.Contains(output, "Service "+unreachableAddr+" is DOWN") {
		t.Errorf("Expected output to contain 'Service %s is DOWN', but got:\n%s", unreachableAddr, output)
	}
}
