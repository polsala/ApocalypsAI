package main

import (
	"bytes"
	"fmt"
	"net"
	"testing"
	"time"
)

// mockUDPConn implements the net.Conn interface for testing purposes.
type mockUDPConn struct {
	bytes.Buffer
	readErr  error
	writeErr error
}

// Mock rationale: `net.Conn` is an interface. We implement a mock to capture
// written data and simulate errors without actual network I/O. This ensures
// deterministic and offline testing of the `sendBeacon` function.

func (m *mockUDPConn) Read(b []byte) (n int, err error) {
	if m.readErr != nil {
		return 0, m.readErr
	}
	return m.Buffer.Read(b)
}

func (m *mockUDPConn) Write(b []byte) (n int, err error) {
	if m.writeErr != nil {
		return 0, m.writeErr
	}
	return m.Buffer.Write(b)
}

func (m *mockUDPConn) Close() error { return nil }
func (m *mockUDPConn) LocalAddr() net.Addr { return nil }
func (m *mockUDPConn) RemoteAddr() net.Addr { return nil }
func (m *mockUDPConn) SetDeadline(t time.Time) error { return nil }
func (m *mockUDPConn) SetReadDeadline(t time.Time) error { return nil }
func (m *mockUDPConn) SetWriteDeadline(t time.Time) error { return nil }

func TestFormatTime(t *testing.T) {
	testTime := time.Date(2023, time.October, 27, 10, 30, 0, 123456789, time.UTC)
	expectedFormat := "2023-10-27T10:30:00.123456789Z"

	formattedTime := formatTime(testTime)
	if formattedTime != expectedFormat {
		t.Errorf("Expected formatted time '%s', got '%s'", expectedFormat, formattedTime)
	}

	// Test with different nanoseconds
	testTimeNano := time.Date(2023, time.October, 27, 10, 30, 0, 987654321, time.UTC)
	expectedFormatNano := "2023-10-27T10:30:00.987654321Z"
	formattedTimeNano := formatTime(testTimeNano)
	if formattedTimeNano != expectedFormatNano {
		t.Errorf("Expected formatted time '%s', got '%s'", expectedFormatNano, formattedTimeNano)
	}
}

func TestSendBeacon(t *testing.T) {
	mockConn := &mockUDPConn{}
	testTimeStr := "2023-10-27T10:30:00.123456789Z"

	err := sendBeacon(mockConn, testTimeStr)
	if err != nil {
		t.Fatalf("sendBeacon failed: %v", err)
	}

	if mockConn.String() != testTimeStr {
		t.Errorf("Expected '%s' to be written, got '%s'", testTimeStr, mockConn.String())
	}

	// Test with write error
	mockConn = &mockUDPConn{writeErr: fmt.Errorf("mock write error")}
	err = sendBeacon(mockConn, testTimeStr)
	if err == nil {
		t.Error("Expected error, got nil")
	}
	if err.Error() != "mock write error" {
		t.Errorf("Expected 'mock write error', got '%v'", err)
	}
}
