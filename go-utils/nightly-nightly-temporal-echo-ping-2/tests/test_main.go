package main

import (
	"bytes"
	"flag"
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

// TestPingTargetSuccess verifies successful ping and latency measurement.
func TestPingTargetSuccess(t *testing.T) {
	// Mock rationale: httptest.NewServer creates a local HTTP server to simulate a network endpoint,
	// allowing deterministic and offline testing of network requests without actual internet access.
	testServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(50 * time.Millisecond) // Simulate network delay
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "OK")
	}))
	defer testServer.Close()

	results := make(chan PingResult, 1)
	pingTarget(testServer.URL, 1*time.Second, results)
	close(results)

	res := <-results

	if res.Error != nil {
		t.Errorf("Expected no error, got: %v", res.Error)
	}
	if res.Latency < 50*time.Millisecond || res.Latency > 200*time.Millisecond {
		t.Errorf("Expected latency around 50ms, got: %v", res.Latency)
	}
	if res.Target != testServer.URL {
		t.Errorf("Expected target %s, got %s", testServer.URL, res.Target)
	}
}

// TestPingTargetTimeout verifies that pingTarget correctly handles timeouts.
func TestPingTargetTimeout(t *testing.T) {
	// Mock rationale: httptest.NewServer simulates a server that delays its response beyond the client's timeout,
	// ensuring the timeout mechanism is correctly triggered and an error is reported.
	testServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(200 * time.Millisecond) // Longer than the 100ms timeout
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "OK")
	}))
	defer testServer.Close()

	results := make(chan PingResult, 1)
	pingTarget(testServer.URL, 100*time.Millisecond, results)
	close(results)

	res := <-results

	if res.Error == nil {
		t.Errorf("Expected a timeout error, got nil")
	}
	if !strings.Contains(res.Error.Error(), "timeout") {
		t.Errorf("Expected timeout error, got: %v", res.Error)
	}
}

// TestPingTargetConnectionRefused verifies handling of connection errors.
func TestPingTargetConnectionRefused(t *testing.T) {
	// Mock rationale: By closing the test server immediately, we simulate a connection refusal or an unavailable host,
	// allowing us to test how the utility handles such network errors.
	testServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// This handler won't even be reached if the connection is refused
	}))
	addr := testServer.URL
	testServer.Close() // Close the server immediately to simulate connection refused

	results := make(chan PingResult, 1)
	pingTarget(addr, 1*time.Second, results)
	close(results)

	res := <-results

	if res.Error == nil {
		t.Errorf("Expected a connection error, got nil")
	}
	if !strings.Contains(res.Error.Error(), "connect: connection refused") &&
	   !strings.Contains(res.Error.Error(), "connection reset by peer") &&
	   !strings.Contains(res.Error.Error(), "no connection could be made") {
		// Different OS/Go versions might yield slightly different errors for connection refused/reset
		t.Errorf("Expected connection error, got: %v", res.Error)
	}
}

// TestRunPings verifies that runPings executes multiple pings concurrently.
func TestRunPings(t *testing.T) {
	// Mock rationale: httptest.NewServer simulates a responsive endpoint. A WaitGroup ensures all goroutines complete.
	// The channel collects results, allowing verification of the number of pings executed.
	testServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(10 * time.Millisecond)
		w.WriteHeader(http.StatusOK)
	}))
	defer testServer.Close()

	const pingCount = 5
	results := make(chan PingResult, pingCount)
	var wg sync.WaitGroup

	wg.Add(1)
	go runPings(testServer.URL, pingCount, 1*time.Second, results, &wg)

	wg.Wait()
	close(results)

	if len(results) != pingCount {
		t.Errorf("Expected %d results, got %d", pingCount, len(results))
	}

	for res := range results {
		if res.Error != nil {
			t.Errorf("Expected no error, got %v", res.Error)
		}
	}
}

// TestMainFunctionIntegration verifies the main function's logic with mocked inputs and outputs.
func TestMainFunctionIntegration(t *testing.T) {
	// Mock rationale: flag.CommandLine is mocked to control command-line arguments programmatically.
	// os.Stdout is redirected to a bytes.Buffer to capture and inspect the console output.
	// httptest.NewServer is used to simulate multiple network targets with different behaviors (success, timeout, error).

	// Save original os.Args and os.Stdout, then restore them after test
	oldArgs := os.Args
	oldStdout := os.Stdout
	defer func() {
		os.Args = oldArgs
		os.Stdout = oldStdout
		flag.CommandLine = flag.NewFlagSet(oldArgs[0], flag.ExitOnError) // Reset flag package
	}()

	// Create a buffer to capture stdout
	var buf bytes.Buffer
	os.Stdout = io.MultiWriter(oldStdout, &buf)

	// Setup mock servers
	successServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(20 * time.Millisecond)
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "Success")
	}))
	defer successServer.Close()

	timeoutServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(500 * time.Millisecond) // Will timeout with 100ms timeout
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "Timeout")
	}))
	defer timeoutServer.Close()

	// Simulate command-line arguments
	os.Args = []string{
		"temporal-echo-ping",
		"-targets", fmt.Sprintf("%s,%s", successServer.URL, timeoutServer.URL),
		"-count", "2",
		"-timeout", "100ms",
	}

	// Reset the flag package for testing main
	flag.CommandLine = flag.NewFlagSet(os.Args[0], flag.ExitOnError)

	// Run main function
	main()

	output := buf.String()

	// Assertions on the captured output
	if !strings.Contains(output, "Initiating Temporal Echo Pings...") {
		t.Errorf("Output missing 'Initiating Temporal Echo Pings...'")
	}
	if !strings.Contains(output, fmt.Sprintf("--- Ping Statistics for %s ---", successServer.URL)) {
		t.Errorf("Output missing stats for success server")
	}
	if !strings.Contains(output, "Successful: 2") {
		t.Errorf("Output missing successful count for success server")
	}
	if !strings.Contains(output, fmt.Sprintf("--- Ping Statistics for %s ---", timeoutServer.URL)) {
		t.Errorf("Output missing stats for timeout server")
	}
	if !strings.Contains(output, "Failed: 2") {
		t.Errorf("Output missing failed count for timeout server")
	}
	if !strings.Contains(output, "timeout") {
		t.Errorf("Output missing timeout error message")
	}
	if !strings.Contains(output, "Temporal Echo Pings Complete.") {
		t.Errorf("Output missing 'Temporal Echo Pings Complete.'")
	}
}

// TestMainFunctionMissingTargets verifies that main exits with an error if targets are not provided.
func TestMainFunctionMissingTargets(t *testing.T) {
	// Mock rationale: os.Args is mocked to simulate missing command-line arguments.
	// os.Exit is mocked to prevent the test from terminating the test runner prematurely.
	// os.Stderr is redirected to capture error output.

	oldArgs := os.Args
	oldStderr := os.Stderr
	oldExit := exit
	defer func() {
		os.Args = oldArgs
		os.Stderr = oldStderr
		exit = oldExit
		flag.CommandLine = flag.NewFlagSet(oldArgs[0], flag.ExitOnError) // Reset flag package
	}()

	var buf bytes.Buffer
	os.Stderr = &buf

	exitCalled := false
	exit = func(code int) {
		exitCalled = true
		if code != 1 {
			t.Errorf("Expected exit code 1, got %d", code)
		}
		panic("os.Exit called") // Panic to stop execution without terminating test runner
	}

	os.Args = []string{"temporal-echo-ping"}
	flag.CommandLine = flag.NewFlagSet(os.Args[0], flag.ExitOnError)

	defer func() {
		if r := recover(); r == nil || r.(string) != "os.Exit called" {
			t.Errorf("Expected os.Exit to be called, but it wasn't or panic was different")
		}
	}()

	main()

	if !exitCalled {
		t.Errorf("Expected main to call os.Exit")
	}
	if !strings.Contains(buf.String(), "Error: -targets flag is required.") {
		t.Errorf("Expected error message about missing targets, got: %s", buf.String())
	}
}

// exit is a variable that can be overridden for testing os.Exit
var exit = os.Exit
