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

// MockDialer is a mock for net.Dialer to control connection behavior.
// Mock rationale: Replaces actual network calls with controlled responses for deterministic testing.
type MockDialer struct {
	MockConn net.Conn
	MockErr  error
	Timeout  time.Duration
}

func (md *MockDialer) DialTimeout(network, address string, timeout time.Duration) (net.Conn, error) {
	// Simulate timeout if specified and matches
	if md.Timeout > 0 && timeout != md.Timeout {
		return nil, fmt.Errorf("dial timeout mismatch: expected %v, got %v", md.Timeout, timeout)
	}
	return md.MockConn, md.MockErr
}

// MockConn is a mock for net.Conn.
// Mock rationale: Provides a dummy connection object that can be closed.
type MockConn struct {
	CloseFunc func() error
}

func (mc *MockConn) Read(b []byte) (n int, err error) { return 0, nil }
func (mc *MockConn) Write(b []byte) (n int, err error) { return 0, nil }
func (mc *MockConn) Close() error { 
	if mc.CloseFunc != nil {
		return mc.CloseFunc()
	}
	return nil 
}
func (mc *MockConn) LocalAddr() net.Addr { return nil }
func (mc *MockConn) RemoteAddr() net.Addr { return nil }
func (mc *MockConn) SetDeadline(t time.Time) error { return nil }
func (mc *MockConn) SetReadDeadline(t time.Time) error { return nil }
func (mc *MockConn) SetWriteDeadline(t time.Time) error { return nil }

// Replace the global net.DialTimeout with our mock for testing.
var originalDialTimeout = net.DialTimeout

func setupMockDialer(conn net.Conn, err error, timeout time.Duration) {
	net.DialTimeout = func(network, address string, timeout time.Duration) (net.Conn, error) {
		return (&MockDialer{MockConn: conn, MockErr: err, Timeout: timeout}).DialTimeout(network, address, timeout)
	}
}

func restoreDialTimeout() {
	net.DialTimeout = originalDialTimeout
}

func TestMain_SuccessfulProbes(t *testing.T) {
	// Mock a successful connection
	mockConn := &MockConn{}
	setupMockDialer(mockConn, nil, 2*time.Second)
	defer restoreDialTimeout()

	// Capture stdout
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Run the main function with mock arguments
	os.Args = []string{"./nightly-go-net-probe", "localhost:8080", "example.com:443"}
	main()

	w.Close()
	os.Stdout = oldStdout // Restore stdout

	var buf bytes.Buffer
	buf.ReadFrom(r)
	out := buf.String()

	if !strings.Contains(out, "Target: localhost:8080 | Reachable: true") {
		t.Errorf("Expected successful probe for localhost:8080, but got:\n%s", out)
	}
	if !strings.Contains(out, "Target: example.com:443 | Reachable: true") {
		t.Errorf("Expected successful probe for example.com:443, but got:\n%s", out)
	}

	// Check for latency presence (not exact value as it depends on execution time)
	if !strings.Contains(out, "Latency:") {
		t.Errorf("Expected latency to be reported, but got:\n%s", out)
	}
}

func TestMain_FailedProbes(t *testing.T) {
	// Mock a failed connection (connection refused)
	mockConn := &MockConn{}
	setupMockDialer(mockConn, fmt.Errorf("connection refused"), 2*time.Second)
	defer restoreDialTimeout()

	// Capture stdout
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Run the main function with mock arguments
	os.Args = []string{"./nightly-go-net-probe", "localhost:9999", "nonexistent.host:1234"}
	main()

	w.Close()
	os.Stdout = oldStdout // Restore stdout

	var buf bytes.Buffer
	buf.ReadFrom(r)
	out := buf.String()

	if !strings.Contains(out, "Target: localhost:9999 | Reachable: false | Error: connection refused") {
		t.Errorf("Expected failed probe for localhost:9999, but got:\n%s", out)
	}
	if !strings.Contains(out, "Target: nonexistent.host:1234 | Reachable: false | Error: connection refused") {
		t.Errorf("Expected failed probe for nonexistent.host:1234, but got:\n%s", out)
	}
}

func TestMain_MixedProbes(t *testing.T) {
	// Mock a mix of successful and failed probes
	var wg sync.WaitGroup
	results := make(chan ProbeResult, 3)

	// Successful probe
	mockConnSuccess := &MockConn{}
	setupMockDialer(mockConnSuccess, nil, 2*time.Second)
	wg.Add(1)
	go probeTarget("success.host:80", &wg, results)

	// Failed probe
	mockConnFail := &MockConn{}
	setupMockDialer(mockConnFail, fmt.Errorf("dial error"), 2*time.Second)
	wg.Add(1)
	go probeTarget("fail.host:80", &wg, results)

	// Another successful probe
	mockConnSuccess2 := &MockConn{}
	setupMockDialer(mockConnSuccess2, nil, 2*time.Second)
	wg.Add(1)
	go probeTarget("another.host:443", &wg, results)

	wg.Wait()
	close(results)

	// Capture stdout
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Re-run main logic to process results (this is a bit of a hack for testing)
	// In a real scenario, we'd test the result processing logic directly.
	// For this example, we'll just check the output of the main function.
	// We need to re-set os.Args to avoid issues if main was called before.
	os.Args = []string{"./nightly-go-net-probe", "success.host:80", "fail.host:80", "another.host:443"}
	main()

	w.Close()
	os.Stdout = oldStdout // Restore stdout

	var buf bytes.Buffer
	buf.ReadFrom(r)
	out := buf.String()

	if !strings.Contains(out, "Target: success.host:80 | Reachable: true") {
		t.Errorf("Expected successful probe for success.host:80, but got:\n%s", out)
	}
	if !strings.Contains(out, "Target: fail.host:80 | Reachable: false | Error: dial error") {
		t.Errorf("Expected failed probe for fail.host:80, but got:\n%s", out)
	}
	if !strings.Contains(out, "Target: another.host:443 | Reachable: true") {
		t.Errorf("Expected successful probe for another.host:443, but got:\n%s", out)
	}
}

func TestMain_NoArguments(t *testing.T) {
	// Capture stdout
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Run the main function with no arguments
	os.Args = []string{"./nightly-go-net-probe"}
	// Expecting os.Exit(1), so we need to handle that.
	// This is a common pattern for testing functions that call os.Exit.
	defer func() {
		if r := recover(); r != nil {
			// os.Exit(1) causes a panic, which we catch here.
			// We can assert that the exit code was 1 if needed, but for now,
			// we just ensure the program exited as expected.
		}
	}()

	main()

	w.Close()
	os.Stdout = oldStdout // Restore stdout

	var buf bytes.Buffer
	buf.ReadFrom(r)
	out := buf.String()

	if !strings.Contains(out, "Usage: nightly-go-net-probe <host1>:<port1> <host2>:<port2> ...") {
		t.Errorf("Expected usage message, but got:\n%s", out)
	}
}
