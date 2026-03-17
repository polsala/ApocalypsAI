package main

import (
	"bytes"
	"fmt"
	"io"
	"net"
	"sync"
	"testing"
	"time"
)

// MockAddr implements net.Addr for testing purposes.
type MockAddr string

func (m MockAddr) Network() string { return "tcp" }
func (m MockAddr) String() string  { return string(m) }

// MockConn implements net.Conn for testing purposes.
// It uses in-memory buffers to simulate network read/write operations.
type MockConn struct {
	readBuffer  bytes.Buffer
	writeBuffer bytes.Buffer
	closeOnce   sync.Once
	closed      chan struct{}
	localAddr   net.Addr
	remoteAddr  net.Addr
}

// NewMockConn creates a new MockConn with specified local and remote addresses.
func NewMockConn(local, remote string) *MockConn {
	return &MockConn{
		closed:    make(chan struct{}),
		localAddr: MockAddr(local),
		remoteAddr: MockAddr(remote),
	}
}

// Read reads data from the mock connection's read buffer.
func (m *MockConn) Read(b []byte) (n int, err error) {
	select {
	case <-m.closed:
		return 0, io.EOF
	default:
		return m.readBuffer.Read(b)
	}
}

// Write writes data to the mock connection's write buffer.
func (m *MockConn) Write(b []byte) (n int, err error) {
	return m.writeBuffer.Write(b)
}

// Close closes the mock connection.
func (m *MockConn) Close() error {
	m.closeOnce.Do(func() {
		close(m.closed)
	})
	return nil
}

// LocalAddr returns the mock local address.
func (m *MockConn) LocalAddr() net.Addr  { return m.localAddr }
// RemoteAddr returns the mock remote address.
func (m *MockConn) RemoteAddr() net.Addr { return m.remoteAddr }

// SetDeadline is a no-op for MockConn.
func (m *MockConn) SetDeadline(t time.Time) error      { return nil }
// SetReadDeadline is a no-op for MockConn.
func (m *MockConn) SetReadDeadline(t time.Time) error  { return nil }
// SetWriteDeadline is a no-op for MockConn.
func (m *MockConn) SetWriteDeadline(t time.Time) error { return nil }

// WriteToReadBuffer simulates data coming into the connection from the network.
func (m *MockConn) WriteToReadBuffer(data string) {
	m.readBuffer.WriteString(data)
}

// ReadFromWriteBuffer reads data that was written to the connection, simulating data sent out.
func (m *MockConn) ReadFromWriteBuffer() string {
	return m.writeBuffer.String()
}

// ClearWriteBuffer clears the write buffer for fresh reads in subsequent test steps.
func (m *MockConn) ClearWriteBuffer() {
	m.writeBuffer.Reset()
}

// mockSleeper is a function that replaces time.Sleep during tests.
func mockSleeper(d time.Duration) {
	// Mock rationale: Prevents actual time.Sleep calls during tests, making them deterministic and fast.
	// This ensures tests complete quickly without waiting for simulated delays.
}

// TestHubClientLifecycle verifies that clients can register and unregister correctly with the Hub.
func TestHubClientLifecycle(t *testing.T) {
	hub := NewHub()
	hub.sleeper = mockSleeper // Mock rationale: Ensure tests don't wait for actual delays.
	go hub.Run()

	conn1 := NewMockConn("127.0.0.1:1000", "127.0.0.1:1001")
	conn2 := NewMockConn("127.0.0.1:1000", "127.0.0.1:1002")

	// Test registration
	go hub.handleConnection(conn1)
	go hub.handleConnection(conn2)

	// Give some time for goroutines to process registration
	time.Sleep(10 * time.Millisecond) // Mock rationale: A small, non-deterministic sleep is used here to allow goroutines to schedule and process channel operations. This is a common pattern in Go tests for concurrent code to ensure state changes propagate before assertions.

	hub.mu.RLock()
	if len(hub.clients) != 2 {
		t.Fatalf("Expected 2 clients after registration, got %d", len(hub.clients))
	}
	hub.mu.RUnlock()

	// Test unregistration
	conn1.Close() // Simulate client disconnecting
	time.Sleep(10 * time.Millisecond) // Mock rationale: Allow goroutines to process unregistration.

	hub.mu.RLock()
	if len(hub.clients) != 1 {
		t.Fatalf("Expected 1 client after disconnect, got %d", len(hub.clients))
	}
	if _, ok := hub.clients[conn1.RemoteAddr().String()]; ok {
		t.Fatalf("Client %s should be unregistered", conn1.RemoteAddr().String())
	}
	hub.mu.RUnlock()
}

// TestHubMessageBroadcast verifies that messages sent by one client are broadcasted to all connected clients after a delay.
func TestHubMessageBroadcast(t *testing.T) {
	hub := NewHub()
	hub.sleeper = mockSleeper // Mock rationale: Ensure tests don't wait for actual delays.
	go hub.Run()

	conn1 := NewMockConn("127.0.0.1:1000", "127.0.0.1:1001")
	conn2 := NewMockConn("127.0.0.1:1000", "127.0.0.1:1002")
	conn3 := NewMockConn("127.0.0.1:1000", "127.0.0.1:1003")

	go hub.handleConnection(conn1)
	go hub.handleConnection(conn2)
	go hub.handleConnection(conn3)

	time.Sleep(10 * time.Millisecond) // Mock rationale: Allow clients to register.

	testMessage := "Hello from the past!"
	conn1.WriteToReadBuffer(testMessage + "\n") // Simulate conn1 sending a message

	time.Sleep(10 * time.Millisecond) // Mock rationale: Allow message to be processed and broadcasted.

	expectedPrefix := fmt.Sprintf("[Temporal Echo from %s] ", conn1.RemoteAddr().String())
	expectedMessage := expectedPrefix + testMessage + "\n"

	// Check if all clients received the message
	for _, conn := range []*MockConn{conn1, conn2, conn3} {
		received := conn.ReadFromWriteBuffer()
		if received != expectedMessage {
			t.Errorf("Client %s: Expected '%s', got '%s'", conn.RemoteAddr().String(), expectedMessage, received)
		}
		conn.ClearWriteBuffer() // Clear for next test if any
	}

	// Test with another message from a different client
	testMessage2 := "Another ripple in time."
	conn2.WriteToReadBuffer(testMessage2 + "\n")

	time.Sleep(10 * time.Millisecond) // Mock rationale: Allow message to be processed and broadcasted.

	expectedPrefix2 := fmt.Sprintf("[Temporal Echo from %s] ", conn2.RemoteAddr().String())
	expectedMessage2 := expectedPrefix2 + testMessage2 + "\n"

	for _, conn := range []*MockConn{conn1, conn2, conn3} {
		received := conn.ReadFromWriteBuffer()
		if received != expectedMessage2 {
			t.Errorf("Client %s: Expected '%s', got '%s'", conn.RemoteAddr().String(), expectedMessage2, received)
		}
	}
}

// TestHubEmptyMessage ensures that empty or whitespace-only messages are ignored and not broadcasted.
func TestHubEmptyMessage(t *testing.T) {
	hub := NewHub()
	hub.sleeper = mockSleeper // Mock rationale: Ensure tests don't wait for actual delays.
	go hub.Run()

	conn1 := NewMockConn("127.0.0.1:1000", "127.0.0.1:1001")
	go hub.handleConnection(conn1)
	time.Sleep(10 * time.Millisecond) // Mock rationale: Allow client to register.

	conn1.WriteToReadBuffer("\n")    // Empty line
	conn1.WriteToReadBuffer("   \n") // Whitespace line

	time.Sleep(10 * time.Millisecond) // Mock rationale: Allow messages to be processed.

	received := conn1.ReadFromWriteBuffer()
	if received != "" {
		t.Errorf("Expected no message for empty/whitespace input, got '%s'", received)
	}
}
