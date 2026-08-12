package main

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

func TestFetchURL(t *testing.T) {
	// Mock rationale: Using httptest.NewServer to simulate HTTP servers for deterministic testing.
	serverOK := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	}))
	defer serverOK.Close()

	serverDelayed := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(50 * time.Millisecond) // Simulate a delay
		w.WriteHeader(http.StatusOK)
	}))
	defer serverDelayed.Close()

	serverNotFound := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
	}))
	defer serverNotFound.Close()

	// Mock rationale: Creating a custom client with a short timeout to test timeout scenarios.
	clientTimeout := &http.Client{
		Timeout: 10 * time.Millisecond,
	}

	// Mock rationale: A server that will intentionally cause a connection error.
	// We can't directly mock connection errors with httptest, so we'll test the error handling path
	// by providing an invalid URL format that the http client will reject before making a request.
	// For a true connection error, one would need to manipulate network conditions or use a mock client.
	// For this test, we'll focus on URL parsing errors.
	invalidURL := "invalid-url-format"

	tests := []struct {
		name       string
		url        string
		client     *http.Client
		expStatus  int
		expErr     bool
		minDuration time.Duration // To check if duration is at least some value
	}{
		{"OK Server", serverOK.URL, &http.Client{Timeout: defaultTimeout}, http.StatusOK, false, 0 * time.Millisecond},
		{"Delayed Server", serverDelayed.URL, &http.Client{Timeout: defaultTimeout}, http.StatusOK, false, 40 * time.Millisecond},
		{"Not Found Server", serverNotFound.URL, &http.Client{Timeout: defaultTimeout}, http.StatusNotFound, false, 0 * time.Millisecond},
		{"Timeout Test", serverDelayed.URL, clientTimeout, 0, true, 0 * time.Millisecond},
		{"Invalid URL Format", invalidURL, &http.Client{Timeout: defaultTimeout}, 0, true, 0 * time.Millisecond},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var wg sync.WaitGroup
			results := make(chan FetchResult, 1)

			wg.Add(1)
			go fetchURL(tt.url, tt.client, &wg, results)
			wg.Wait()
			close(results)

			var result FetchResult
			select {
			case res := <-results:
				result = res
			case <-time.After(1 * time.Second): // Safety net for channel read
				t.Fatal("Timeout waiting for result")
			}

			if tt.expErr {
				if result.Error == nil {
					t.Errorf("fetchURL() error = %v, wantErr %v", result.Error, tt.expErr)
				}
			} else {
				if result.Error != nil {
					t.Errorf("fetchURL() unexpected error: %v", result.Error)
				}
				if result.StatusCode != tt.expStatus {
					t.Errorf("fetchURL() statusCode = %v, want %v", result.StatusCode, tt.expStatus)
				}
				if result.Duration < tt.minDuration {
					t.Errorf("fetchURL() duration = %v, want at least %v", result.Duration, tt.minDuration)
				}
			}
		})
	}
}

func TestMain_NoArgsStdin(t *testing.T) {
	// Mock rationale: Redirecting os.Args and os.Stdin to simulate no input.
	oldArgs := os.Args
	os.Args = []string{"concurrent-fetcher"}
	defer func() { os.Args = oldArgs }()

	// Capture stdout to check for the "No URLs provided" message.
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	defer func() { os.Stdout = oldStdout }()

	main()

	w.Close()
	output, _ := io.ReadAll(r)

	if !strings.Contains(string(output), "No URLs provided.") {
		t.Errorf("Expected 'No URLs provided.' message, but got: %s", string(output))
	}
}

// Helper to simulate reading from stdin for tests
func TestMain_StdinInput(t *testing.T) {
	// Mock rationale: Redirecting os.Args and os.Stdin to simulate input via stdin.
	oldArgs := os.Args
	os.Args = []string{"concurrent-fetcher"}
	defer func() { os.Args = oldArgs }()

	// Mock rationale: Using a string reader to simulate stdin.
	input := "https://example.com\nhttps://httpbin.org/status/200"
	oldStdin := os.Stdin
	os.Stdin = strings.NewReader(input)
	defer func() { os.Stdin = oldStdin }()

	// Capture stdout to check results.
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	defer func() { os.Stdout = oldStdout }()

	main()

	w.Close()
	output, _ := io.ReadAll(r)

	if !strings.Contains(string(output), "https://example.com: Status 200") {
		t.Errorf("Expected output for example.com, but got: %s", string(output))
	}
	if !strings.Contains(string(output), "https://httpbin.org/status/200: Status 200") {
		t.Errorf("Expected output for httpbin.org, but got: %s", string(output))
	}
}
