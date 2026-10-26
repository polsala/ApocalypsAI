package main

import (
	"errors"
	"io"
	"net"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// mockConn implements net.Conn for testing purposes.
type mockConn struct{}

func (m *mockConn) Read(b []byte) (n int, err error)         { return 0, nil }
func (m *mockConn) Write(b []byte) (n int, err error)        { return 0, nil }
func (m *mockConn) Close() error                             { return nil }
func (m *mockConn) LocalAddr() net.Addr                      { return &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 1234} }
func (m *mockConn) RemoteAddr() net.Addr                     { return &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 5678} }
func (m *mockConn) SetDeadline(t time.Time) error            { return nil }
func (m *mockConn) SetReadDeadline(t time.Time) error        { return nil }
func (m *mockConn) SetWriteDeadline(t time.Time) error       { return nil }

// TestPingTarget tests the pingTarget function with mocked network calls.
func TestPingTarget(t *testing.T) {
	// Mock rationale: We need to control network behavior for deterministic tests.
	// By replacing the global 'dialer' variable, we can simulate successful connections,
	// failed connections, and timeouts without actual network calls.

	// Store the original dialer to restore it after tests.
	originalDialer := dialer
	defer func() { dialer = originalDialer }()

	t.Run("successful connection", func(t *testing.T) {
		mockTarget := "example.com:80" // A dummy target for the mock

		// Replace the dialer with a mock that always succeeds for this target.
		dialer = func(network, address string, timeout time.Duration) (net.Conn, error) {
			if address == mockTarget {
				return &mockConn{}, nil // Return a dummy connection
			}
			return nil, errors.New("unexpected dial for " + address)
		}

		result := pingTarget(mockTarget, 1*time.Second)
		if result.Status != "Success" {
			t.Errorf("Expected Status 'Success', got '%s'", result.Status)
		}
		if result.Error != "" {
			t.Errorf("Expected no error, got '%s'", result.Error)
		}
		if result.Latency <= 0 {
			t.Errorf("Expected positive latency, got %s", result.Latency)
		}
	})

	t.Run("failed connection", func(t *testing.T) {
		mockTarget := "unreachable.host:80" // A dummy target for the mock
		mockError := errors.New("connection refused")

		// Replace the dialer with a mock that always fails for this target.
		dialer = func(network, address string, timeout time.Duration) (net.Conn, error) {
			if address == mockTarget {
				return nil, mockError
			}
			return nil, errors.New("unexpected dial for " + address)
		}

		result := pingTarget(mockTarget, 1*time.Second)
		if result.Status != "Failed" {
			t.Errorf("Expected Status 'Failed', got '%s'", result.Status)
		}
		if result.Error != mockError.Error() {
			t.Errorf("Expected error '%s', got '%s'", mockError.Error(), result.Error)
		}
		if result.Latency <= 0 {
			t.Errorf("Expected positive latency, got %s", result.Latency)
		}
	})

	t.Run("timeout connection", func(t *testing.T) {
		mockTarget := "slow.host:80" // A dummy target for the mock
		testTimeout := 10 * time.Millisecond

		// Replace the dialer with a mock that simulates a timeout.
		dialer = func(network, address string, timeout time.Duration) (net.Conn, error) {
			if address == mockTarget {
				// Simulate a delay longer than the test timeout
				time.Sleep(timeout + 5*time.Millisecond) // Ensure it's longer than the passed timeout
				return nil, errors.New("i/o timeout")    // Simulate timeout error
			}
			return nil, errors.New("unexpected dial for " + address)
		}

		result := pingTarget(mockTarget, testTimeout)
		if result.Status != "Failed" {
			t.Errorf("Expected Status 'Failed', got '%s'", result.Status)
		}
		if !strings.Contains(result.Error, "timeout") {
			t.Errorf("Expected timeout error, got '%s'", result.Error)
		}
		if result.Latency <= 0 {
			t.Errorf("Expected positive latency, got %s", result.Latency)
		}
		// The latency should be approximately the timeout duration, but can be slightly more due to scheduling.
		if result.Latency < testTimeout {
			t.Errorf("Expected latency to be at least timeout duration (%s), got %s", testTimeout, result.Latency)
		}
	})
}

// TestMainFunction tests the main function's argument parsing and output format.
// This requires capturing stdout and mocking pingTarget.
func TestMainFunction(t *testing.T) {
	// Mock rationale: To test the main function's behavior (argument parsing,
	// concurrency, output formatting) without making actual network calls,
	// we need to mock the underlying pingTarget function.
	// We also capture stdout to verify the printed output.

	// Store original os.Args and dialer
	oldArgs := os.Args
	originalDialer := dialer
	defer func() {
		os.Args = oldArgs
		dialer = originalDialer
	}()

	// Mock pingTarget to return predefined results
	mockPingResults := map[string]PingResult{
		"host1:80":  {Target: "host1:80", Status: "Success", Latency: 10 * time.Millisecond, Error: ""},
		"host2:443": {Target: "host2:443", Status: "Failed", Latency: 50 * time.Millisecond, Error: "connection refused"},
		"host3:22":  {Target: "host3:22", Status: "Success", Latency: 25 * time.Millisecond, Error: ""},
	}

	// Replace the dialer with a mock that uses mockPingResults
	dialer = func(network, address string, timeout time.Duration) (net.Conn, error) {
		if res, ok := mockPingResults[address]; ok {
			if res.Status == "Success" {
				return &mockConn{}, nil
			}
			return nil, errors.New(res.Error)
		}
		return nil, errors.New("unexpected dial for " + address)
	}

	// Capture stdout
	r, w, _ := os.Pipe()
	oldStdout := os.Stdout
	os.Stdout = w

	// Run main with mock arguments
	os.Args = []string{"nightly-echo-location-pinger", "host1:80", "host2:443", "host3:22", "--timeout=100ms"}
	main()

	w.Close()
	os.Stdout = oldStdout // Restore stdout
	out, _ := io.ReadAll(r)
	output := string(out)

	// Verify output contains expected lines (order might vary due to concurrency)
	expectedSubstrings := []string{
		"--- Echo-Location Report ---",
		"Target: host1:80              Status: Success  Latency: 10ms",
		"Target: host2:443             Status: Failed   Error: connection refused",
		"Target: host3:22              Status: Success  Latency: 25ms",
		"--------------------------",
	}

	for _, line := range expectedSubstrings {
		if !strings.Contains(output, line) {
			t.Errorf("Expected output to contain:\n%s\nBut got:\n%s", line, output)
		}
	}

	// Test case: No targets
	t.Run("no targets", func(t *testing.T) {
		r, w, _ := os.Pipe()
		oldStdout := os.Stdout
		os.Stdout = w
		oldExit := os.Exit
		defer func() {
			os.Stdout = oldStdout
			os.Exit = oldExit
		}()

		exitCalled := false
		os.Exit = func(code int) {
			exitCalled = true
			if code != 1 {
				t.Errorf("Expected exit code 1, got %d", code)
			}
			panic("os.Exit called") // Panic to stop execution without exiting the test runner
		}

		os.Args = []string{"nightly-echo-location-pinger", "--timeout=1s"}
		func() {
			defer func() {
				if r := recover(); r != nil && r.(string) != "os.Exit called" {
					panic(r) // Re-panic if it's not our expected panic
				}
			}()
			main()
		}()

		w.Close()
		out, _ := io.ReadAll(r)
		output := string(out)

		if !exitCalled {
			t.Errorf("Expected os.Exit to be called")
		}
		if !strings.Contains(output, "No targets specified") {
			t.Errorf("Expected 'No targets specified' message, got:\n%s", output)
		}
	})

	// Test case: Invalid timeout
	t.Run("invalid timeout", func(t *testing.T) {
		r, w, _ := os.Pipe()
		oldStdout := os.Stdout
		os.Stdout = w
		oldExit := os.Exit
		defer func() {
			os.Stdout = oldStdout
			os.Exit = oldExit
		}()

		exitCalled := false
		os.Exit = func(code int) {
			exitCalled = true
			if code != 1 {
				t.Errorf("Expected exit code 1, got %d", code)
			}
			panic("os.Exit called")
		}

		os.Args = []string{"nightly-echo-location-pinger", "host:80", "--timeout=invalid"}
		func() {
			defer func() {
				if r := recover(); r != nil && r.(string) != "os.Exit called" {
					panic(r)
				}
			}()
			main()
		}()

		w.Close()
		out, _ := io.ReadAll(r)
		output := string(out)

		if !exitCalled {
			t.Errorf("Expected os.Exit to be called")
		}
		if !strings.Contains(output, "Error parsing timeout duration 'invalid'") {
			t.Errorf("Expected 'Error parsing timeout duration' message, got:\n%s", output)
		}
	})
}
