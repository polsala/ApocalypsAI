package main

import (
	"net"
	"testing"
	"time"
	"sync"
	"fmt"
	"errors"
)

// MockDialer is a mock implementation of net.Dialer.
type MockDialer struct {
	DialFunc func(network, address string, timeout time.Duration) (net.Conn, error)
}

func (m *MockDialer) DialTimeout(network, address string, timeout time.Duration) (net.Conn, error) {
	if m.DialFunc != nil {
		return m.DialFunc(network, address, timeout)
	}
	return nil, errors.New("MockDialer: DialFunc not set")
}

// MockConn is a mock implementation of net.Conn.
type MockConn struct {
	// Add any necessary fields for your mock connection if needed
}

func (m *MockConn) Read(b []byte) (n int, err error) { return 0, nil } // Mock implementation
func (m *MockConn) Write(b []byte) (n int, err error) { return 0, nil } // Mock implementation
func (m *MockConn) Close() error { return nil } // Mock implementation
func (m *MockConn) LocalAddr() net.Addr { return nil } // Mock implementation
func (m *MockConn) RemoteAddr() net.Addr { return nil } // Mock implementation
func (m *MockConn) SetDeadline(t time.Time) error { return nil } // Mock implementation
func (m *MockConn) SetReadDeadline(t time.Time) error { return nil } // Mock implementation
func (m *MockConn) SetWriteDeadline(t time.Time) error { return nil } // Mock implementation

// Mock rationale: We are mocking the net.DialTimeout function to simulate successful and failed network connections without actually making network calls. This ensures deterministic and offline test execution.
func TestProbeService(t *testing.T) {
	var wg sync.WaitGroup
	results := make(chan string, 1)

	// Mock for a successful connection
	mockDialerSuccess := &MockDialer{
		DialFunc: func(network, address string, timeout time.Duration) (net.Conn, error) {
			return &MockConn{}, nil
		},
	}

	// Mock for a failed connection (e.g., connection refused)
	mockDialerFailure := &MockDialer{
		DialFunc: func(network, address string, timeout time.Duration) (net.Conn, error) {
			return nil, errors.New("connection refused")
		},
	}

	// Test case: Successful probe
	wg.Add(1)
	go func() {
		// Temporarily replace net.DialTimeout with our mock
		originalDialTimeout := net.DialTimeout
		net.DialTimeout = mockDialerSuccess.DialTimeout
		defer func() { net.DialTimeout = originalDialTimeout }() // Restore original

		probeService("example.com:80", &wg, results)
	}()
	wg.Wait()
	close(results)

	result := <-results
	if !strings.Contains(result, "is UP") {
		t.Errorf("Expected successful probe, but got: %s", result)
	}

	// Reset for the next test case
	results = make(chan string, 1)

	// Test case: Failed probe
	wg.Add(1)
	go func() {
		// Temporarily replace net.DialTimeout with our mock
		originalDialTimeout := net.DialTimeout
		net.DialTimeout = mockDialerFailure.DialTimeout
		defer func() { net.DialTimeout = originalDialTimeout }() // Restore original

		probeService("localhost:8080", &wg, results)
	}()
	wg.Wait()
	close(results)

	result = <-results
	if !strings.Contains(result, "is DOWN") {
		t.Errorf("Expected failed probe, but got: %s", result)
	}
}

// Helper to check if a string contains a substring (Go 1.18+ has strings.Contains)
func stringsContains(s, substr string) bool {
	return len(s) >= len(substr) && s[0:len(substr)] == substr
}

// Mock rationale: The original probeService function directly calls net.DialTimeout. To test it without actual network calls, we need to replace net.DialTimeout with a mock. This test function achieves that by temporarily assigning a mock implementation to net.DialTimeout within the scope of the test.
func TestMainFunctionality(t *testing.T) {
	// This test is more of an integration test for the main function's argument parsing and goroutine management.
	// For true unit testing of probeService, see TestProbeService.

	// Mocking os.Args to simulate command-line input
	originalArgs := os.Args
	os.Args = []string{"./concurrency_probe", "mock.host:1234", "another.host:5678"}
	defer func() { os.Args = originalArgs }() // Restore original args

	// Mocking net.DialTimeout for the duration of the main function execution
	originalDialTimeout := net.DialTimeout
	mockDialer := &MockDialer{
		DialFunc: func(network, address string, timeout time.Duration) (net.Conn, error) {
			// Simulate one success and one failure based on address
			if address == "mock.host:1234" {
				return &MockConn{}, nil
			} else if address == "another.host:5678" {
				return nil, errors.New("timeout")
			}
			return nil, errors.New("unexpected host")
		},
	}
	net.DialTimeout = mockDialer.DialTimeout
	defer func() { net.DialTimeout = originalDialTimeout }() // Restore original

	// Capture stdout to verify output
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	main()

	w := w
	w.Close()
	os.Stdout = oldStdout

	// Read captured output
	var buf strings.Builder
	io.Copy(&buf, r)
	output := buf.String()

	if !strings.Contains(output, "mock.host:1234 is UP") {
		t.Errorf("Expected 'mock.host:1234 is UP' in output, got: %s", output)
	}

	if !strings.Contains(output, "another.host:5678 is DOWN") {
		t.Errorf("Expected 'another.host:5678 is DOWN' in output, got: %s", output)
	}
}

// Mock rationale: This test verifies the main function's behavior, including argument parsing and the overall flow of goroutine creation and result aggregation. It mocks `os.Args` to control input and `net.DialTimeout` to simulate network responses. It also captures stdout to assert the printed output, ensuring the utility functions as expected from end-to-end.
