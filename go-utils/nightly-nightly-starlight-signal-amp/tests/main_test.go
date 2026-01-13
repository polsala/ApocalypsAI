package main

import (
	"errors"
	"fmt"
	"net"
	"strconv"
	"sync"
	"testing"
	"time"
)

// MockConn implements net.Conn for testing purposes.
type MockConn struct{}

func (m *MockConn) Read(b []byte) (n int, err error)         { return 0, nil }
func (m *MockConn) Write(b []byte) (n int, err error)        { return 0, nil }
func (m *MockConn) Close() error                             { return nil }
func (m *MockConn) LocalAddr() net.Addr                      { return nil }
func (m *MockConn) RemoteAddr() net.Addr                     { return nil }
func (m *MockConn) SetDeadline(t time.Time) error            { return nil }
func (m *MockConn) SetReadDeadline(t time.Time) error        { return nil }
func (m *MockConn) SetWriteDeadline(t time.Time) error       { return nil }

// Mock rationale: We need to simulate network connections without actually performing I/O.
// This mockDialer function replaces net.DialTimeout to return a successful connection
// for specific "open" ports and an error for "closed" ports, making tests deterministic and offline.
func mockDialer(openPorts map[int]bool) DialerFunc {
	return func(network, address string, timeout time.Duration) (net.Conn, error) {
		// Extract port from address string (e.g., "localhost:80" -> 80)
		_, portStr, err := net.SplitHostPort(address)
		if err != nil {
			return nil, err
		}
		port, err := strconv.Atoi(portStr)
		if err != nil {
			return nil, err
		}

		if openPorts[port] {
			return &MockConn{}, nil // Simulate a successful connection
		}
		return nil, errors.New("connection refused") // Simulate a failed connection
	}
}

func TestScanPort(t *testing.T) {
	tests := []struct {
		name      string
		host      string
		port      int
		openPorts map[int]bool
		expected  bool // true if port is expected to be found open
	}{
		{
			name:      "Open Port",
			host:      "localhost",
			port:      80,
			openPorts: map[int]bool{80: true},
			expected:  true,
		},
		{
			name:      "Closed Port",
			host:      "localhost",
			port:      81,
			openPorts: map[int]bool{80: true},
			expected:  false,
		},
		{
			name:      "Another Open Port",
			host:      "remote.example.com",
			port:      443,
			openPorts: map[int]bool{443: true, 22: true},
			expected:  true,
		},
		{
			name:      "Another Closed Port",
			host:      "remote.example.com",
			port:      21,
			openPorts: map[int]bool{443: true, 22: true},
			expected:  false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var wg sync.WaitGroup
			results := make(chan int, 1) // Buffered channel for a single result
			dialer := mockDialer(tt.openPorts)

			wg.Add(1)
			go scanPort(tt.host, tt.port, 100*time.Millisecond, dialer, results, &wg)

			wg.Wait()
			close(results)

			found := false
			for p := range results {
				if p == tt.port {
					found = true
					break
				}
			}

			if found != tt.expected {
				t.Errorf("scanPort(%s, %d) = %v, expected %v", tt.host, tt.port, found, tt.expected)
			}
		})
	}
}

func TestScanPortRange(t *testing.T) {
	// Mock rationale: Similar to TestScanPort, we use a mockDialer to control
	// which ports appear open or closed, ensuring deterministic behavior
	// without actual network calls.
	openPorts := map[int]bool{
		22:   true,
		80:   true,
		443:  true,
		8080: true,
	}
	dialer := mockDialer(openPorts)

	host := "test.host"
	startPort := 1
	endPort := 10000 // A wide range to ensure concurrency works
	timeout := 100 * time.Millisecond

	var wg sync.WaitGroup
	results := make(chan int, endPort-startPort+1) // Buffered channel

	for port := startPort; port <= endPort; port++ {
		wg.Add(1)
		go scanPort(host, port, timeout, dialer, results, &wg)
	}

	wg.Wait()
	close(results)

	foundPorts := make(map[int]bool)
	for p := range results {
		foundPorts[p] = true
	}

	// Check if all expected open ports were found
	for p := range openPorts {
		if !foundPorts[p] {
			t.Errorf("Expected port %d to be found open, but it was not.", p)
		}
	}

	// Check if only expected open ports were found (no false positives)
	for p := range foundPorts {
		if !openPorts[p] {
			t.Errorf("Unexpected port %d reported as open.", p)
		}
	}

	if len(foundPorts) != len(openPorts) {
		t.Errorf("Expected %d open ports, got %d. Mismatch in count.", len(openPorts), len(foundPorts))
	}
}
