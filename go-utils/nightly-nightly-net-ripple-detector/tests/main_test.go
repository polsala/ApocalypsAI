package main

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock rationale: httptest.NewServer is used to create a local HTTP server,
// simulating network targets without actual external network calls,
// ensuring deterministic and offline tests.
// Mock rationale: os.Exit is mocked to prevent tests from terminating the test runner,
// allowing assertion on the intended exit code.
// Mock rationale: os.Stdout is redirected to capture console output for verification,
// ensuring deterministic and offline output checks.

// Helper to capture os.Exit calls
var osExit = os.Exit

func TestProbeTarget_Success(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "OK")
	}))
	defer server.Close()

	results := make(chan RippleReport, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	probeTarget(server.URL, 1*time.Second, results, &wg, 100)
	wg.Wait()
	close(results)

	report := <-results
	if report.Target != server.URL {
		t.Errorf("Expected target %s, got %s", server.URL, report.Target)
	}
	if report.Status != "200 OK" {
		t.Errorf("Expected status '200 OK', got '%s'", report.Status)
	}
	if report.Error != nil {
		t.Errorf("Expected no error, got %v", report.Error)
	}
	if report.IsRipple {
		t.Errorf("Expected no ripple, but one was detected")
	}
	if !strings.Contains(report.Message, "stable resonance") {
		t.Errorf("Expected stable message, got '%s'", report.Message)
	}
}

func TestProbeTarget_HighLatencyRipple(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(200 * time.Millisecond) // Simulate high latency
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "OK")
	}))
	defer server.Close()

	results := make(chan RippleReport, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	// Set a low latency threshold (e.g., 50ms) to trigger a ripple
	probeTarget(server.URL, 1*time.Second, results, &wg, 50)
	wg.Wait()
	close(results)

	report := <-results
	if report.Target != server.URL {
		t.Errorf("Expected target %s, got %s", server.URL, report.Target)
	}
	if report.Status != "200 OK" {
		t.Errorf("Expected status '200 OK', got '%s'", report.Status)
	}
	if report.Error != nil {
		t.Errorf("Expected no error, got %v", report.Error)
	}
	if !report.IsRipple {
		t.Errorf("Expected a ripple due to high latency, but none was detected")
	}
	if !strings.Contains(report.Message, "temporal distortion") {
		t.Errorf("Expected temporal distortion message, got '%s'", report.Message)
	}
	if report.Latency.Milliseconds() < 200 {
		t.Errorf("Expected latency > 200ms, got %s", report.Latency)
	}
}

func TestProbeTarget_ErrorStatusRipple(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError) // Simulate error status
		fmt.Fprintln(w, "Internal Server Error")
	}))
	defer server.Close()

	results := make(chan RippleReport, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	probeTarget(server.URL, 1*time.Second, results, &wg, 100)
	wg.Wait()
	close(results)

	report := <-results
	if report.Target != server.URL {
		t.Errorf("Expected target %s, got %s", server.URL, report.Target)
	}
	if report.Status != "500 Internal Server Error" {
		t.Errorf("Expected status '500 Internal Server Error', got '%s'", report.Status)
	}
	if report.Error != nil {
		t.Errorf("Expected no connection error, got %v", report.Error)
	}
	if !report.IsRipple {
		t.Errorf("Expected a ripple due to error status, but none was detected")
	}
	if !strings.Contains(report.Message, "unstable resonance") {
		t.Errorf("Expected unstable resonance message, got '%s'", report.Message)
	}
}

func TestProbeTarget_ConnectionErrorRipple(t *testing.T) {
	invalidURL := "http://127.0.0.1:65535" // A port that is highly unlikely to be open

	results := make(chan RippleReport, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	probeTarget(invalidURL, 100*time.Millisecond, results, &wg, 100) // Short timeout to fail fast
	wg.Wait()
	close(results)

	report := <-results
	if report.Target != invalidURL {
		t.Errorf("Expected target %s, got %s", invalidURL, report.Target)
	}
	if report.Status != "ERROR" {
		t.Errorf("Expected status 'ERROR', got '%s'", report.Status)
	}
	if report.Error == nil {
		t.Errorf("Expected an error, got nil")
	}
	if !report.IsRipple {
		t.Errorf("Expected a ripple due to connection error, but none was detected")
	}
	if !strings.Contains(report.Message, "Failed to connect") {
		t.Errorf("Expected 'Failed to connect' message, got '%s'", report.Message)
	}
}

func TestProbeTarget_TimeoutRipple(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(500 * time.Millisecond) // Longer than probe timeout
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "OK")
	}))
	defer server.Close()

	results := make(chan RippleReport, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	// Set a short timeout (e.g., 100ms) to trigger a timeout error
	probeTarget(server.URL, 100*time.Millisecond, results, &wg, 100)
	wg.Wait()
	close(results)

	report := <-results
	if report.Target != server.URL {
		t.Errorf("Expected target %s, got %s", server.URL, report.Target)
	}
	if report.Status != "ERROR" { // Timeout results in an error status
		t.Errorf("Expected status 'ERROR', got '%s'", report.Status)
	}
	if report.Error == nil {
		t.Errorf("Expected a timeout error, got nil")
	}
	if !report.IsRipple {
		t.Errorf("Expected a ripple due to timeout, but none was detected")
	}
	// Check for common timeout error messages
	if !strings.Contains(report.Message, "Failed to connect") && !strings.Contains(report.Message, "context deadline exceeded") {
		t.Errorf("Expected timeout message, got '%s'", report.Message)
	}
}

func TestMainFunction_NoRipples(t *testing.T) {
	server1 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	}))
	defer server1.Close()

	server2 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	}))
	defer server2.Close()

	// Temporarily redirect os.Args and capture stdout
	oldArgs := os.Args
	defer func() { os.Args = oldArgs }()
	os.Args = []string{"nightly-net-ripple-detector", server1.URL, server2.URL, "--timeout=1000", "--threshold=100"}

	var buf bytes.Buffer
	oldStdout := os.Stdout
	os.Stdout = &buf
	defer func() { os.Stdout = oldStdout }() // Restore stdout

	// Mock os.Exit
	exitCode := 0
	originalOsExit := osExit
	osExit = func(code int) {
		exitCode = code
	}
	defer func() { osExit = originalOsExit }()

	main()

	output := buf.String()
	if !strings.Contains(output, "All network resonances are stable. No etheric ripples detected.") {
		t.Errorf("Expected 'No etheric ripples detected' message, got:\n%s", output)
	}
	if strings.Contains(output, "[RIPPLE DETECTED]") {
		t.Errorf("Unexpected ripple detected in output:\n%s", output)
	}
	if exitCode != 0 {
		t.Errorf("Expected exit code 0 (success), got %d", exitCode)
	}
}

func TestMainFunction_WithRipples(t *testing.T) {
	server1 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(200 * time.Millisecond) // High latency
		w.WriteHeader(http.StatusOK)
	}))
	defer server1.Close()

	server2 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError) // Error status
	}))
	defer server2.Close()

	// Temporarily redirect os.Args and capture stdout
	oldArgs := os.Args
	defer func() { os.Args = oldArgs }()
	os.Args = []string{"nightly-net-ripple-detector", server1.URL, server2.URL, "--timeout=1000", "--threshold=50"} // Low threshold

	var buf bytes.Buffer
	oldStdout := os.Stdout
	os.Stdout = &buf
	defer func() { os.Stdout = oldStdout }() // Restore stdout

	// Mock os.Exit
	exitCode := 0
	originalOsExit := osExit
	osExit = func(code int) {
		exitCode = code
	}
	defer func() { osExit = originalOsExit }()

	main()

	output := buf.String()
	if !strings.Contains(output, "Warning: One or more etheric ripples detected in the network fabric!") {
		t.Errorf("Expected 'etheric ripples detected' message, got:\n%s", output)
	}
	if !strings.Contains(output, "[RIPPLE DETECTED]") {
		t.Errorf("Expected '[RIPPLE DETECTED]' in output:\n%s", output)
	}
	if exitCode != 1 {
		t.Errorf("Expected exit code 1 (failure), got %d", exitCode)
	}
}

func TestMainFunction_NoTargets(t *testing.T) {
	oldArgs := os.Args
	defer func() { os.Args = oldArgs }()
	os.Args = []string{"nightly-net-ripple-detector"}

	var buf bytes.Buffer
	oldStdout := os.Stdout
	os.Stdout = &buf
	defer func() { os.Stdout = oldStdout }()

	exitCode := 0
	originalOsExit := osExit
	osExit = func(code int) {
		exitCode = code
	}
	defer func() { osExit = originalOsExit }()

	main()

	output := buf.String()
	if !strings.Contains(output, "No targets specified.") {
		t.Errorf("Expected 'No targets specified' message, got:\n%s", output)
	}
	if exitCode != 1 {
		t.Errorf("Expected exit code 1 (failure), got %d", exitCode)
	}
}

func TestMainFunction_InvalidArgs(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	}))
	defer server.Close()

	oldArgs := os.Args
	defer func() { os.Args = oldArgs }()
	os.Args = []string{"nightly-net-ripple-detector", server.URL, "--timeout=abc", "--threshold=-100"}

	var buf bytes.Buffer
	oldStdout := os.Stdout
	os.Stdout = &buf
	defer func() { os.Stdout = oldStdout }()

	exitCode := 0
	originalOsExit := osExit
	osExit = func(code int) {
		exitCode = code
	}
	defer func() { osExit = originalOsExit }()

	main()

	output := buf.String()
	if !strings.Contains(output, "Warning: Invalid timeout value 'abc'") {
		t.Errorf("Expected warning for invalid timeout, got:\n%s", output)
	}
	if !strings.Contains(output, "Warning: Invalid threshold value '-100'") {
		t.Errorf("Expected warning for invalid threshold, got:\n%s", output)
	}
	if !strings.Contains(output, "All network resonances are stable. No etheric ripples detected.") {
		t.Errorf("Expected success message despite warnings, got:\n%s", output)
	}
	if exitCode != 0 {
		t.Errorf("Expected exit code 0 (success), got %d", exitCode)
	}
}
