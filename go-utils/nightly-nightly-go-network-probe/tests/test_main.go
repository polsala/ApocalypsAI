package main

import (
	"net"
	"testing"
	"time"
)

// MockDialer is a mock implementation of net.Dialer.
type MockDialer struct {
	DialFunc func(network, address string) (net.Conn, error)
}

func (m *MockDialer) Dial(network, address string) (net.Conn, error) {
	if m.DialFunc != nil {
		return m.DialFunc(network, address)
	}
	return nil, nil
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

// Mock rationale: Replace the global net.Dialer with our mock for deterministic testing.
// This allows us to control the outcome of network connections without actual network calls.
var originalDialer = net.Dial

func setupMockDialer(dialFunc func(network, address string) (net.Conn, error)) {
	net.Dial = func(network, address string) (net.Conn, error) {
		return (&MockDialer{DialFunc: dialFunc}).Dial(network, address)
	}
}

func restoreDialer() {
	net.Dial = originalDialer
}

func TestProbeTarget_Success(t *testing.T) {
	defer restoreDialer()

	// Mock rationale: Simulate a successful TCP connection.
	setupMockDialer(func(network, address string) (net.Conn, error) {
		// Simulate a small delay to mimic latency.
		time.Sleep(10 * time.Millisecond)
		return &MockConn{}, nil
	})

	var wg sync.WaitGroup
	results := make(chan ProbeResult, 1)

	wg.Add(1)
	go probeTarget("example.com:80", &wg, results)
	wg.Wait()
	close(results)

	result := <-results

	if result.Status != "UP" {
		t.Errorf("Expected status UP, got %s", result.Status)
	}

	if result.Error != nil {
		t.Errorf("Expected no error, got %v", result.Error)
	}

	if result.Latency < 0 {
		t.Errorf("Expected positive latency, got %s", result.Latency)
	}
}

func TestProbeTarget_Failure(t *testing.T) {
	defer restoreDialer()

	// Mock rationale: Simulate a failed TCP connection.
	setupMockDialer(func(network, address string) (net.Conn, error) {
		return nil, &net.OpError{Op: "dial", Net: "tcp", Addr: nil, Err: fmt.Errorf("connection refused")}
	})

	var wg sync.WaitGroup
	results := make(chan ProbeResult, 1)

	wg.Add(1)
	go probeTarget("nonexistent.com:8080", &wg, results)
	wg.Wait()
	close(results)

	result := <-results

	if result.Status != "DOWN" {
		t.Errorf("Expected status DOWN, got %s", result.Status)
	}

	if result.Error == nil {
		t.Errorf("Expected an error, got nil")
	}
}

func TestProbeTarget_Timeout(t *testing.T) {
	// Mock rationale: Simulate a connection timeout.
	// We don't need to restore the dialer here because the main function's timeout
	// will handle this scenario, and our mock will just return an error.
	setupMockDialer(func(network, address string) (net.Conn, error) {
		// Simulate a delay longer than the DialTimeout in probeTarget.
		time.Sleep(6 * time.Second)
		return nil, &net.OpError{Op: "dial", Net: "tcp", Addr: nil, Err: fmt.Errorf("i/o timeout")}
	})

	var wg sync.WaitGroup
	results := make(chan ProbeResult, 1)

	wg.Add(1)
	go probeTarget("slow.server.com:80", &wg, results)
	wg.Wait()
	close(results)

	result := <-results

	if result.Status != "DOWN" {
		t.Errorf("Expected status DOWN on timeout, got %s", result.Status)
	}

	if result.Error == nil {
		t.Errorf("Expected an error on timeout, got nil")
	}

	// The latency measurement might be slightly off due to the sleep, but the status should be DOWN.
}
