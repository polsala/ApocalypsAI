package main_test

import (
	"bytes"
	"fmt"
	"net"
	"os/exec"
	"strings"
	"testing"
	"time"
)

// Mock rationale: This mock replaces the standard net.DialTimeout function
// to allow for deterministic testing without actual network calls.
// It simulates successful connections and timeouts based on predefined scenarios.
var mockDialTimeout func(network, address string, timeout time.Duration) (net.Conn, error)

type mockConn struct{}`

func (m *mockConn) Read(b []byte) (n int, err error) { return 0, nil }
func (m *mockConn) Write(b []byte) (n int, err error) { return 0, nil }
func (m *mockConn) Close() error { return nil }
func (m *mockConn) LocalAddr() net.Addr { return nil }
func (m *mockConn) RemoteAddr() net.Addr { return nil }
func (m *mockConn) SetDeadline(t time.Time) error { return nil }
func (m *mockConn) SetReadDeadline(t time.Time) error { return nil }
func (m *mockConn) SetWriteDeadline(t time.Time) error { return nil }

func TestPingHost_Reachable(t *testing.T) {
	// Mock net.DialTimeout to always succeed for this test case.
	mockDialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return &mockConn{}, nil
	}

	// Temporarily replace the actual DialTimeout with our mock.
	originalDialTimeout := net.DialTimeout
	net.DialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return mockDialTimeout(network, address, timeout)
	}
	defer func() { net.DialTimeout = originalDialTimeout }() // Restore original function

	result := pingHost("example.com", 5*time.Second)
	if result != "Reachable" {
		t.Errorf("Expected 'Reachable', got '%s'", result)
	}
}

func TestPingHost_UnreachableTimeout(t *testing.T) {
	// Mock net.DialTimeout to simulate a timeout error.
	mockDialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return nil, net.DNSError{IsTimeout: true}
	}

	originalDialTimeout := net.DialTimeout
	net.DialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return mockDialTimeout(network, address, timeout)
	}
	defer func() { net.DialTimeout = originalDialTimeout }()

	result := pingHost("nonexistent.local", 1*time.Second)
	if !strings.Contains(result, "Unreachable (timeout)") {
		t.Errorf("Expected 'Unreachable (timeout)', got '%s'", result)
	}
}

func TestPingHost_UnreachableOtherError(t *testing.T) {
	// Mock net.DialTimeout to simulate a different network error.
	mockDialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return nil, fmt.Errorf("connection refused")
	}

	originalDialTimeout := net.DialTimeout
	net.DialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return mockDialTimeout(network, address, timeout)
	}
	defer func() { net.DialTimeout = originalDialTimeout }()

	result := pingHost("localhost:9999", 1*time.Second)
	if !strings.Contains(result, "Unreachable (connection refused)") {
		t.Errorf("Expected 'Unreachable (connection refused)', got '%s'", result)
	}
}

func TestMain_ConcurrentPinging(t *testing.T) {
	// This test executes the main program and checks its output.
	// We'll use a mock for DialTimeout to ensure deterministic results.

	// Mock DialTimeout to simulate a mix of reachable and unreachable hosts.
	// The first two hosts will be reachable, the third will timeout.
	var callCount int
	mockDialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		callCount++
		if callCount <= 2 {
			return &mockConn{}, nil
		}
		return nil, net.DNSError{IsTimeout: true}
	}

	originalDialTimeout := net.DialTimeout
	net.DialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return mockDialTimeout(network, address, timeout)
	}
	defer func() { net.DialTimeout = originalDialTimeout }()

	// Build and run the command
	cmd := exec.Command("go", "run", "src/main.go", "host1", "host2", "host3")
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	err := cmd.Run()
	if err != nil {
		t.Fatalf("Command failed: %v\nStderr: %s", err, stderr.String())
	}

	output := stdout.String()

	// Check if all hosts are mentioned and have correct statuses
	if !strings.Contains(output, "Host: host1 - Status: Reachable") {
		t.Errorf("Output missing or incorrect for host1: %s", output)
	}
	if !strings.Contains(output, "Host: host2 - Status: Reachable") {
		t.Errorf("Output missing or incorrect for host2: %s", output)
	}
	if !strings.Contains(output, "Host: host3 - Status: Unreachable (timeout)") {
		t.Errorf("Output missing or incorrect for host3: %s", output)
	}
}

func TestMain_NoHosts(t *testing.T) {
	// Test case where no hosts are provided.
	cmd := exec.Command("go", "run", "src/main.go")
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	err := cmd.Run()
	if err == nil {
		t.Fatalf("Command should have failed with no hosts, but succeeded.")
	}

	expectedUsage := "Usage: ping-probe"
	if !strings.Contains(stderr.String(), expectedUsage) {
		t.Errorf("Expected stderr to contain '%s', but got '%s'", expectedUsage, stderr.String())
	}
}
