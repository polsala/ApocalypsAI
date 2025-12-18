package main

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"strings"
	"testing"
	"time"
)

// MockDialer is a mock implementation of net.Dialer.
type MockDialer struct {
	DialFunc func(network, address string, timeout time.Duration) (net.Conn, error)
}

func (m *MockDialer) Dial(network, address string, timeout time.Duration) (net.Conn, error) {
	if m.DialFunc != nil {
		return m.DialFunc(network, address, timeout)
	}
	return nil, fmt.Errorf("DialFunc not implemented")
}

// MockConn is a mock implementation of net.Conn.
type MockConn struct {
	ReadFunc  func(b []byte) (n int, err error)
	WriteFunc func(b []byte) (n int, err error)
	CloseFunc func() error
	LocalAddrFunc func() net.Addr
	RemoteAddrFunc func() net.Addr
	SetDeadlineFunc func(t time.Time) error
	SetReadDeadlineFunc func(t time.Time) error
	SetWriteDeadlineFunc func(t time.Time) error
}

func (m *MockConn) Read(b []byte) (n int, err error) {
	if m.ReadFunc != nil {
		return m.ReadFunc(b)
	}
	return 0, io.EOF
}

func (m *MockConn) Write(b []byte) (n int, err error) {
	if m.WriteFunc != nil {
		return m.WriteFunc(b)
	}
	return len(b), nil
}

func (m *MockConn) Close() error {
	if m.CloseFunc != nil {
		return m.CloseFunc()
	}
	return nil
}

func (m *MockConn) LocalAddr() net.Addr {
	if m.LocalAddrFunc != nil {
		return m.LocalAddrFunc()
	}
	return &net.IPAddr{IP: net.ParseIP("127.0.0.1")}
}

func (m *MockConn) RemoteAddr() net.Addr {
	if m.RemoteAddrFunc != nil {
		return m.RemoteAddrFunc()
	}
	return &net.IPAddr{IP: net.ParseIP("1.1.1.1")}
}

func (m *MockConn) SetDeadline(t time.Time) error {
	if m.SetDeadlineFunc != nil {
		return m.SetDeadlineFunc(t)
	}
	return nil
}

func (m *MockConn) SetReadDeadline(t time.Time) error {
	if m.SetReadDeadlineFunc != nil {
		return m.SetReadDeadlineFunc(t)
	}
	return nil
}

func (m *MockConn) SetWriteDeadline(t time.Time) error {
	if m.SetWriteDeadlineFunc != nil {
		return m.SetWriteDeadlineFunc(t)
	}
	return nil
}

// MockDial is a helper to create a mock dialer that returns a specific connection.
func MockDial(conn net.Conn, err error) *MockDialer {
	return &MockDialer{
		DialFunc: func(network, address string, timeout time.Duration) (net.Conn, error) {
			return conn, err
		},
	}
}

// Replace net.DialTimeout with our mock for testing.
var originalDialTimeout func(network, address string, timeout time.Duration) (net.Conn, error)

func setupMockDial() {
	originalDialTimeout = net.DialTimeout
	net.DialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		// This function will be replaced by the specific mock in each test.
		panic("net.DialTimeout should have been mocked")
	}
}

func restoreDial() {
	net.DialTimeout = originalDialTimeout
}

func TestProbeEndpoint_Success(t *testing.T) {
	setupMockDial()
	defer restoreDial()

	// Mock a successful connection.
	mockConn := &MockConn{}
	mockDialer := MockDial(mockConn, nil)

	// Temporarily replace net.DialTimeout with our mock dialer's Dial function.
	// This is a bit of a hack to inject the mock. In a real-world scenario, you might
	// pass the dialer as a dependency.
	originalNetDialTimeout := net.DialTimeout
	net.DialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return mockDialer.Dial(network, address, timeout)
	}
	defer func() { net.DialTimeout = originalNetDialTimeout }()

	// Capture stdout
	oldStdout := os.Stdout
	defer func() { os.Stdout = oldStdout }()
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Run the probe
	go probeEndpoint("example.com:80", 1*time.Second)

	w.Close()
	var buf bytes.Buffer
	io.Copy(&buf, r)
	output := buf.String()

	expectedPrefix := "Endpoint: example.com:80, Status: UP, Latency: "
	if !strings.HasPrefix(output, expectedPrefix) {
		t.Errorf("Expected output to start with '%s', but got '%s'", expectedPrefix, output)
	}

	// Check if latency is a valid duration string (e.g., '10ms')
	latencyStr := strings.TrimSpace(strings.TrimPrefix(output, expectedPrefix))
	_, err := time.ParseDuration(latencyStr)
	if err != nil {
		t.Errorf("Invalid latency format: %s, error: %v", latencyStr, err)
	}
}

func TestProbeEndpoint_Failure(t *testing.T) {
	setupMockDial()
	defer restoreDial()

	// Mock a failed connection.
	mockConn := &MockConn{}
	mockDialer := MockDial(mockConn, fmt.Errorf("connection refused"))

	originalNetDialTimeout := net.DialTimeout
	net.DialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return mockDialer.Dial(network, address, timeout)
	}
	defer func() { net.DialTimeout = originalNetDialTimeout }()

	// Capture stdout
	oldStdout := os.Stdout
	defer func() { os.Stdout = oldStdout }()
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Run the probe
	go probeEndpoint("nonexistent.com:80", 1*time.Second)

	w.Close()
	var buf bytes.Buffer
	io.Copy(&buf, r)
	output := buf.String()

	expected := "Endpoint: nonexistent.com:80, Status: DOWN, Latency: N/A (Error: connection refused)\n"
	if output != expected {
		t.Errorf("Expected output '%s', but got '%s'", expected, output)
	}
}

func TestMain_NoArgs(t *testing.T) {
	// Save original args and replace os.Args
	oldArgs := os.Args
	defer func() { os.Args = oldArgs }()

	// Mock os.Args to simulate running with no arguments
	os.Args = []string{os.Args[0]} // Program name only

	// Capture stdout
	oldStdout := os.Stdout
	defer func() { os.Stdout = oldStdout }()
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Mock os.Exit to prevent actual exit and capture exit code
	exitCode := 0
	originalExit := os.Exit
	defer func() { os.Exit = originalExit }()
	os.Exit = func(code int) {
		exitCode = code
	}

	// Run main function
	main()

	w.Close()
	var buf bytes.Buffer
	io.Copy(&buf, r)
	output := buf.String()

	expectedUsage := "Usage: netprobe [-timeout duration] <endpoint1> <endpoint2> ...\n"
	if output != expectedUsage {
		t.Errorf("Expected output '%s', but got '%s'", expectedUsage, output)
	}

	if exitCode != 1 {
		t.Errorf("Expected exit code 1, but got %d", exitCode)
	}
}

func TestMain_WithArgs(t *testing.T) {
	setupMockDial()
	defer restoreDial()

	// Mock successful connections for the arguments
	mockConn1 := &MockConn{}
	mockConn2 := &MockConn{}

	// Create a map to track which endpoint is being dialed and return the appropriate mock.
	// This is a simplified approach; a more robust mock would handle specific addresses.
	var mockDialerMap = map[string]net.Conn{
		"google.com:80": mockConn1,
		"example.com:443": mockConn2,
	}

	originalNetDialTimeout := net.DialTimeout
	net.DialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		conn, ok := mockDialerMap[address]
		if !ok {
			return nil, fmt.Errorf("unexpected endpoint: %s", address)
		}
		return conn, nil
	}
	defer func() { net.DialTimeout = originalNetDialTimeout }()

	// Save original args and replace os.Args
	oldArgs := os.Args
	defer func() { os.Args = oldArgs }()

	// Mock os.Args to simulate running with arguments
	os.Args = []string{os.Args[0], "google.com:80", "example.com:443"}

	// Capture stdout
	oldStdout := os.Stdout
	defer func() { os.Stdout = oldStdout }()
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Run main function
	main()

	w.Close()
	var buf bytes.Buffer
	io.Copy(&buf, r)
	output := buf.String()

	// Check if output contains expected lines for both endpoints
	expectedLine1 := "Endpoint: google.com:80, Status: UP, Latency: "
	expectedLine2 := "Endpoint: example.com:443, Status: UP, Latency: "

	if !strings.Contains(output, expectedLine1) {
		t.Errorf("Output missing expected line for google.com:80. Got: %s", output)
	}

	if !strings.Contains(output, expectedLine2) {
		t.Errorf("Output missing expected line for example.com:443. Got: %s", output)
	}

	// Basic check for latency format in the output lines
	lines := strings.Split(strings.TrimSpace(output), "\n")
	for _, line := range lines {
		if strings.Contains(line, "google.com:80") {
			latencyStr := strings.TrimSpace(strings.TrimPrefix(line, expectedLine1))
			if _, err := time.ParseDuration(latencyStr); err != nil {
				t.Errorf("Invalid latency format for google.com:80: %s", latencyStr)
			}
		}
		if strings.Contains(line, "example.com:443") {
			latencyStr := strings.TrimSpace(strings.TrimPrefix(line, expectedLine2))
			if _, err := time.ParseDuration(latencyStr); err != nil {
				t.Errorf("Invalid latency format for example.com:443: %s", latencyStr)
			}
		}
	}
}
