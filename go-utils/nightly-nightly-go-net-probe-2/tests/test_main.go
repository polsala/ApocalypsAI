package main

import (
	"net"
	"testing"
	"time"
)

// MockDialer is a mock implementation of net.Dialer
type MockDialer struct {
	ShouldError bool
	Delay       time.Duration
}

// Dial implements the net.Dialer interface for the mock
func (m *MockDialer) Dial(network, address string) (net.Conn, error) {
	if m.ShouldError {
		return nil, fmt.Errorf("mock dial error")
	}
	// Mock a successful connection with a delay
	return &MockConn{Delay: m.Delay},
		nil
}

// MockConn is a mock implementation of net.Conn
type MockConn struct {
	Delay time.Duration
}

// Read implements net.Conn Read
func (mc *MockConn) Read(b []byte) (n int, err error) { time.Sleep(mc.Delay); return 0, nil }
// Write implements net.Conn Write
func (mc *MockConn) Write(b []byte) (n int, err error) { time.Sleep(mc.Delay); return 0, nil }
// Close implements net.Conn Close
func (mc *MockConn) Close() error { return nil }
// LocalAddr implements net.Conn LocalAddr
func (mc *MockConn) LocalAddr() net.Addr { return nil }
// RemoteAddr implements net.Conn RemoteAddr
func (mc *MockConn) RemoteAddr() net.Addr { return nil }
// SetDeadline implements net.Conn SetDeadline
func (mc *MockConn) SetDeadline(t time.Time) error { return nil }
// SetReadDeadline implements net.Conn SetReadDeadline
func (mc *MockConn) SetReadDeadline(t time.Time) error { return nil }
// SetWriteDeadline implements net.Conn SetWriteDeadline
func (mc *MockConn) SetWriteDeadline(t time.Time) error { return nil }

// Mock rationale: This mock replaces the actual network dialing to allow for deterministic testing.
// We can control whether the dial succeeds or fails, and simulate network latency.
var originalDialTimeout func(network, address string, timeout time.Duration) (net.Conn, error)

func setupMockDialer(shouldError bool, delay time.Duration) {
	originalDialTimeout = net.DialTimeout
	net.DialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		mockDialer := &MockDialer{ShouldError: shouldError, Delay: delay}
		return mockDialer.Dial(network, address)
	}
}

func restoreDialer() {
	net.DialTimeout = originalDialTimeout
}

func TestProbeEndpoint_Success(t *testing.T) {
	setupMockDialer(false, 50*time.Millisecond) // Mock success with 50ms delay
	defer restoreDialer()

	var wg sync.WaitGroup
	results := make(chan string, 1)

	wg.Add(1)
	go probeEndpoint("test.com:80", &wg, results)
	wg.Wait()
	close(results)

	result := <-results
	expectedPrefix := "Probing test.com:80... Reachable (Latency: "
	if !strings.HasPrefix(result, expectedPrefix) {
		t.Errorf("Expected result to start with '%s', but got '%s'", expectedPrefix, result)
	}
	// Basic check for latency format, actual value will vary slightly due to mock timing
	if !strings.Contains(result, "ms)") {
		t.Errorf("Expected latency in ms, but got '%s'", result)
	}
}

func TestProbeEndpoint_Failure(t *testing.T) {
	setupMockDialer(true, 0) // Mock failure
	defer restoreDialer()

	var wg sync.WaitGroup
	results := make(chan string, 1)

	wg.Add(1)
	go probeEndpoint("unreachable.com:80", &wg, results)
	wg.Wait()
	close(results)

	result := <-results
	expected := "Probing unreachable.com:80... Unreachable (mock dial error)"
	if result != expected {
		t.Errorf("Expected '%s', but got '%s'", expected, result)
	}
}

func TestMain_NoArgs(t *testing.T) {
	// Mock os.Args to simulate no arguments being passed
	originalArgs := os.Args
	os.Args = []string{originalArgs[0]} // Only the program name
	defer func() { os.Args = originalArgs }()

	// Capture stdout to check for usage message
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Expecting os.Exit to be called, so we use a defer to recover from panic
	defer func() {
		if r := recover(); r != nil {
			// Check if the panic was due to os.Exit
			if exitCode, ok := r.(int); ok && exitCode == 1 {
				// Successfully recovered from os.Exit(1)
			} else {
				t.Errorf("Unexpected panic: %v", r)
			}
		}
		os.Stdout = oldStdout // Restore stdout
	}()

	main() // This should call os.Exit(1)

	w.Close()
	output, _ := io.ReadAll(r)

	if !strings.Contains(string(output), "Usage:") {
		t.Errorf("Expected usage message, but got:\n%s", string(output))
	}
}
