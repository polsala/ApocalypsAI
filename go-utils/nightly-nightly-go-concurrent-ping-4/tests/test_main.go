package main

import (
	"context"
	"net"
	"testing"
	"time"
	"sync"
	"fmt"
)

// MockDialer is a mock for net.Dialer
type MockDialer struct {
	DialFunc func(network, address string) (net.Conn, error)
}

func (m *MockDialer) Dial(network, address string) (net.Conn, error) {
	if m.DialFunc != nil {
		return m.DialFunc(network, address)
	}
	return nil, fmt.Errorf("MockDialer: DialFunc not set")
}

// MockConn is a mock for net.Conn
type MockConn struct {}

func (m *MockConn) Read(b []byte) (n int, err error) { return 0, fmt.Errorf("MockConn: Read not implemented") }
func (m *MockConn) Write(b []byte) (n int, err error) { return 0, fmt.Errorf("MockConn: Write not implemented") }
func (m *MockConn) Close() error { return nil }
func (m *MockConn) LocalAddr() net.Addr { return nil }
func (m *MockConn) RemoteAddr() net.Addr { return nil }
func (m *MockConn) SetDeadline(t time.Time) error { return nil }
func (m *MockConn) SetReadDeadline(t time.Time) error { return nil }
func (m *MockConn) SetWriteDeadline(t time.Time) error { return nil }

// Mock net.DialTimeout to control behavior
var mockDialTimeout func(network, address string, timeout time.Duration) (net.Conn, error)

func init() {
	// Replace the actual net.DialTimeout with our mock for testing
	originalDialTimeout := net.DialTimeout
	net.DialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		if mockDialTimeout != nil {
			return mockDialTimeout(network, address, timeout)
		}
		return originalDialTimeout(network, address, timeout) // Fallback to real if not mocked
	}
}

func TestPingHost_Reachable(t *testing.T) {
	// Mock rationale: Simulate a successful TCP connection.
	mockDialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return &MockConn{}, nil
	}

	var wg sync.WaitGroup
	results := make(chan string, 1)
	ctx := context.Background()

	wg.Add(1)
	go pingHost(ctx, "example.com", results, &wg)
	wg.Wait()
	close(results)

	result := <-results
	if !strings.Contains(result, "Reachable") {
		t.Errorf("Expected 'Reachable', got '%s'", result)
	}

	// Reset mock
	mockDialTimeout = nil
}

func TestPingHost_Unreachable(t *testing.T) {
	// Mock rationale: Simulate a failed TCP connection.
	mockDialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return nil, fmt.Errorf("connection refused")
	}

	var wg sync.WaitGroup
	results := make(chan string, 1)
	ctx := context.Background()

	wg.Add(1)
	go pingHost(ctx, "nonexistent.local", results, &wg)
	wg.Wait()
	close(results)

	result := <-results
	if !strings.Contains(result, "Unreachable") {
		t.Errorf("Expected 'Unreachable', got '%s'", result)
	}

	// Reset mock
	mockDialTimeout = nil
}

func TestPingHost_Timeout(t *testing.T) {
	// Mock rationale: Simulate a connection that takes too long, triggering context timeout.
	mockDialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		// Simulate a delay longer than the context timeout
		time.Sleep(2 * time.Second)
		return &MockConn{}, nil
	}

	var wg sync.WaitGroup
	results := make(chan string, 1)
	// Use a short context timeout to trigger the test
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()

	wg.Add(1)
	go pingHost(ctx, "slow.host.com", results, &wg)
	wg.Wait()
	close(results)

	result := <-results
	if !strings.Contains(result, "Timed out") {
		t.Errorf("Expected 'Timed out', got '%s'", result)
	}

	// Reset mock
	mockDialTimeout = nil
}

// Helper function to check if a string contains another string
func strings.Contains(s, substr string) bool {
	return len(s) >= len(substr) && s[0:len(substr)] == substr
}
