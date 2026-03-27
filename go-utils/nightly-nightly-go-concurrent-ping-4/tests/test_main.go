package main

import (
	"net"
	"testing"
	"time"
)

// MockDialer is a mock implementation of net.Dialer.
type MockDialer struct {
	DialFn func(network, address string) (net.Conn, error)
}

func (m *MockDialer) Dial(network, address string) (net.Conn, error) {
	if m.DialFn != nil {
		return m.DialFn(network, address)
	}
	return nil, nil // Default to no error if DialFn is not set
}

// MockConn is a mock implementation of net.Conn.
type MockConn struct {}

func (mc *MockConn) Read(b []byte) (n int, err error) { return 0, nil }
func (mc *MockConn) Write(b []byte) (n int, err error) { return 0, nil }
func (mc *MockConn) Close() error { return nil }
func (mc *MockConn) LocalAddr() net.Addr { return nil }
func (mc *MockConn) RemoteAddr() net.Addr { return nil }
func (mc *MockConn) SetDeadline(t time.Time) error { return nil }
func (mc *MockConn) SetReadDeadline(t time.Time) error { return nil }
func (mc *MockConn) SetWriteDeadline(t time.Time) error { return nil }

func TestPingHost_Reachable(t *testing.T) {
	// Mock rationale: We are mocking net.DialTimeout to simulate a successful connection.
	// This allows us to test the Reachable logic without actual network calls.
	originalDialTimeout := netDialTimeout
	defer func() { netDialTimeout = originalDialTimeout }()

	netDialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return &MockConn{}, nil // Simulate a successful connection
	}

	host := "test.example.com"
	timeout := 500 * time.Millisecond

	status := pingHost(host, timeout)

	if !status.Reachable {
		t.Errorf("Expected host %s to be reachable, but it was not.", host)
	}
	if status.Error != nil {
		t.Errorf("Expected no error for reachable host %s, but got: %v", host, status.Error)
	}
}

func TestPingHost_Unreachable(t *testing.T) {
	// Mock rationale: We are mocking net.DialTimeout to simulate a connection error.
	// This allows us to test the Unreachable logic without actual network calls.
	originalDialTimeout := netDialTimeout
	defer func() { netDialTimeout = originalDialTimeout }()

	mockErr := &net.OpError{Op: "dial", Net: "tcp", Addr: nil, Err: "connection refused"}
	netDialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return nil, mockErr // Simulate a connection error
	}

	host := "unreachable.example.com"
	timeout := 500 * time.Millisecond

	status := pingHost(host, timeout)

	if status.Reachable {
		t.Errorf("Expected host %s to be unreachable, but it was reachable.", host)
	}
	if status.Error == nil {
		t.Errorf("Expected an error for unreachable host %s, but got none.", host)
	}
	if status.Error != mockErr {
		t.Errorf("Expected error to be %v, but got %v", mockErr, status.Error)
	}
}

// Helper to allow mocking of net.DialTimeout
var netDialTimeout = net.DialTimeout
