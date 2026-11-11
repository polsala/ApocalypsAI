package main

import (
	"bytes"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
)

// Mock rationale: This mock server simulates an HTTP server to test the fetchURL function without making actual network requests.
func mockServer(statusCode int, body string) *httptest.Server {
	return httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(statusCode)
		fmt.Fprintln(w, body)
	}))
}

func TestFetchURL_Success(t *testing.T) {
	server := mockServer(http.StatusOK, "Hello, client!")
	defer server.Close()

	var wg sync.WaitGroup
	results := make(chan string, 1)

	wg.Add(1)
	go fetchURL(server.URL, &wg, results)
	wg.Wait()
	close(results)

	result := <-results
	if !strings.Contains(result, fmt.Sprintf("Status: %d OK", http.StatusOK)) {
		t.Errorf("Expected success status, got: %s", result)
	}
}

func TestFetchURL_NotFound(t *testing.T) {
	server := mockServer(http.StatusNotFound, "Not Found")
	defer server.Close()

	var wg sync.WaitGroup
	results := make(chan string, 1)

	wg.Add(1)
	go fetchURL(server.URL, &wg, results)
	wg.Wait()
	close(results)

	result := <-results
	if !strings.Contains(result, "Status: 404 Not Found") {
		t.Errorf("Expected 404 status, got: %s", result)
	}
}

func TestFetchURL_NetworkError(t *testing.T) {
	// Use a URL that is guaranteed to fail DNS resolution
	nonExistentURL := "http://this.domain.does.not.exist.example.com"

	var wg sync.WaitGroup
	results := make(chan string, 1)

	wg.Add(1)
	go fetchURL(nonExistentURL, &wg, results)
	wg.Wait()
	close(results)

	result := <-results
	if !strings.Contains(result, "Error: Get \"http://this.domain.does.not.exist.example.com\": dial tcp: lookup this.domain.does.not.exist.example.com: no such host") {
		t.Errorf("Expected network error, got: %s", result)
	}
}

func TestMain_NoArgs(t *testing.T) {
	// Mock os.Args to simulate no arguments being passed
	originalArgs := os.Args
	os.Args = []string{originalArgs[0]} // Program name only
	defer func() { os.Args = originalArgs }()

	// Capture stdout
	oldStdout := os.Stdout
	var buf bytes.Buffer
	os.Stdout = &buf
	defer func() { os.Stdout = oldStdout }()

	main()

	expectedOutput := "Usage: concurrent-fetcher <url1> <url2> ...\n"
	if buf.String() != expectedOutput {
		t.Errorf("Expected output '%s', but got '%s'", expectedOutput, buf.String())
	}
}

func TestMain_WithArgs(t *testing.T) {
	// Mock the http.Get function to return our mock server responses
	serverSuccess := mockServer(http.StatusOK, "Success!")
	defer serverSuccess.Close()

	serverNotFound := mockServer(http.StatusNotFound, "Not Found")
	defer serverNotFound.Close()

	// Mock os.Args
	originalArgs := os.Args
	os.Args = []string{"concurrent-fetcher", serverSuccess.URL, serverNotFound.URL}
	defer func() { os.Args = originalArgs }()

	// Capture stdout
	oldStdout := os.Stdout
	var buf bytes.Buffer
	os.Stdout = &buf
	defer func() { os.Stdout = oldStdout }()

	main()

	output := buf.String()
	if !strings.Contains(output, fmt.Sprintf("URL: %s, Status: 200 OK", serverSuccess.URL)) {
		t.Errorf("Output missing success URL status: %s", output)
	}
	if !strings.Contains(output, fmt.Sprintf("URL: %s, Status: 404 Not Found", serverNotFound.URL)) {
		t.Errorf("Output missing not found URL status: %s", output)
	}
}
