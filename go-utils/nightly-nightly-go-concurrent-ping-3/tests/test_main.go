package main

import (
	"bytes"
	"fmt"
	"net"
	"os"
	"strings"
	"testing"
	"time"
)

// Mock implementation of net.LookupHost for testing DNS resolution.
var mockLookupHost func(host string) ([]string, error)

// Mock implementation of net.DialTimeout for testing network connectivity.
var mockDialTimeout func(network, addr string, timeout time.Duration) (net.Conn, error)

// MockConn is a dummy net.Conn for testing.
type MockConn struct{}

func (mc *MockConn) Read(b []byte) (n int, err error) { return 0, fmt.Errorf("not implemented") }
func (mc *MockConn) Write(b []byte) (n int, err error) { return 0, fmt.Errorf("not implemented") }
func (mc *MockConn) Close() error { return nil }
func (mc *MockConn) LocalAddr() net.Addr { return nil }
func (mc *MockConn) RemoteAddr() net.Addr { return nil }
func (mc *MockConn) SetDeadline(t time.Time) error { return nil }
func (mc *MockConn) SetReadDeadline(t time.Time) error { return nil }
func (mc *MockConn) SetWriteDeadline(t time.Time) error { return nil }

func TestMain_NoArgs(t *testing.T) {
	// Mock os.Args to simulate no arguments being passed.
	originalArgs := os.Args
	os.Args = []string{os.Args[0]}
	defer func() {
		os.Args = originalArgs
	}()

	// Capture stdout to check for error message.
	oldStdout := os.Stdout
	var buf bytes.Buffer
	os.Stdout = &buf
	defer func() {
		os.Stdout = oldStdout
	}()

	// Expecting os.Exit to be called, so we'll defer a panic recovery.
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("The code did not panic as expected
")
		}
	}()

	main()

	expectedOutput := "Usage: concurrent-ping <host1,host2,வைக்\n"
	if buf.String() != expectedOutput {
		t.Errorf("Expected output '%s', but got '%s'", expectedOutput, buf.String())
	}
}

func TestPingHost_Success(t *testing.T) {
	// Mock rationale: Simulate a successful DNS lookup and TCP connection.
	mockLookupHost = func(host string) ([]string, error) {
		return []string{"127.0.0.1"}, nil
	}
	mockDialTimeout = func(network, addr string, timeout time.Duration) (net.Conn, error) {
		return &MockConn{}, nil
	}

	var wg sync.WaitGroup
	results := make(chan HostStatus, 1)

	wg.Add(1)
	go pingHost("example.com", &wg, results)
	wg.Wait()
	close(results)

	status := <-results

	if status.Status != "UP" {
		t.Errorf("Expected status UP, got %s", status.Status)
	}
	if status.ErrorMsg != "" {
		t.Errorf("Expected no error, got %s", status.ErrorMsg)
	}
	if status.Duration == 0 {
		t.Errorf("Expected non-zero duration, got 0")
	}
}

func TestPingHost_DNSLookupError(t *testing.T) {
	// Mock rationale: Simulate a DNS lookup failure.
	mockLookupHost = func(host string) ([]string, error) {
		return nil, fmt.Errorf("lookup %s: no such host", host)
	}
	mockDialTimeout = func(network, addr string, timeout time.Duration) (net.Conn, error) {
		// This should not be called.
		return nil, fmt.Errorf("dial should not be called")
	}

	var wg sync.WaitGroup
	results := make(chan HostStatus, 1)

	wg.Add(1)
	go pingHost("invalid.host.local", &wg, results)
	wg.Wait()
	close(results)

	status := <-results

	if status.Status != "ERROR" {
		t.Errorf("Expected status ERROR, got %s", status.Status)
	}
	if !strings.Contains(status.ErrorMsg, "no such host") {
		t.Errorf("Expected error message containing 'no such host', got '%s'", status.ErrorMsg)
	}
	if status.Duration == 0 {
		t.Errorf("Expected non-zero duration, got 0")
	}
}

func TestPingHost_DialTimeoutError(t *testing.T) {
	// Mock rationale: Simulate a successful DNS lookup but a dial timeout.
	mockLookupHost = func(host string) ([]string, error) {
		return []string{"127.0.0.1"}, nil
	}
	mockDialTimeout = func(network, addr string, timeout time.Duration) (net.Conn, error) {
		return nil, fmt.Errorf("dial tcp %s: i/o timeout", addr)
	}

	var wg sync.WaitGroup
	results := make(chan HostStatus, 1)

	wg.Add(1)
	go pingHost("unreachable.host", &wg, results)
	wg.Wait()
	close(results)

	status := <-results

	if status.Status != "DOWN" {
		t.Errorf("Expected status DOWN, got %s", status.Status)
	}
	if status.ErrorMsg != "" {
		t.Errorf("Expected no error message, got '%s'", status.ErrorMsg)
	}
	if status.Duration == 0 {
		t.Errorf("Expected non-zero duration, got 0")
	}
}

// Helper function to replace the actual net functions with mocks.
func init() {
	// Mock rationale: Replace standard library functions with mocks for deterministic testing.
	net.LookupHost = func(host string) ([]string, error) {
		if mockLookupHost != nil {
			return mockLookupHost(host)
		}
		return nil, fmt.Errorf("mockLookupHost not set")
	}

	net.DialTimeout = func(network, addr string, timeout time.Duration) (net.Conn, error) {
		if mockDialTimeout != nil {
			return mockDialTimeout(network, addr, timeout)
		}
		return nil, fmt.Errorf("mockDialTimeout not set")
	}
}
