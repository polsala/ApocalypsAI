package main

import (
	"bytes"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
)

func TestConcurrentFetcher(t *testing.T) {
	// Mock HTTP server
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Mock rationale: Simulate different status codes and delays
		switch r.URL.Path {
		case "/success":
			w.WriteHeader(http.StatusOK)
			fmt.Fprintln(w, "Success!")
		case "/notfound":
			w.WriteHeader(http.StatusNotFound)
			fmt.Fprintln(w, "Not Found")
		case "/slow":
			time.Sleep(100 * time.Millisecond) // Simulate a slow response
			w.WriteHeader(http.StatusOK)
			fmt.Fprintln(w, "Slow Response")
		default:
			w.WriteHeader(http.StatusInternalServerError)
		}
	}))
	defer server.Close()

	// Test cases
	tests := []struct {
		name      string
		urls      []string
		expected  string
		expectErr bool
	}{
		{
			name: "Single Success URL",
			urls: []string{server.URL + "/success"},
			expected: "URL: " + server.URL + "/success, Status: 200, Duration: ",
			expectErr: false,
		},
		{
			name: "Multiple URLs (Success, Not Found)",
			urls: []string{server.URL + "/success", server.URL + "/notfound"},
			expected: "URL: " + server.URL + "/success, Status: 200, Duration: " + "\n" + "URL: " + server.URL + "/notfound, Status: 404, Duration: ",
			expectErr: false,
		},
		{
			name: "URL with Error (Non-existent domain)",
			urls: []string{"http://nonexistent.domain.invalid"},
			expected: "URL: http://nonexistent.domain.invalid, Error: Get http://nonexistent.domain.invalid: dial tcp: lookup nonexistent.domain.invalid: no such host",
			expectErr: true,
		},
		{
			name: "Mixed URLs (Success, Slow, Error)",
			urls: []string{server.URL + "/success", server.URL + "/slow", "http://another.invalid.domain"},
			expected: "URL: " + server.URL + "/success, Status: 200, Duration: " + "\n" + "URL: " + server.URL + "/slow, Status: 200, Duration: " + "\n" + "URL: http://another.invalid.domain, Error: Get http://another.invalid.domain: dial tcp: lookup another.invalid.domain: no such host",
			expectErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Redirect stdout to capture output
			oldStdout := os.Stdout
			defer func() { os.Stdout = oldStdout }()
			stdoutBuffer := new(bytes.Buffer)
			os.Stdout = stdoutBuffer

			// Save original args and set new ones
			oldArgs := os.Args
			defer func() { os.Args = oldArgs }()
			os.Args = append([]string{os.Args[0]}, tt.urls...)

			main()

			output := stdoutBuffer.String()

			// Check for expected output, ignoring duration as it's variable
			for _, line := range strings.Split(tt.expected, "\n") {
				if !strings.Contains(output, line) {
					t.Errorf("Expected output line \"%s\" not found in output:\n%s", line, output)
				}
			}

			// Basic check for error presence/absence
			containsError := strings.Contains(output, "Error:")
			if tt.expectErr && !containsError {
				t.Errorf("Expected an error, but none was found in output:\n%s", output)
			}
			if !tt.expectErr && containsError {
				t.Errorf("Did not expect an error, but one was found in output:\n%s", output)
			}
		})
	}
}
