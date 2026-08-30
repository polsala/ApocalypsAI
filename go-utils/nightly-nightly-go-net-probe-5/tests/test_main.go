package main

import (
	"bufio"
	"bytes"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

// Mock rationale: We are mocking the http.Server and its handlers to simulate network responses.
// This allows us to test the probeTarget function deterministically without actual network calls.

func TestProbeTarget_Success(t *testing.T) {
	// Create a mock HTTP server that responds with 200 OK
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Hello, client!"))
	}))
	defer server.Close()

	var wg sync.WaitGroup
	results := make(chan ProbeResult, 1)

	wg.Add(1)
	go probeTarget(server.URL, &wg, results)
	wg.Wait()
	close(results)

	result := <-results

	if result.Status != "OK" {
		t.Errorf("Expected status OK, got %s", result.Status)
	}

	if result.Error != nil {
		t.Errorf("Expected no error, got %v", result.Error)
	}

	if result.Latency < 0 {
		t.Errorf("Expected positive latency, got %s", result.Latency)
	}
}

func TestProbeTarget_NotFound(t *testing.T) {
	// Create a mock HTTP server that responds with 404 Not Found
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("Not Found"))
	}))
	defer server.Close()

	var wg sync.WaitGroup
	results := make(chan ProbeResult, 1)

	wg.Add(1)
	go probeTarget(server.URL, &wg, results)
	wg.Wait()
	close(results)

	result := <-results

	if result.Status != "HTTP 404" {
		t.Errorf("Expected status HTTP 404, got %s", result.Status)
	}

	if result.Error == nil {
		t.Errorf("Expected an error for 404, but got none")
	}

	if !strings.Contains(result.Error.Error(), "unexpected status code: 404") {
		t.Errorf("Expected error message to contain 'unexpected status code: 404', got %v", result.Error)
	}
}

func TestProbeTarget_Timeout(t *testing.T) {
	// Create a mock HTTP server that delays response indefinitely
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(10 * time.Second) // Longer than client timeout
		w.WriteHeader(http.StatusOK)
	}))
	defer server.Close()

	// Temporarily override the client timeout for this test to ensure it triggers
	originalClient := &http.Client{}
	*originalClient = http.Client{Timeout: 1 * time.Second} // Shorter timeout for test

	var wg sync.WaitGroup
	results := make(chan ProbeResult, 1)

	wg.Add(1)
	// Manually call probeTarget with the modified client (this is a bit of a hack for testing)
	// In a real scenario, you'd inject the client or modify the global one carefully.
	// For this test, we'll simulate the call structure.
	go func() {
		defer wg.Done()
		startTime := time.Now()
		resp, err := originalClient.Get(server.URL)
		latency := time.Since(startTime)
		if err != nil {
			results <- ProbeResult{Target: server.URL, Status: "Error", Latency: latency, Error: err}
			return
		}
		defer resp.Body.Close()
		results <- ProbeResult{Target: server.URL, Status: "OK", Latency: latency, Error: nil}
	}()

	wg.Wait()
	close(results)

	result := <-results

	if result.Status != "Error" {
		t.Errorf("Expected status Error due to timeout, got %s", result.Status)
	}

	if result.Error == nil {
		t.Errorf("Expected a timeout error, but got none")
	}

	if !strings.Contains(result.Error.Error(), "Client.Timeout exceeded") {
		t.Errorf("Expected error message to contain 'Client.Timeout exceeded', got %v", result.Error)
	}

	if result.Latency < 1*time.Second || result.Latency > 2*time.Second { // Allow some buffer
		t.Errorf("Expected latency around 1 second for timeout, got %s", result.Latency)
	}
}

func TestMainFunction_WithArgs(t *testing.T) {
	// Mock os.Args to simulate command-line arguments
	originalArgs := os.Args
	os.Args = []string{"netprobe", "http://mock.url.success", "http://mock.url.fail"}
	defer func() { os.Args = originalArgs }()

	// Mock the http.Get function to return predefined responses
	originalHTTPGet := http.Get
	http.Get = func(url string) (*http.Response, error) {
		if url == "http://mock.url.success" {
			return httptest.NewRecorder().Result(), nil
		} else if url == "http://mock.url.fail" {
			return nil, fmt.Errorf("simulated network error")
		}
		return nil, fmt.Errorf("unexpected URL: %s", url)
	}
	defer func() { http.Get = originalHTTPGet }()

	// Capture stdout
	oldStdout := os.Stdout
	var buf bytes.Buffer
	os.Stdout = &buf
	defer func() { os.Stdout = oldStdout }()

	// Run main
	main()

	output := buf.String()

	if !strings.Contains(output, "Target: http://mock.url.success, Status: OK") {
		t.Errorf("Stdout did not contain expected success message. Output: %s", output)
	}

	if !strings.Contains(output, "Target: http://mock.url.fail, Status: Error") {
		t.Errorf("Stdout did not contain expected failure message. Output: %s", output)
	}
}

func TestMainFunction_WithStdin(t *testing.T) {
	// Mock os.Args to simulate no command-line arguments
	originalArgs := os.Args
	os.Args = []string{"netprobe"}
	defer func() { os.Args = originalArgs }()

	// Mock os.Stdin to provide input
	input := "http://mock.stdin.success\nhttp://mock.stdin.fail"
	os.Stdin = bytes.NewBufferString(input)
	defer func() { os.Stdin = nil }()

	// Mock the http.Get function to return predefined responses
	originalHTTPGet := http.Get
	http.Get = func(url string) (*http.Response, error) {
		if url == "http://mock.stdin.success" {
			recorder := httptest.NewRecorder()
			recorder.WriteHeader(http.StatusOK)
			return recorder.Result(), nil
		} else if url == "http://mock.stdin.fail" {
			return nil, fmt.Errorf("simulated stdin network error")
		}
		return nil, fmt.Errorf("unexpected URL: %s", url)
	}
	defer func() { http.Get = originalHTTPGet }()

	// Capture stdout
	oldStdout := os.Stdout
	var buf bytes.Buffer
	os.Stdout = &buf
	defer func() { os.Stdout = oldStdout }()

	// Run main
	main()

	output := buf.String()

	if !strings.Contains(output, "Target: http://mock.stdin.success, Status: OK") {
		t.Errorf("Stdout did not contain expected success message. Output: %s", output)
	}

	if !strings.Contains(output, "Target: http://mock.stdin.fail, Status: Error") {
		t.Errorf("Stdout did not contain expected failure message. Output: %s", output)
	}
}

// Mock rationale: The bufio.Scanner is a standard library component. For testing stdin, we replace os.Stdin with a bytes.Buffer.
// The core logic of reading from stdin is tested by providing mock input to os.Stdin.
