package main

import (
	"bufio"
	"fmt"
	"net"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock rationale: We need to test the server's internal logic (like handleConnection)
// without actually binding to a port and making real network calls. This makes tests
// fast, deterministic, and prevents port conflicts. We simulate client connections
// and server responses using an in-memory mock net.Conn implementation.
// For testing the server's ability to start/stop and bind to a port, we use real
// network calls on ephemeral ports, as this is a core functionality to verify.

// MockConn implements net.Conn for testing purposes.
type MockConn struct {
	net.Conn
	readBuffer  *strings.Reader
	writeBuffer *strings.Builder
	closeOnce   sync.Once
	closed      chan struct{}
	localAddr   net.Addr
	remoteAddr  net.Addr
}

func NewMockConn(readInput string) *MockConn {
	return &MockConn{
		readBuffer:  strings.NewReader(readInput),
		writeBuffer: &strings.Builder{},
		closed:      make(chan struct{}),
		localAddr:   &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 12345}, // Mock address
		remoteAddr:  &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 54321}, // Mock address
	}
}

func (m *MockConn) Read(b []byte) (n int, err error) {
	select {
	case <-m.closed:
		return 0, fmt.Errorf("read on closed connection")
	default:
		return m.readBuffer.Read(b)
	}
}

func (m *MockConn) Write(b []byte) (n int, err error) {
	select {
	case <-m.closed:
		return 0, fmt.Errorf("write on closed connection")
	default:
		return m.writeBuffer.Write(b)
	}
}

func (m *MockConn) Close() error {
	m.closeOnce.Do(func() {
		close(m.closed)
	})
	return nil
}

func (m *MockConn) LocalAddr() net.Addr {
	return m.localAddr
}

func (m *MockConn) RemoteAddr() net.Addr {
	return m.remoteAddr
}

func (m *MockConn) SetDeadline(t time.Time) error {
	return nil // Mock: no-op for deadlines
}

func (m *MockConn) SetReadDeadline(t time.Time) error {
	return nil // Mock: no-op for deadlines
}

func (m *MockConn) SetWriteDeadline(t time.Time) error {
	return nil // Mock: no-op for deadlines
}

// GetWrittenData returns the data written to the mock connection.
func (m *MockConn) GetWrittenData() string {
	return m.writeBuffer.String()
}

func TestHandleConnection_SyncCommand(t *testing.T) {
	server := NewServer(0) // Port 0 for testing, won't actually listen
	mockConn := NewMockConn("SYNC\n")

	// Run handleConnection in a goroutine as it's blocking on ReadString
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		server.handleConnection(mockConn)
	}()

	// Give the goroutine a moment to process the command and write a response
	time.Sleep(10 * time.Millisecond)

	// Close the mock connection to signal end of read/write and unblock handleConnection
	mockConn.Close()
	wg.Wait() // Ensure handleConnection has finished

	response := mockConn.GetWrittenData()
	if !strings.HasSuffix(response, "\n") {
		t.Errorf("Expected response to end with newline, got: %q", response)
	}
	response = strings.TrimSpace(response)

	// Verify the response is a valid RFC3339Nano timestamp
	parsedTime, err := time.Parse(time.RFC3339Nano, response)
	if err != nil {
		t.Fatalf("Failed to parse timestamp from response: %v, response: %q", err, response)
	}

	// Check if the time is recent (within a reasonable delta)
	now := time.Now().UTC()
	if now.Sub(parsedTime) > 1*time.Second || parsedTime.Sub(now) > 1*time.Second {
		t.Errorf("Timestamp is not recent enough. Got %v, expected around %v", parsedTime, now)
	}
}

func TestHandleConnection_UnknownCommand(t *testing.T) {
	server := NewServer(0)
	mockConn := NewMockConn("UNKNOWN_CMD\n")

	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		server.handleConnection(mockConn)
	}()

	time.Sleep(10 * time.Millisecond)
	mockConn.Close()
	wg.Wait()

	response := mockConn.GetWrittenData()
	expectedPrefix := "UNKNOWN_COMMAND: UNKNOWN_CMD\n"
	if !strings.HasPrefix(response, expectedPrefix) {
		t.Errorf("Expected response to start with %q, got %q", expectedPrefix, response)
	}
}

func TestServerStartAndStop(t *testing.T) {
	// Use a high ephemeral port to avoid conflicts
	port := 10000 + (time.Now().Nanosecond() % 10000)
	server := NewServer(port)

	err := server.Start()
	if err != nil {
		t.Fatalf("Server failed to start: %v", err)
	}

	// Verify server is running by trying to connect
	conn, err := net.DialTimeout("tcp", fmt.Sprintf("localhost:%d", port), 100*time.Millisecond)
	if err != nil {
		t.Fatalf("Failed to connect to server: %v", err)
	}
	conn.Close()

	server.Stop()

	// Verify server is stopped by trying to connect again (should fail)
	_, err = net.DialTimeout("tcp", fmt.Sprintf("localhost:%d", port), 100*time.Millisecond)
	if err == nil {
		t.Error("Expected connection to fail after server stopped, but it succeeded")
	}
}

func TestServerStartFailure(t *testing.T) {
	// Try to start on a privileged port without root (should fail)
	server := NewServer(1) // Port 1 is usually privileged
	err := server.Start()
	if err == nil {
		t.Error("Expected server to fail starting on a privileged port, but it succeeded")
	}
	server.Stop() // Ensure it's stopped if it somehow started
}

func TestMultipleSyncRequests(t *testing.T) {
	server := NewServer(0)
	mockConn := NewMockConn("SYNC\nSYNC\nUNKNOWN_CMD\nSYNC\n")

	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		server.handleConnection(mockConn)
	}()

	time.Sleep(50 * time.Millisecond) // Give it time to process multiple commands
	mockConn.Close()
	wg.Wait()

	response := mockConn.GetWrittenData()
	lines := strings.Split(strings.TrimSpace(response), "\n")

	if len(lines) != 4 {
		t.Fatalf("Expected 4 response lines, got %d: %q", len(lines), response)
	}

	// Check first SYNC response
	_, err := time.Parse(time.RFC3339Nano, lines[0])
	if err != nil {
		t.Errorf("First SYNC response invalid: %v", err)
	}

	// Check second SYNC response
	_, err = time.Parse(time.RFC3339Nano, lines[1])
	if err != nil {
		t.Errorf("Second SYNC response invalid: %v", err)
	}

	// Check UNKNOWN_CMD response
	expectedUnknownPrefix := "UNKNOWN_COMMAND: UNKNOWN_CMD"
	if !strings.HasPrefix(lines[2], expectedUnknownPrefix) {
		t.Errorf("Expected unknown command response %q, got %q", expectedUnknownPrefix, lines[2])
	}

	// Check third SYNC response
	_, err = time.Parse(time.RFC3339Nano, lines[3])
	if err != nil {
		t.Errorf("Third SYNC response invalid: %v", err)
	}
}

func TestServerRunningState(t *testing.T) {
	port := 10000 + (time.Now().Nanosecond() % 10000)
	server := NewServer(port)

	err := server.Start()
	if err != nil {
		t.Fatalf("Server failed to start: %v", err)
	}

	// Try to start again, should return an error
	err = server.Start()
	if err == nil || !strings.Contains(err.Error(), "already running") {
		t.Errorf("Expected 'server already running' error, got: %v", err)
	}

	server.Stop()

	// Try to stop again, should be a no-op
	server.Stop()
}
