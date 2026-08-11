package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

// Mock rationale: These tests use httptest to create a local HTTP server that simulates responses.
// This allows for deterministic testing without relying on external network calls.

func TestConcurrentFetcher_Success(t *testing.T) {
	// Create a mock server that always returns 200 OK
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	}))
	defer server.Close()

	// Capture stdout to check the output
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Call the main function with the mock server URL
	// We need to temporarily replace os.Args to simulate command-line arguments
	oldArgs := os.Args
	os.Args = []string{"concurrent-fetcher", server.URL}

	main()

	// Restore stdout and os.Args
	w.Close()
	os.Stdout = oldStdout
	os.Args = oldArgs

	// Read the captured output
	output, _ := io.ReadAll(r)

	// Check if the output contains the expected summary
	outputStr := string(output)
	if !strings.Contains(outputStr, "Successful Fetches: 1") {
		t.Errorf("Expected successful fetch count not found. Output: %s", outputStr)
	}
	if !strings.Contains(outputStr, "Failed Fetches: 0") {
		t.Errorf("Expected failed fetch count not found. Output: %s", outputStr)
	}
	if !strings.Contains(outputStr, "Success Rate: 100.00%") {
		t.Errorf("Expected success rate not found. Output: %s", outputStr)
	}
}

func TestConcurrentFetcher_Failure_NonExistent(t *testing.T) {
	// Create a mock server that simulates a non-existent domain (will cause a network error)
	// We don't need a real server for this, as the client.Get will fail directly.

	// Capture stdout to check the output
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Call the main function with a non-existent URL
	oldArgs := os.Args
	os.Args = []string{"concurrent-fetcher", "http://nonexistent.invalid.local"}

	main()

	// Restore stdout and os.Args
	w.Close()
	os.Stdout = oldStdout
	os.Args = oldArgs

	// Read the captured output
	output, _ := io.ReadAll(r)

	// Check if the output contains the expected summary
	outputStr := string(output)
	if !strings.Contains(outputStr, "Successful Fetches: 0") {
		t.Errorf("Expected successful fetch count not found. Output: %s", outputStr)
	}
	if !strings.Contains(outputStr, "Failed Fetches: 1") {
		t.Errorf("Expected failed fetch count not found. Output: %s", outputStr)
	}
	if !strings.Contains(outputStr, "Failure Rate: 100.00%") {
		t.Errorf("Expected failure rate not found. Output: %s", outputStr)
	}
	if !strings.Contains(outputStr, "http://nonexistent.invalid.local") {
		t.Errorf("Expected failed URL not found in output. Output: %s", outputStr)
	}
}

func TestConcurrentFetcher_Failure_BadStatus(t *testing.T) {
	// Create a mock server that returns a 404 Not Found
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("Not Found"))
	}))
	defer server.Close()

	// Capture stdout to check the output
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Call the main function with the mock server URL
	oldArgs := os.Args
	os.Args = []string{"concurrent-fetcher", server.URL}

	main()

	// Restore stdout and os.Args
	w.Close()
	os.Stdout = oldStdout
	os.Args = oldArgs

	// Read the captured output
	output, _ := io.ReadAll(r)

	// Check if the output contains the expected summary
	outputStr := string(output)
	if !strings.Contains(outputStr, "Successful Fetches: 0") {
		t.Errorf("Expected successful fetch count not found. Output: %s", outputStr)
	}
	if !strings.Contains(outputStr, "Failed Fetches: 1") {
		t.Errorf("Expected failed fetch count not found. Output: %s", outputStr)
	}
	if !strings.Contains(outputStr, "Failure Rate: 100.00%") {
		t.Errorf("Expected failure rate not found. Output: %s", outputStr)
	}
	if !strings.Contains(outputStr, "non-2xx status code: 404") {
		t.Errorf("Expected bad status code message not found. Output: %s", outputStr)
	}
}

func TestConcurrentFetcher_MixedResults(t *testing.T) {
	// Create a mock server for success
	ssuccessServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	}))
	defer successServer.Close()

	// Create a mock server for failure (404)
	failureServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("Not Found"))
	}))
	defer failureServer.Close()

	// Capture stdout to check the output
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Call the main function with mixed URLs
	oldArgs := os.Args
	os.Args = []string{"concurrent-fetcher", successServer.URL, "http://nonexistent.invalid.local", failureServer.URL}

	main()

	// Restore stdout and os.Args
	w.Close()
	os.Stdout = oldStdout
	os.Args = oldArgs

	// Read the captured output
	output, _ := io.ReadAll(r)

	// Check if the output contains the expected summary
	outputStr := string(output)
	if !strings.Contains(outputStr, "Total URLs: 3") {
		t.Errorf("Expected total URLs not found. Output: %s", outputStr)
	}
	if !strings.Contains(outputStr, "Successful Fetches: 1") {
		t.Errorf("Expected successful fetch count not found. Output: %s", outputStr)
	}
	if !strings.Contains(outputStr, "Failed Fetches: 2") {
		t.Errorf("Expected failed fetch count not found. Output: %s", outputStr)
	}
	if !strings.Contains(outputStr, "Success Rate: 33.33%") {
		t.Errorf("Expected success rate not found. Output: %s", outputStr)
	}
	if !strings.Contains(outputStr, "Failure Rate: 66.67%") {
		t.Errorf("Expected failure rate not found. Output: %s", outputStr)
	}
	if !strings.Contains(outputStr, "http://nonexistent.invalid.local") {
		t.Errorf("Expected nonexistent URL not found in failed list. Output: %s", outputStr)
	}
	if !strings.Contains(outputStr, "non-2xx status code: 404") {
		t.Errorf("Expected bad status code message not found. Output: %s", outputStr)
	}
}

func TestConcurrentFetcher_NoURLs(t *testing.T) {
	// Capture stdout to check the output
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Call the main function with no URLs
	oldArgs := os.Args
	os.Args = []string{"concurrent-fetcher"}

	// Expecting the program to exit with an error message
	// We can't directly test os.Exit in Go without more complex setups, 
	// but we can check that the output is the usage message.
	main()

	// Restore stdout and os.Args
	w.Close()
	os.Stdout = oldStdout
	os.Args = oldArgs

	output, _ := io.ReadAll(r)

	if !strings.Contains(string(output), "Usage: concurrent-fetcher <url1> <url2> ...") {
		t.Errorf("Expected usage message not found. Output: %s", string(output))
	}
}
