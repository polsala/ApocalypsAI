package main

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

// Mock rationale: We are mocking the HTTP server to control responses and simulate various scenarios (success, failure, slow responses) without relying on external network calls.
func TestConcurrentFetcher(t *testing.T) {
	// Mock server for successful responses
	sserverSuccess := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Success!"))
	}))
	defer serverSuccess.Close()

	// Mock server for non-success status codes
	serverFailStatus := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("Internal Server Error"))
	}))
	defer serverFailStatus.Close()

	// Mock server for slow responses (to test timeout)
	serverSlow := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(15 * time.Second) // Longer than client timeout
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Slow response"))
	}))
	defer serverSlow.Close()

	tests := []struct {
		name     string
		urls     []string
		expSuccess int
		expFail    int
		expFailMsg string // Substring to check in error messages
	}{
		{
			name:     "All successful",
			urls:     []string{serverSuccess.URL, serverSuccess.URL},
			expSuccess: 2,
			expFail:    0,
		},
		{
			name:     "One failure (status code)",
			urls:     []string{serverSuccess.URL, serverFailStatus.URL},
			expSuccess: 1,
			expFail:    1,
			expFailMsg: "received non-success status code: 500",
		},
		{
			name:     "One failure (timeout)",
			urls:     []string{serverSuccess.URL, serverSlow.URL},
			expSuccess: 1,
			expFail:    1,
			expFailMsg: "Client.Get failed: Get \"", // Check for generic client error due to timeout
		},
		{
			name:     "Invalid URL (DNS error)",
			urls:     []string{"http://nonexistent.domain.for.testing.xyz"},
			expSuccess: 0,
			expFail:    1,
			expFailMsg: "lookup nonexistent.domain.for.testing.xyz: no such host",
		},
		{
			name:     "Empty URL list",
			urls:     []string{}, // This case is handled by default URLs in main, but testing empty input is good.
			expSuccess: 2, // Based on default URLs
			expFail:    1, // Based on default URLs
			expFailMsg: "lookup invalid.domain.for.testing: no such host", // Based on default URLs
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Temporarily override os.Args to pass our test URLs
			originalArgs := os.Args
			
			// If it's the empty list test, we need to simulate no args passed to main
			if tt.name == "Empty URL list" {
				os.Args = []string{originalArgs[0]} // Only the program name
			} else {
				os.Args = append([]string{originalArgs[0]}, tt.urls...)
			}
			defer func() { os.Args = originalArgs }() // Restore original args

			// Capture stdout
			oldStdout := os.Stdout
			
			r, w, _ := os.Pipe()
			os.Stdout = w
			defer func() {
				os.Stdout = oldStdout
			}()

			main()

			w.Close()
			output, _ := io.ReadAll(r)
			outputStr := string(output)

			if strings.Contains(outputStr, fmt.Sprintf("Successful: %d", tt.expSuccess)) == false {
				t.Errorf("Test %s: Expected successful count %d, got output:\n%s", tt.name, tt.expSuccess, outputStr)
			}
			if strings.Contains(outputStr, fmt.Sprintf("Failed: %d", tt.expFail)) == false {
				t.Errorf("Test %s: Expected failed count %d, got output:\n%s", tt.name, tt.expFail, outputStr)
			}

			if tt.expFail > 0 {
				if strings.Contains(outputStr, tt.expFailMsg) == false {
					t.Errorf("Test %s: Expected failure message containing \"%s\", got output:\n%s", tt.name, tt.expFailMsg, outputStr)
				}
			}
		})
	}
}
