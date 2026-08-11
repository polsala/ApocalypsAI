package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

// Mock rationale: These tests use a local HTTP test server to simulate responses
// without making actual network calls. This ensures deterministic and offline execution.

func TestConcurrentFetcher_Success(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Hello, world!"))
	}))
	defer server.Close()

	// Temporarily replace os.Args to simulate command-line arguments
	originalArgs := os.Args
	os.Args = []string{"concurrent-fetcher", server.URL}
	defer func() {
		os.Args = originalArgs
	}()

	// Capture stdout to check output
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	main()

	w.Close()
	os.Stdout = oldStdout

	// Basic check: ensure the output contains the URL and status code
	// More sophisticated output parsing could be added here.
	output, _ := io.ReadAll(r)
	if !strings.Contains(string(output), "Status=200 OK") {
		t.Errorf("Expected 200 OK in output, but got: %s", string(output))
	}
}

func TestConcurrentFetcher_Error(t *testing.T) {
	// A server that will cause a connection refused error when accessed
	// We don't even need to start a server, just use a non-existent address.
	nonExistentURL := "http://localhost:9999"

	// Temporarily replace os.Args to simulate command-line arguments
	originalArgs := os.Args
	os.Args = []string{"concurrent-fetcher", nonExistentURL}
	defer func() {
		os.Args = originalArgs
	}()

	// Capture stdout to check output
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	main()

	w.Close()
	os.Stdout = oldStdout

	output, _ := io.ReadAll(r)
	if !strings.Contains(string(output), "Error=Get \"http://localhost:9999\": dial tcp 127.0.0.1:9999: connectex: No connection could be made because the target machine actively refused it.") {
		t.Errorf("Expected connection refused error in output, but got: %s", string(output))
	}
}

func TestConcurrentFetcher_Timeout(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(2 * time.Second) // Sleep longer than the timeout
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Slow response"))
	}))
	defer server.Close()

	// Temporarily replace os.Args to simulate command-line arguments
	originalArgs := os.Args
	os.Args = []string{"concurrent-fetcher", "-timeout", "1s", server.URL}
	defer func() {
		os.Args = originalArgs
	}()

	// Capture stdout to check output
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	main()

	w.Close()
	os.Stdout = oldStdout

	output, _ := io.ReadAll(r)
	if !strings.Contains(string(output), "Time=1s (Timeout)") {
		t.Errorf("Expected timeout indication in output, but got: %s", string(output))
	}
}

func TestConcurrentFetcher_MultipleURLs(t *testing.T) {
	server1 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Server 1"))
	}))
	defer server1.Close()

	server2 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("Server 2"))
	}))
	defer server2.Close()

	// Temporarily replace os.Args to simulate command-line arguments
	originalArgs := os.Args
	os.Args = []string{"concurrent-fetcher", server1.URL, server2.URL}
	defer func() {
		os.Args = originalArgs
	}()

	// Capture stdout to check output
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	main()

	w.Close()
	os.Stdout = oldStdout

	output, _ := io.ReadAll(r)
	if !strings.Contains(string(output), "Status=200 OK") {
		t.Errorf("Expected 200 OK for server1, but got: %s", string(output))
	}
	if !strings.Contains(string(output), "Status=404 Not Found") {
		t.Errorf("Expected 404 Not Found for server2, but got: %s", string(output))
	}
}
