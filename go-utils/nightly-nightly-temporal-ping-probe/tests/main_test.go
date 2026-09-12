package main

import (
	"bytes"
	"errors"
	"io"
	"net"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// MockConn implements net.Conn for testing purposes.
// Only Close() is actively used by probeHost, so other methods are stubs.
type MockConn struct {
	closed   bool
	mu       sync.Mutex
}

// Mock rationale: These methods are not called by probeHost, so they are stubbed to satisfy the net.Conn interface.
func (mc *MockConn) Read(b []byte) (n int, err error)         { return 0, io.EOF }
func (mc *MockConn) Write(b []byte) (n int, err error)        { return 0, nil }
func (mc *MockConn) LocalAddr() net.Addr                      { return nil }
func (mc *MockConn) RemoteAddr() net.Addr                     { return nil }
func (mc *MockConn) SetDeadline(t time.Time) error            { return nil }
func (mc *MockConn) SetReadDeadline(t time.Time) error        { return nil }
func (mc *MockConn) SetWriteDeadline(t time.Time) error       { return nil }

func (mc *MockConn) Close() error {
	mc.mu.Lock()
	defer mc.mu.Unlock()
	mc.closed = true
	return nil
}

func (mc *MockConn) IsClosed() bool {
	mc.mu.Lock()
	defer mc.mu.Unlock()
	return mc.closed
}

// MockDialer implements Dialer interface for testing.
type MockDialer struct {
	// Mock rationale: Simulates network responses for deterministic testing without actual network calls.
	// Map of address (host:port) to a function that returns (net.Conn, error, duration).
	responses map[string]func() (net.Conn, error, time.Duration)
}

func (md *MockDialer) DialTimeout(network, address string, timeout time.Duration) (net.Conn, error) {
	if respFunc, ok := md.responses[address]; ok {
		conn, err, duration := respFunc()
		// Mock rationale: Simulate network latency for realistic test results.
		time.Sleep(duration)
		return conn, err
	}
	// Default to connection refused if not explicitly mocked.
	return nil, errors.New("connection refused (mocked)"), 0
}

func TestProbeHost_Success(t *testing.T) {
	mockConn := &MockConn{}
	mockDialer := &MockDialer{
		responses: map[string]func() (net.Conn, error, time.Duration){
			"example.com:80": func() (net.Conn, error, time.Duration) {
				return mockConn, nil, 10 * time.Millisecond
			},
		},
	}
	result := probeHost(mockDialer, "example.com", 80, 1*time.Second)

	if !result.Reachable {
		t.Errorf("Expected host to be reachable, got unreachable. Error: %v", result.Error)
	}
	if result.Latency == 0 {
		t.Errorf("Expected non-zero latency, got %v", result.Latency)
	}
	if result.Error != nil {
		t.Errorf("Expected no error, got %v", result.Error)
	}
	if result.Timestamp.IsZero() {
		t.Errorf("Expected timestamp to be set, got zero")
	}
	// Mock rationale: Verify that the mock connection was closed as expected by the probeHost function.
	if !mockConn.IsClosed() {
		t.Errorf("Expected mock connection to be closed")
	}
}

func TestProbeHost_Failure(t *testing.T) {
	mockDialer := &MockDialer{
		responses: map[string]func() (net.Conn, error, time.Duration){
			"nonexistent.com:80": func() (net.Conn, error, time.Duration) {
				return nil, errors.New("connection refused"), 0
			},
		},
	}
	result := probeHost(mockDialer, "nonexistent.com", 80, 1*time.Second)

	if result.Reachable {
		t.Errorf("Expected host to be unreachable, got reachable")
	}
	if result.Error == nil {
		t.Errorf("Expected an error, got nil")
	}
	if result.Timestamp.IsZero() {
		t.Errorf("Expected timestamp to be set, got zero")
	}
}

func TestRunProbes_MultipleHosts(t *testing.T) {
	mockDialer := &MockDialer{
		responses: map[string]func() (net.Conn, error, time.Duration){
			"host1.com:80": func() (net.Conn, error, time.Duration) { return &MockConn{}, nil, 5 * time.Millisecond },
			"host2.com:80": func() (net.Conn, error, time.Duration) { return nil, errors.New("timeout"), 0 },
			"host3.com:80": func() (net.Conn, error, time.Duration) { return &MockConn{}, nil, 15 * time.Millisecond },
		},
	}
	hosts := []string{"host1.com", "host2.com", "host3.com"}
	results := runProbes(mockDialer, hosts, 80, 1*time.Second)

	if len(results) != 3 {
		t.Fatalf("Expected 3 results, got %d", len(results))
	}

	// Check specific results
	foundHost1 := false
	foundHost2 := false
	foundHost3 := false
	for _, r := range results {
		switch r.Host {
		case "host1.com":
			foundHost1 = true
			if !r.Reachable || r.Error != nil {
				t.Errorf("host1.com: Expected reachable, no error. Got reachable=%t, error=%v", r.Reachable, r.Error)
			}
		case "host2.com":
			foundHost2 = true
			if r.Reachable || r.Error == nil {
				t.Errorf("host2.com: Expected unreachable, error. Got reachable=%t, error=%v", r.Reachable, r.Error)
			}
		case "host3.com":
			foundHost3 = true
			if !r.Reachable || r.Error != nil {
				t.Errorf("host3.com: Expected reachable, no error. Got reachable=%t, error=%v", r.Reachable, r.Error)
			}
		}
	}
	if !foundHost1 || !foundHost2 || !foundHost3 {
		t.Errorf("Not all hosts processed. Found host1: %t, host2: %t, host3: %t", foundHost1, foundHost2, foundHost3)
	}
}

// captureStdout is a helper function to capture os.Stdout for testing output.
func captureStdout(f func()) string {
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	f()

	w.Close()
	os.Stdout = old
	var buf bytes.Buffer
	io.Copy(&buf, r)
	return buf.String()
}

func TestMainFunction_SuccessOutput(t *testing.T) {
	// Mock rationale: Replace the real dialer with a mock for deterministic testing of main's output.
	originalDialer := currentDialer // Store original
	defer func() { currentDialer = originalDialer }() // Restore original after test

	mockDialer := &MockDialer{
		responses: map[string]func() (net.Conn, error, time.Duration){
			"mockhost1.com:80": func() (net.Conn, error, time.Duration) { return &MockConn{}, nil, 10 * time.Millisecond },
			"mockhost2.com:80": func() (net.Conn, error, time.Duration) { return nil, errors.New("mock timeout"), 0 },
		},
	}
	currentDialer = mockDialer // Assign mock dialer to the global variable used by main

	// Mock rationale: Capture os.Args for deterministic testing of command-line parsing.
	oldArgs := os.Args
	defer func() { os.Args = oldArgs }()
	os.Args = []string{"nightly-temporal-ping-probe", "80", "mockhost1.com", "mockhost2.com"}

	// Mock rationale: Capture stdout for deterministic testing of output format.
	output := captureStdout(func() {
		main()
	})

	if !strings.Contains(output, "Host: mockhost1.com:80 | Status: REACHABLE | Latency:") {
		t.Errorf("Output missing expected reachable host: %s", output)
	}
	if !strings.Contains(output, "Host: mockhost2.com:80 | Status: UNREACHABLE | Latency: N/A") {
		t.Errorf("Output missing expected unreachable host: %s", output)
	}
	if !strings.Contains(output, "Timestamp:") {
		t.Errorf("Output missing timestamp: %s", output)
	}
}

func TestMainFunction_InvalidPort(t *testing.T) {
	// Mock rationale: Capture os.Args for deterministic testing of command-line parsing.
	oldArgs := os.Args
	defer func() { os.Args = oldArgs }()
	os.Args = []string{"nightly-temporal-ping-probe", "invalid", "host.com"}

	// Mock rationale: Capture stderr for deterministic testing of error messages.
	oldStderr := os.Stderr
	r, w, _ := os.Pipe()
	os.Stderr = w
	exitCode := 0
	originalOsExit := osExit
	defer func() {
		os.Stderr = oldStderr
		osExit = originalOsExit
	}()
	// Mock rationale: Intercept os.Exit to prevent the test from terminating prematurely.
	osExit = func(code int) { exitCode = code }

	captureStdout(func() { // Capture stdout to prevent it from printing to console
		main()
	})
	w.Close()
	var buf bytes.Buffer
	io.Copy(&buf, r)
	stderrOutput := buf.String()

	if !strings.Contains(stderrOutput, "Invalid port: invalid") {
		t.Errorf("Expected invalid port error, got: %s", stderrOutput)
	}
	if exitCode != 1 {
		t.Errorf("Expected exit code 1 for invalid port, got %d", exitCode)
	}
}

func TestMainFunction_NoArguments(t *testing.T) {
	// Mock rationale: Capture os.Args for deterministic testing of command-line parsing.
	oldArgs := os.Args
	defer func() { os.Args = oldArgs }()
	os.Args = []string{"nightly-temporal-ping-probe"}

	// Mock rationale: Capture stderr for deterministic testing of error messages.
	oldStderr := os.Stderr
	r, w, _ := os.Pipe()
	os.Stderr = w
	exitCode := 0
	originalOsExit := osExit
	defer func() {
		os.Stderr = oldStderr
		osExit = originalOsExit
	}()
	// Mock rationale: Intercept os.Exit to prevent the test from terminating prematurely.
	osExit = func(code int) { exitCode = code }

	captureStdout(func() {
		main()
	})
	w.Close()
	var buf bytes.Buffer
	io.Copy(&buf, r)
	stderrOutput := buf.String()

	if !strings.Contains(stderrOutput, "Usage: nightly-temporal-ping-probe <port> <host1> [host2...]") {
		t.Errorf("Expected usage message, got: %s", stderrOutput)
	}
	if exitCode != 1 {
		t.Errorf("Expected exit code 1 for no arguments, got %d", exitCode)
	}
}
