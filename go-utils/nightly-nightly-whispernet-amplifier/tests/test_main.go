package main

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

// Mock rationale: httptest.NewServer is used to create a local HTTP server
// that can be controlled by the test. This allows simulating various network
// conditions (success, failure, latency) without relying on actual external
// network requests, making tests deterministic and offline.

func TestCheckNode_Success(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Hello, WhisperNet!")
	}))
	defer ts.Close()

	results := make(chan NodeStatus, 1)
	checkNode(ts.URL, results)
	res := <-results

	if res.URL != ts.URL {
		t.Errorf("Expected URL %s, got %s", ts.URL, res.URL)
	}
	if res.Status != "Signal Strong" {
		t.Errorf("Expected status 'Signal Strong', got '%s'", res.Status)
	}
	if res.StatusCode != 200 {
		t.Errorf("Expected status code 200, got %d", res.StatusCode)
	}
	if res.Error != nil {
		t.Errorf("Expected no error, got %v", res.Error)
	}
	if res.Latency == 0 {
		t.Errorf("Expected non-zero latency")
	}
}

func TestCheckNode_NotFound(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		fmt.Fprintln(w, "404 Not Found")
	}))
	defer ts.Close()

	results := make(chan NodeStatus, 1)
	checkNode(ts.URL, results)
	res := <-results

	if res.Status != "Faint Echo (Client Error)" {
		t.Errorf("Expected status 'Faint Echo (Client Error)', got '%s'", res.Status)
	}
	if res.StatusCode != 404 {
		t.Errorf("Expected status code 404, got %d", res.StatusCode)
	}
	if res.Error != nil {
		t.Errorf("Expected no error, got %v", res.Error)
	}
}

func TestCheckNode_ServerError(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprintln(w, "500 Internal Server Error")
	}))
	defer ts.Close()

	results := make(chan NodeStatus, 1)
	checkNode(ts.URL, results)
	res := <-results

	if res.Status != "Lost in the Static (Server Error)" {
		t.Errorf("Expected status 'Lost in the Static (Server Error)', got '%s'", res.Status)
	}
	if res.StatusCode != 500 {
		t.Errorf("Expected status code 500, got %d", res.StatusCode)
	}
	if res.Error != nil {
		t.Errorf("Expected no error, got %v", res.Error)
	}
}

func TestCheckNode_Timeout(t *testing.T) {
	// Create a server that delays response longer than the client timeout
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(requestTimeout + 100*time.Millisecond) // Sleep longer than client timeout
		fmt.Fprintln(w, "Too slow!")
	}))
	defer ts.Close()

	results := make(chan NodeStatus, 1)
	checkNode(ts.URL, results)
	res := <-results

	if !strings.Contains(res.Status, "Faint Echo (Timeout)") {
		t.Errorf("Expected status to contain 'Faint Echo (Timeout)', got '%s'", res.Status)
	}
	if res.Error == nil {
		t.Errorf("Expected an error for timeout, got nil")
	}
	if !strings.Contains(res.Error.Error(), "context deadline exceeded") {
		t.Errorf("Expected error message to contain 'context deadline exceeded', got '%v'", res.Error)
	}
}

func TestRunFunction_SuccessAndFailure(t *testing.T) {
	var buf bytes.Buffer

	// Mock servers for main function test
	ts1 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "OK")
	}))
	defer ts1.Close()

	ts2 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		fmt.Fprintln(w, "Not Found")
	}))
	defer ts2.Close()

	// Simulate command line arguments
	args := []string{ts1.URL, ts2.URL, "http://localhost:9999"} // Last one will fail connection

	exitCode := run(args, &buf)
	output := buf.String()

	if exitCode != 0 {
		t.Errorf("Expected exit code 0, got %d", exitCode)
	}

	if !strings.Contains(output, "--- WhisperNet Signal Amplifier Report ---") {
		t.Errorf("Output missing header")
	}
	if !strings.Contains(output, fmt.Sprintf("Node: %s\n  Status: Signal Strong", ts1.URL)) {
		t.Errorf("Output missing success for %s", ts1.URL)
	}
	if !strings.Contains(output, fmt.Sprintf("Node: %s\n  Status: Faint Echo (Client Error)", ts2.URL)) {
		t.Errorf("Output missing 404 for %s", ts2.URL)
	}
	// The exact error message for localhost:9999 can vary (connection refused, timeout, etc.)
	// So we check for general failure status.
	if !strings.Contains(output, "Node: http://localhost:9999") ||
		(!strings.Contains(output, "Lost in the Static (Connection Refused)") &&
			!strings.Contains(output, "Faint Echo (Timeout)") &&
			!strings.Contains(output, "Lost in the Static (Network Error)")) {
		t.Errorf("Output missing expected failure for http://localhost:9999. Got:\n%s", output)
	}
	if !strings.Contains(output, "--- Scan Complete ---") {
		t.Errorf("Output missing footer")
	}
}

func TestRunFunction_NoArgs(t *testing.T) {
	var buf bytes.Buffer
	args := []string{} // No arguments

	exitCode := run(args, &buf)
	output := buf.String()

	if exitCode != 1 {
		t.Errorf("Expected exit code 1 for no arguments, got %d", exitCode)
	}
	if !strings.Contains(output, "Usage: nightly-whispernet-amplifier <URL1> [URL2]...") {
		t.Errorf("Expected usage message, got: %s", output)
	}
}
