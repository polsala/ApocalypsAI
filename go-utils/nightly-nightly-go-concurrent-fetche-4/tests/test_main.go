package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
)

// MockRoundTripper is a mock for http.RoundTripper.
type MockRoundTripper struct {
	Response *http.Response
	Err      error
}

// RoundTrip implements the http.RoundTripper interface.
func (m *MockRoundTripper) RoundTrip(req *http.Request) (*http.Response, error) {
	// Mock rationale: Simulate network responses and errors without actual network calls.
	return m.Response, m.Err
}

func TestConcurrentFetcher(t *testing.T) {
	// Mock server setup
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Mock rationale: Serve different responses based on the request path.
		switch r.URL.Path {
		case "/success":
			w.WriteHeader(http.StatusOK)
			w.Write([]byte("OK"))
		case "/notfound":
			w.WriteHeader(http.StatusNotFound)
			w.Write([]byte("Not Found"))
		default:
			http.Error(w, "Not Found", http.StatusNotFound)
		}
	}))
	defer server.Close()

	// Save original os.Args and set mock arguments
	oldArgs := os.Args
	defer func() { os.Args = oldArgs }() // Restore original os.Args

	// Test cases
	tests := []struct {
		name      string
		urls      []string
		expected  string
		hasError  bool
	}{
		{
			name:     "All successful fetches",
			urls:     []string{server.URL + "/success", server.URL + "/success"},
			expected: "Fetching " + server.URL + "/success...\n  -> Success: 200 OK\nFetching " + server.URL + "/success...\n  -> Success: 200 OK\n",
			hasError: false,
		},
		{
			name:     "Mixed success and not found",
			urls:     []string{server.URL + "/success", server.URL + "/notfound"},
			expected: "Fetching " + server.URL + "/success...\n  -> Success: 200 OK\nFetching " + server.URL + "/notfound...\n  -> Success: 404 Not Found\n",
			hasError: false,
		},
		{
			name:     "Invalid URL (non-existent host)",
			urls:     []string{"http://invalid.host.local"},
			expected: "Fetching http://invalid.host.local...\n  -> Error: Get \"http://invalid.host.local\": dial tcp: lookup invalid.host.local: no such host\n",
			hasError: true,
		},
		{
			name:     "No URLs provided",
			urls:     []string{},
			expected: "Usage: concurrent-fetcher <url1> <url2> ...\n",
			hasError: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Prepare os.Args for the current test case
			// The first element is the program name, followed by URLs
			args := append([]string{"concurrent-fetcher"}, tt.urls...)
			os.Args = args

			// Capture stdout
			oldStdout := os.Stdout
			r, w, _ := os.Pipe()
			os.Stdout = w
			defer func() { os.Stdout = oldStdout }() // Restore stdout

			main() // Execute the main function

			w.Close() // Close the pipe writer to flush content
			capturedOutput, _ := ioutil.ReadAll(r)
			outputStr := string(capturedOutput)

			// Normalize output for comparison (remove trailing newline if present)
			outputStr = strings.TrimSuffix(outputStr, "\n")
			ttexpected := strings.TrimSuffix(tt.expected, "\n")

			if outputStr != ttexpected {
				t.Errorf("Test '%s' failed.\nExpected:\n%s\nGot:\n%s", tt.name, ttexpected, outputStr)
			}

			// Basic check for error presence if expected
			if tt.hasError && !strings.Contains(outputStr, "Error:") {
				t.Errorf("Test '%s' expected an error but did not find one in output.\nOutput:\n%s", tt.name, outputStr)
			}
		})
	}
}
