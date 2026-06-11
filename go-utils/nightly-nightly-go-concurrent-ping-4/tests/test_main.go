package main

import (
	"net"
	"testing"
	"time"
	"errors"
)

// MockDialer is a mock implementation of net.Dialer.
type MockDialer struct {
	DialFunc func(network, address string) (net.Conn, error)
}

func (m *MockDialer) Dial(network, address string) (net.Conn, error) {
	if m.DialFunc != nil {
		return m.DialFunc(network, address)
	}
	return nil, errors.New("MockDialer: DialFunc not set")
}

// MockConn is a mock implementation of net.Conn.
type MockConn struct {}

func (m *MockConn) Read(b []byte) (n int, err error) { return 0, nil }
func (m *MockConn) Write(b []byte) (n int, err error) { return 0, nil }
func (m *MockConn) Close() error { return nil }
func (m *MockConn) LocalAddr() net.Addr { return nil }
func (m *MockConn) RemoteAddr() net.Addr { return nil }
func (m *MockConn) SetDeadline(t time.Time) error { return nil }
func (m *MockConn) SetReadDeadline(t time.Time) error { return nil }
func (m *MockConn) SetWriteDeadline(t time.Time) error { return nil }

// Mock net.DialTimeout to use our MockDialer.
// Mock rationale: This allows us to control the network behavior for testing without actual network calls.
var mockDialTimeout func(network, address string, timeout time.Duration) (net.Conn, error)

func init() {
	// Replace the actual net.DialTimeout with our mock.
	originalDialTimeout := net.DialTimeout
	net.DialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		if mockDialTimeout != nil {
			return mockDialTimeout(network, address, timeout)
		}
		return originalDialTimeout(network, address, timeout) // Fallback to real if mock not set
	}
}

func TestPingHost_Success(t *testing.T) {
	// Mock rationale: Simulate a successful connection.
	mockDialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return &MockConn{}, nil
	}

	status := pingHost("example.com", 1*time.Second)

	if status.Error != nil {
		t.Errorf("Expected no error, but got: %v", status.Error)
	}
	if !status.IsUp {
		t.Error("Expected host to be UP, but it was reported DOWN")
	}
	if status.Latency == 0 {
		t.Error("Expected non-zero latency, but got 0")
	}
}

func TestPingHost_Timeout(t *testing.T) {
	// Mock rationale: Simulate a timeout by returning a timeout error.
	mockDialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return nil, net.ErrDeadlineExceeded
	}

	status := pingHost("timeout.host", 500*time.Millisecond)

	if status.Error == nil {
		t.Error("Expected a timeout error, but got nil")
	}
	if status.IsUp {
		t.Error("Expected host to be DOWN due to timeout, but it was reported UP")
	}
}

func TestPingHost_NetworkError(t *testing.T) {
	// Mock rationale: Simulate a general network error.
	mockDialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return nil, errors.New("simulated network error")
	}

	status := pingHost("error.host", 1*time.Second)

	if status.Error == nil {
		t.Error("Expected a network error, but got nil")
	}
	if status.IsUp {
		t.Error("Expected host to be DOWN due to error, but it was reported UP")
	}
}

func TestMain_NoHosts(t *testing.T) {
	// Mock rationale: Ensure the program exits gracefully when no hosts are provided.
	// We'll capture os.Exit calls to verify.
	exitCalled := false
	originalExit := os.Exit
	os.Exit = func(code int) {
		exitCalled = true
		// Don't actually exit during test
	}
	defer func() { os.Exit = originalExit }()

	// Temporarily clear command-line arguments to simulate no hosts.
	originalArgs := os.Args
	os.Args = []string{os.Args[0]}
	defer func() { os.Args = originalArgs }()

	main()

	if !exitCalled {
		t.Error("Expected os.Exit to be called when no hosts are provided, but it was not")
	}
}
