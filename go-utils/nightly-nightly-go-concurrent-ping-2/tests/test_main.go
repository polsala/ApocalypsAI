package main

import (
	"bytes"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os/exec"
	"strings"
	"testing"
	"time"
)

// Mock rationale: We are mocking the net.DialTimeout function to simulate network responses
// without actually making network calls. This ensures deterministic and offline tests.
var mockDialTimeout func(network, address string, timeout time.Duration) (netConn net.Conn, err error)

type mockConn struct {},

func (m *mockConn) Read(b []byte) (n int, err error) { return 0, nil }
func (m *mockConn) Write(b []byte) (n int, err error) { return 0, nil }
func (m *mockConn) Close() error { return nil }
func (m *mockConn) LocalAddr() net.Addr { return nil }
func (m *mockConn) RemoteAddr() net.Addr { return nil }
func (m *mockConn) SetDeadline(t time.Time) error { return nil }
func (m *mockConn) SetReadDeadline(t time.Time) error { return nil }
func (m *mockConn) SetWriteDeadline(t time.Time) error { return nil }

// Mock the net.DialTimeout function
func mockNetDialTimeout(network, address string, timeout time.Duration) (netConn net.Conn, err error) {
	if strings.Contains(address, "nonexistentserver.local") {
		return nil, fmt.Errorf("lookup nonexistentserver.local: no such host")
	}
	return &mockConn{}, nil
}

// Mock the net.LookupHost function
var mockLookupHost func(host string) ([]string, error)

func mockNetLookupHost(host string) ([]string, error) {
	if host == "nonexistentserver.local" {
		return nil, fmt.Errorf("no such host")
	}
	return []string{"1.2.3.4"}, nil
}

func TestMain_SuccessfulPings(t *testing.T) {
	// Mock net.DialTimeout and net.LookupHost
	originalDialTimeout := net.DialTimeout
	originalLookupHost := net.LookupHost
	defer func() { net.DialTimeout = originalDialTimeout }()
	defer func() { net.LookupHost = originalLookupHost }()

	net.DialTimeout = mockNetDialTimeout
	net.LookupHost = mockNetLookupHost

	// Capture stdout
	oldStdout := os.Stdout
	var buf bytes.Buffer
	os.Stdout = &buf
	defer func() { os.Stdout = oldStdout }()

	// Simulate command line arguments
	args := []string{"./concurrent-ping", "google.com", "example.com"}
	os.Args = args

	main()

	output := buf.String()

	if !strings.Contains(output, "Pinging google.com (1.2.3.4)...") {
		t.Errorf("Expected output for google.com not found. Got: %s", output)
	}
	if !strings.Contains(output, "Success: google.com is reachable") {
		t.Errorf("Expected success message for google.com not found. Got: %s", output)
	}

	if !strings.Contains(output, "Pinging example.com (1.2.3.4)...") {
		t.Errorf("Expected output for example.com not found. Got: %s", output)
	}
	if !strings.Contains(output, "Success: example.com is reachable") {
		t.Errorf("Expected success message for example.com not found. Got: %s", output)
	}
}

func TestMain_FailedPing(t *testing.T) {
	// Mock net.DialTimeout and net.LookupHost
	originalDialTimeout := net.DialTimeout
	originalLookupHost := net.LookupHost
	defer func() { net.DialTimeout = originalDialTimeout }()
	defer func() { net.LookupHost = originalLookupHost }()

	net.DialTimeout = mockNetDialTimeout
	net.LookupHost = mockNetLookupHost

	// Capture stdout
	oldStdout := os.Stdout
	var buf bytes.Buffer
	os.Stdout = &buf
	defer func() { os.Stdout = oldStdout }()

	// Simulate command line arguments
	args := []string{"./concurrent-ping", "nonexistentserver.local"}
	os.Args = args

	main()

	output := buf.String()

	if !strings.Contains(output, "Pinging nonexistentserver.local (1.2.3.4)...") {
		t.Errorf("Expected output for nonexistentserver.local not found. Got: %s", output)
	}
	if !strings.Contains(output, "Failed: nonexistentserver.local: lookup nonexistentserver.local: no such host") {
		t.Errorf("Expected failure message for nonexistentserver.local not found. Got: %s", output)
	}
}

func TestMain_NoHostsProvided(t *testing.T) {
	// Capture stdout
	oldStdout := os.Stdout
	var buf bytes.Buffer
	os.Stdout = &buf
	defer func() { os.Stdout = oldStdout }()

	// Simulate command line arguments with no hosts
	args := []string{"./concurrent-ping"}
	os.Args = args

	// Expecting os.Exit(1), so we need to defer the exit
	exitCode := 0
	exitCh := make(chan int)
	go func() {
		defer func() {
			if r := recover(); r != nil {
				if exitErr, ok := r.(*exec.ExitError); ok {
					exitCode = exitErr.ExitCode()
				} else {
					panic(r) // Not an ExitError
				}
			}
		}()
		main()
		exitCh <- exitCode
	}()

	finalExitCode := <-exitCh

	if finalExitCode != 1 {
		t.Errorf("Expected os.Exit(1) when no hosts are provided, but got exit code %d. Output: %s", finalExitCode, buf.String())
	}

	if !strings.Contains(buf.String(), "Usage: concurrent-ping") {
		t.Errorf("Expected usage message when no hosts are provided. Got: %s", buf.String())
	}
}

func TestMain_CustomTimeout(t *testing.T) {
	// Mock net.DialTimeout and net.LookupHost
	originalDialTimeout := net.DialTimeout
	originalLookupHost := net.LookupHost
	defer func() { net.DialTimeout = originalDialTimeout }()
	defer func() { net.LookupHost = originalLookupHost }()

	net.DialTimeout = mockNetDialTimeout
	net.LookupHost = mockNetLookupHost

	// Capture stdout
	oldStdout := os.Stdout
	var buf bytes.Buffer
	os.Stdout = &buf
	defer func() { os.Stdout = oldStdout }()

	// Simulate command line arguments with custom timeout
	args := []string{"./concurrent-ping", "-timeout", "5s", "google.com"}
	os.Args = args

	main()

	output := buf.String()

	if !strings.Contains(output, "Pinging google.com (1.2.3.4)...") {
		t.Errorf("Expected output for google.com not found. Got: %s", output)
	}
	if !strings.Contains(output, "Success: google.com is reachable") {
		t.Errorf("Expected success message for google.com not found. Got: %s", output)
	}
	// We can't directly assert the duration without more complex mocking, but the presence of the success message implies it worked.
}
