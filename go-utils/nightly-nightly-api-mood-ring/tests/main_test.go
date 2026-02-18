package main

import (
	"bytes"
	"errors"
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

// Mock rationale: httptest.NewServer is used to create a local, in-memory HTTP server
// that can be controlled deterministically. This allows simulating various API responses
// (status codes, delays, errors) without making actual network calls, ensuring tests are
// fast, reliable, and isolated from external factors.

func TestDetermineMood(t *testing.T) {
	tests := []struct {
		name       string
		statusCode int
		latency    time.Duration
		err        error
		expected   string
	}{
		{"Serene", 200, 50 * time.Millisecond, nil, "Serene"},
		{"Content", 200, 250 * time.Millisecond, nil, "Content"},
		{"Sluggish", 200, 600 * time.Millisecond, nil, "Sluggish"},
		{"Confused", 404, 10 * time.Millisecond, nil, "Confused"},
		{"Furious", 500, 10 * time.Millisecond, nil, "Furious"},
		{"Mysterious", 302, 10 * time.Millisecond, nil, "Mysterious"},
		{"SilentTimeout", 0, 0, errors.New("Get \"http://example.com\": context deadline exceeded (Client.Timeout exceeded while awaiting headers)"), "Silent (Timeout)"},
		{"SilentConnectionError", 0, 0, errors.New("Get \"http://example.com\": dial tcp 127.0.0.1:80: connect: connection refused"), "Silent (Connection Error)"},
		{"SilentGenericError", 0, 0, errors.New("some other error"), "Silent (Error: some other error)"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			actual := determineMood(tt.statusCode, tt.latency, tt.err)
			if actual != tt.expected {
				t.Errorf("determineMood(%d, %v, %v) = %q; want %q", tt.statusCode, tt.latency, tt.err, actual, tt.expected)
			}
		})
	}
}

func TestCheckAPI(t *testing.T) {
	// Mock rationale: httptest.NewServer provides a controlled HTTP endpoint for testing network interactions.
	// This allows simulating various server behaviors (status codes, delays) without actual external dependencies.

	// Test 1: Success and fast response
	t.Run("SuccessFast", func(t *testing.T) {
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			w.WriteHeader(http.StatusOK)
			fmt.Fprint(w, "OK")
		}))
		defer server.Close()

		results := make(chan Mood, 1)
		var wg sync.WaitGroup
		wg.Add(1)

		client := &http.Client{Timeout: 1 * time.Second}
		checkAPI(server.URL, client, results, &wg)
		wg.Wait()
		close(results)

		mood := <-results
		if mood.StatusCode != http.StatusOK {
			t.Errorf("Expected status %d, got %d", http.StatusOK, mood.StatusCode)
		}
		if mood.Description != "Serene" {
			t.Errorf("Expected mood \"Serene\", got \"%s\"", mood.Description)
		}
		if mood.Error != nil {
			t.Errorf("Expected no error, got %v", mood.Error)
		}
	})

	// Test 2: Success and slow response
	t.Run("SuccessSlow", func(t *testing.T) {
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			time.Sleep(600 * time.Millisecond) // Simulate delay
			w.WriteHeader(http.StatusOK)
			fmt.Fprint(w, "OK")
		}))
		defer server.Close()

		results := make(chan Mood, 1)
		var wg sync.WaitGroup
		wg.Add(1)

		client := &http.Client{Timeout: 1 * time.Second}
		checkAPI(server.URL, client, results, &wg)
		wg.Wait()
		close(results)

		mood := <-results
		if mood.StatusCode != http.StatusOK {
			t.Errorf("Expected status %d, got %d", http.StatusOK, mood.StatusCode)
		}
		if mood.Description != "Sluggish" {
			t.Errorf("Expected mood \"Sluggish\", got \"%s\"", mood.Description)
		}
		if mood.Error != nil {
			t.Errorf("Expected no error, got %v", mood.Error)
		}
	})

	// Test 3: Not Found (404)
	t.Run("NotFound", func(t *testing.T) {
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			w.WriteHeader(http.StatusNotFound)
			fmt.Fprint(w, "Not Found")
		}))
		defer server.Close()

		results := make(chan Mood, 1)
		var wg sync.WaitGroup
		wg.Add(1)

		client := &http.Client{Timeout: 1 * time.Second}
		checkAPI(server.URL, client, results, &wg)
		wg.Wait()
		close(results)

		mood := <-results
		if mood.StatusCode != http.StatusNotFound {
			t.Errorf("Expected status %d, got %d", http.StatusNotFound, mood.StatusCode)
		}
		if mood.Description != "Confused" {
			t.Errorf("Expected mood \"Confused\", got \"%s\"", mood.Description)
		}
		if mood.Error != nil {
			t.Errorf("Expected no error, got %v", mood.Error)
		}
	})

	// Test 4: Server Error (500)
	t.Run("ServerError", func(t *testing.T) {
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			w.WriteHeader(http.StatusInternalServerError)
			fmt.Fprint(w, "Internal Server Error")
		}))
		defer server.Close()

		results := make(chan Mood, 1)
		var wg sync.WaitGroup
		wg.Add(1)

		client := &http.Client{Timeout: 1 * time.Second}
		checkAPI(server.URL, client, results, &wg)
		wg.Wait()
		close(results)

		mood := <-results
		if mood.StatusCode != http.StatusInternalServerError {
			t.Errorf("Expected status %d, got %d", http.StatusInternalServerError, mood.StatusCode)
		}
		if mood.Description != "Furious" {
			t.Errorf("Expected mood \"Furious\", got \"%s\"", mood.Description)
		}
		if mood.Error != nil {
			t.Errorf("Expected no error, got %v", mood.Error)
		}
	})

	// Test 5: Timeout
	t.Run("Timeout", func(t *testing.T) {
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			time.Sleep(200 * time.Millisecond) // Longer than client timeout
			fmt.Fprint(w, "Too slow")
		}))
		defer server.Close()

		results := make(chan Mood, 1)
		var wg sync.WaitGroup
		wg.Add(1)

		client := &http.Client{Timeout: 100 * time.Millisecond}
		checkAPI(server.URL, client, results, &wg)
		wg.Wait()
		close(results)

		mood := <-results
		if mood.Error == nil || !strings.Contains(mood.Error.Error(), "timeout") {
			t.Errorf("Expected timeout error, got %v", mood.Error)
		}
		if mood.Description != "Silent (Timeout)" {
			t.Errorf("Expected mood \"Silent (Timeout)\", got \"%s\"", mood.Description)
		}
	})
}

func TestMainFunction(t *testing.T) {
	// Mock rationale: For testing the main function's output and argument parsing,
	// we redirect os.Stdout and os.Stdin to capture output and provide input programmatically.
	// The actual HTTP requests are handled by mock servers created with httptest.NewServer
	// to ensure determinism and isolation from external network conditions.

	// Save original os.Stdout and os.Stdin
	oldStdout := os.Stdout
	oldStdin := os.Stdin
	defer func() {
		os.Stdout = oldStdout
		os.Stdin = oldStdin
	}()

	// Create mock HTTP servers for the URLs
	server1 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "OK")
	}))
	defer server1.Close()

	server2 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprint(w, "Error")
	}))
	defer server2.Close()

	// Test 1: URLs from file
	t.Run("FromFile", func(t *testing.T) {
		// Create a temporary URL file
		urlsContent := fmt.Sprintf("%s\n%s\n", server1.URL, server2.URL)
		urlFile, err := os.CreateTemp("", "urls-*.txt")
		if err != nil {
			t.Fatalf("Failed to create temp file: %v", err)
		}
		defer os.Remove(urlFile.Name())
		urlFile.WriteString(urlsContent)
		urlFile.Close()

		// Capture stdout
		var buf bytes.Buffer
		os.Stdout = &buf

		// Set command-line arguments
		os.Args = []string{"main", "-urls", urlFile.Name(), "-timeout", "1s"}

		// Run main function
		main()

		output := buf.String()
		if !strings.Contains(output, "URL: "+server1.URL) || !strings.Contains(output, "Mood: Serene") {
			t.Errorf("Expected output for %s (Serene), got:\n%s", server1.URL, output)
		}
		if !strings.Contains(output, "URL: "+server2.URL) || !strings.Contains(output, "Mood: Furious") {
			t.Errorf("Expected output for %s (Furious), got:\n%s", server2.URL, output)
		}
	})

	// Test 2: URLs from stdin
	t.Run("FromStdin", func(t *testing.T) {
		// Provide stdin content
		input := fmt.Sprintf("%s\n%s\n", server1.URL, server2.URL)
		os.Stdin = io.NopCloser(bytes.NewBufferString(input))

		// Capture stdout
		var buf bytes.Buffer
		os.Stdout = &buf

		// Set command-line arguments (no -urls flag)
		os.Args = []string{"main", "-timeout", "1s"}

		// Run main function
		main()

		output := buf.String()
		if !strings.Contains(output, "URL: "+server1.URL) || !strings.Contains(output, "Mood: Serene") {
			t.Errorf("Expected output for %s (Serene), got:\n%s", server1.URL, output)
		}
		if !strings.Contains(output, "URL: "+server2.URL) || !strings.Contains(output, "Mood: Furious") {
			t.Errorf("Expected output for %s (Furious), got:\n%s", server2.URL, output)
		}
	})

	// Test 3: No URLs provided
	t.Run("NoURLs", func(t *testing.T) {
		// Provide empty stdin
		os.Stdin = io.NopCloser(bytes.NewBufferString(""))

		// Capture stdout
		var buf bytes.Buffer
		os.Stdout = &buf

		// Set command-line arguments (no -urls flag)
		os.Args = []string{"main"}

		// Capture os.Exit calls
		exitCalled := false
		oldOsExit := os.Exit
		defer func() { os.Exit = oldOsExit }()
		os.Exit = func(code int) {
			exitCalled = true
			if code != 0 {
				t.Errorf("Expected os.Exit(0) for no URLs, got %d", code)
			}
			panic("os.Exit was called") // Panic to stop execution without exiting the test runner
		}

		defer func() {
			if r := recover(); r != nil && r.(string) != "os.Exit was called" {
				t.Fatalf("Unexpected panic: %v", r)
			}
		}()

		main()

		output := buf.String()
		if !strings.Contains(output, "No URLs provided") {
			t.Errorf("Expected 'No URLs provided' message, got:\n%s", output)
		}
		if !exitCalled {
			t.Error("Expected os.Exit to be called")
		}
	})
}
