package main

import (
	"context"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

// Mock rationale: Using httptest to create a local HTTP server for deterministic testing.
func TestFetchURL_Success(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Hello, client!"))
	}))
	defer server.Close()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	results := make(chan FetchResult, 1)

	go fetchURL(ctx, server.URL, results, 1*time.Second)

	select {
	case res := <-results:
		if res.Status != "Success" {
			t.Errorf("Expected status 'Success', got '%s'", res.Status)
		}
		if res.Err != nil {
			t.Errorf("Expected no error, got '%v'", res.Err)
		}
		if res.Duration > 1*time.Second {
			t.Errorf("Expected duration less than 1s, got %s", res.Duration)
		}
	case <-time.After(2 * time.Second): // Timeout for the test itself
		t.Fatal("Test timed out")
	}
}

// Mock rationale: Using httptest to create a local HTTP server that delays response.
func TestFetchURL_Timeout(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(2 * time.Second) // Simulate a slow response
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Slow response"))
	}))
	defer server.Close()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	results := make(chan FetchResult, 1)

	// Set a short timeout for the fetchURL function
	go fetchURL(ctx, server.URL, results, 500*time.Millisecond)

	select {
	case res := <-results:
		if res.Status != "Error" || res.Err == nil || res.Err.Error() != "context deadline exceeded" {
			t.Errorf("Expected status 'Error' with context deadline exceeded, got status '%s' and error '%v'", res.Status, res.Err)
		}
		if res.Duration < 500*time.Millisecond {
			t.Errorf("Expected duration to be at least 500ms, got %s", res.Duration)
		}
	case <-time.After(2 * time.Second): // Timeout for the test itself
		t.Fatal("Test timed out")
	}
}

// Mock rationale: Using httptest to simulate a server returning an error status code.
func TestFetchURL_HTTPError(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("Internal Server Error"))
	}))
	defer server.Close()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	results := make(chan FetchResult, 1)

	go fetchURL(ctx, server.URL, results, 1*time.Second)

	select {
	case res := <-results:
		if res.Status != "HTTP Error: 500" {
			t.Errorf("Expected status 'HTTP Error: 500', got '%s'", res.Status)
		}
		if res.Err == nil || res.Err.Error() != "status code 500" {
			t.Errorf("Expected error 'status code 500', got '%v'", res.Err)
		}
	case <-time.After(2 * time.Second): // Timeout for the test itself
		t.Fatal("Test timed out")
	}
}

// Mock rationale: Testing with a non-existent host.
func TestFetchURL_NetworkError(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	results := make(chan FetchResult, 1)

	go fetchURL(ctx, "http://nonexistent.domain.for.testing.xyz", results, 1*time.Second)

	select {
	case res := <-results:
		if res.Status != "Error" {
			t.Errorf("Expected status 'Error', got '%s'", res.Status)
		}
		if res.Err == nil {
			t.Error("Expected an error for non-existent domain, but got nil")
		}
		if !strings.Contains(res.Err.Error(), "lookup non-existent.domain.for.testing.xyz") {
			t.Errorf("Expected error message related to lookup, got '%s'", res.Err)
		}
	case <-time.After(2 * time.Second): // Timeout for the test itself
		t.Fatal("Test timed out")
	}
}

// Mock rationale: Testing the main function's argument parsing and output.
func TestMainFunction(t *testing.T) {
	// Save original os.Args and os.Stdout
	originalArgs := os.Args
	originalStdout := os.Stdout

	// Mock os.Args to simulate command-line arguments
	os.Args = []string{"concurrent-fetcher", "-timeout", "1", "http://example.com"}

	// Mock os.Stdout to capture output
	r, w, _ := os.Pipe()
	os.Stdout = w

	main()

	// Restore original os.Args and os.Stdout
	os.Args = originalArgs
	w.Close()
	os.Stdout = originalStdout

	// Read captured output
	output, _ := io.ReadAll(r)
	outputStr := string(output)

	if !strings.Contains(outputStr, "Fetching URLs with a timeout of 1s...") {
		t.Errorf("Expected output to contain 'Fetching URLs with a timeout of 1s...', got:\n%s", outputStr)
	}
	if !strings.Contains(outputStr, "URL: http://example.com") {
		t.Errorf("Expected output to contain 'URL: http://example.com', got:\n%s", outputStr)
	}
	if !strings.Contains(outputStr, "Status: Success") {
		t.Errorf("Expected output to contain 'Status: Success', got:\n%s", outputStr)
	}
}
