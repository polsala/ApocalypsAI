package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
	"time"
)

// TestPingURL_Success tests a successful ping to a mock server.
func TestPingURL_Success(t *testing.T) {
	// Mock rationale: We need a deterministic network endpoint to test pingURL.
	// httptest.NewServer provides a local HTTP server that we can control.
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(50 * time.Millisecond) // Simulate network latency
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "OK")
	}))
	defer server.Close()

	result := pingURL(server.URL)

	if result.Err != nil {
		t.Fatalf("Expected no error, got: %v", result.Err)
	}
	// Allow some buffer for test execution, but ensure it's around 50ms
	if result.Latency < 40*time.Millisecond || result.Latency > 100*time.Millisecond {
		t.Errorf("Expected latency around 50ms, got: %v", result.Latency)
	}
	if result.URL != server.URL {
		t.Errorf("Expected URL %s, got %s", server.URL, result.URL)
	}
}

// TestPingURL_NotFound tests pinging a non-existent path on a mock server.
func TestPingURL_NotFound(t *testing.T) {
	// Mock rationale: Simulating a 404 response from a controlled server.
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		fmt.Fprintln(w, "Not Found")
	}))
	defer server.Close()

	result := pingURL(server.URL)

	if result.Err == nil {
		t.Fatalf("Expected an error for 404 status, got nil")
	}
	if !strings.Contains(result.Err.Error(), "non-OK status code 404") {
		t.Errorf("Expected 'non-OK status code 404' error, got: %v", result.Err)
	}
}

// TestPingURL_NetworkError tests a simulated network error (e.g., connection refused).
func TestPingURL_NetworkError(t *testing.T) {
	// Mock rationale: Testing how pingURL handles an unreachable host.
	// We use a URL that is highly unlikely to be a valid HTTP server.
	// This is an integration-like test, but still deterministic as it expects a connection error.
	invalidURL := "http://localhost:99999" // Port 99999 is almost certainly not in use

	result := pingURL(invalidURL)

	if result.Err == nil {
		t.Fatalf("Expected a network error, got nil")
	}
	// Check for common connection error messages across different OS/Go versions.
	if !strings.Contains(result.Err.Error(), "connect: connection refused") &&
	   !strings.Contains(result.Err.Error(), "connection refused") &&
	   !strings.Contains(result.Err.Error(), "no connection could be made") && // Windows error message
	   !strings.Contains(result.Err.Error(), "dial tcp") { // Generic dial error
		t.Errorf("Expected connection error, got: %v", result.Err)
	}
}

// TestMainFunction tests the main function's output and concurrency.
func TestMainFunction(t *testing.T) {
	// Mock rationale: We need to capture stdout and provide mock URLs for the main function.
	// httptest.NewServer allows us to simulate multiple concurrent endpoints.

	server1 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(20 * time.Millisecond)
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "Server 1 OK")
	}))
	defer server1.Close()

	server2 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(40 * time.Millisecond)
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "Server 2 OK")
	}))
	defer server2.Close()

	// Capture stdout
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Set up command-line arguments
	oldArgs := os.Args
	os.Args = []string{"main", server1.URL, server2.URL}

	main()

	// Restore stdout and args
	w.Close()
	os.Stdout = oldStdout
	os.Args = oldArgs

	out, _ := ioutil.ReadAll(r)
	output := string(out)

	// Check for expected output patterns
	if !strings.Contains(output, "--- Initiating Echo-Location Pings ---") {
		t.Errorf("Expected 'Initiating Echo-Location Pings' in output, got:\n%s", output)
	}
	if !strings.Contains(output, fmt.Sprintf("Pinging %s...", server1.URL)) {
		t.Errorf("Expected ping message for server 1, got:\n%s", output)
	}
	if !strings.Contains(output, fmt.Sprintf("Pinging %s...", server2.URL)) {
		t.Errorf("Expected ping message for server 2, got:\n%s", output)
	}
	if !strings.Contains(output, "--- Echo-Location Report ---") {
		t.Errorf("Expected 'Echo-Location Report' in output, got:\n%s", output)
	}
	if !strings.Contains(output, fmt.Sprintf("%s: ", server1.URL)) {
		t.Errorf("Expected result for server 1, got:\n%s", output)
	}
	if !strings.Contains(output, fmt.Sprintf("%s: ", server2.URL)) {
		t.Errorf("Expected result for server 2, got:\n%s", output)
	}

	// Ensure both URLs are mentioned in the report section
	reportStart := strings.Index(output, "--- Echo-Location Report ---")
	reportEnd := strings.Index(output, "----------------------------")
	if reportStart == -1 || reportEnd == -1 || reportStart >= reportEnd {
		t.Fatalf("Could not find report section in output:\n%s", output)
	}
	reportSection := output[reportStart:reportEnd]

	if !strings.Contains(reportSection, server1.URL) {
		t.Errorf("Server 1 URL not found in report section:\n%s", reportSection)
	}
	if !strings.Contains(reportSection, server2.URL) {
		t.Errorf("Server 2 URL not found in report section:\n%s", reportSection)
	}
}

// TestMainFunction_NoArgs tests the main function with no arguments.
func TestMainFunction_NoArgs(t *testing.T) {
	// Mock rationale: Capture stdout to verify the usage message and exit code.
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	oldArgs := os.Args
	os.Args = []string{"main"}

	exitCode := 0
	originalOsExit := osExit
	osExit = func(code int) {
		exitCode = code
	}
	defer func() { osExit = originalOsExit }() // Ensure osExit is restored

	main()

	w.Close()
	os.Stdout = oldStdout
	os.Args = oldArgs

	out, _ := ioutil.ReadAll(r)
	output := string(out)

	if !strings.Contains(output, "Usage: go run src/main.go <url1> [url2]...") {
		t.Errorf("Expected usage message, got:\n%s", output)
	}
	if exitCode != 1 {
		t.Errorf("Expected exit code 1, got %d", exitCode)
	}
}

// osExit is a variable that can be overridden for testing os.Exit
var osExit = os.Exit
