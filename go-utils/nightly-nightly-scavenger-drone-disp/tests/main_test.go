package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// MockRoundTripper is a mock implementation of http.RoundTripper for testing.
// # Mock rationale: This custom RoundTripper allows simulating various HTTP responses
// # without making actual network calls, ensuring tests are deterministic and offline.
type MockRoundTripper struct {
	Response *http.Response
	Error    error
	Delay    time.Duration
}

func (m *MockRoundTripper) RoundTrip(req *http.Request) (*http.Response, error) {
	if m.Delay > 0 {
		time.Sleep(m.Delay)
	}
	if m.Error != nil {
		return nil, m.Error
	}
	return m.Response, nil
}

func TestFetchURL_Success(t *testing.T) {
	// Mock a successful HTTP response
	mockBody := "<html><body>Hello, World!</body></html>"
	mockResponse := &http.Response{
		StatusCode: 200,
		Status:     "200 OK",
		Body:       ioutil.NopCloser(strings.NewReader(mockBody)),
		Header:     make(http.Header),
	}
	mockClient := &http.Client{
		Transport: &MockRoundTripper{Response: mockResponse},
		Timeout:   defaultTimeout,
	}

	url := "http://example.com/success"
	results := make(chan DroneResult, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	go fetchURL(mockClient, url, results, &wg)

	wg.Wait()
	close(results)

	result := <-results

	if result.Error != nil {
		t.Fatalf("Expected no error, got: %v", result.Error)
	}
	if result.URL != url {
		t.Errorf("Expected URL %s, got %s", url, result.URL)
	}
	if result.StatusCode != 200 {
		t.Errorf("Expected status code 200, got %d", result.StatusCode)
	}
	if result.Status != "200 OK" {
		t.Errorf("Expected status '200 OK', got '%s'", result.Status)
	}
	expectedSnippet := "<html><body>Hello, World!</body></html>"
	if len(expectedSnippet) > bodySnippetLen {
		expectedSnippet = expectedSnippet[:bodySnippetLen] + "..."
	}
	expectedSnippet = strings.ReplaceAll(expectedSnippet, "\n", "\\n")
	if result.BodySnippet != expectedSnippet {
		t.Errorf("Expected body snippet '%s', got '%s'", expectedSnippet, result.BodySnippet)
	}
	if result.Latency <= 0 {
		t.Errorf("Expected positive latency, got %s", result.Latency)
	}
}

func TestFetchURL_NotFound(t *testing.T) {
	// Mock a 404 Not Found response
	mockResponse := &http.Response{
		StatusCode: 404,
		Status:     "404 Not Found",
		Body:       ioutil.NopCloser(strings.NewReader("")), // Empty body for 404
		Header:     make(http.Header),
	}
	mockClient := &http.Client{
		Transport: &MockRoundTripper{Response: mockResponse},
		Timeout:   defaultTimeout,
	}

	url := "http://example.com/notfound"
	results := make(chan DroneResult, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	go fetchURL(mockClient, url, results, &wg)

	wg.Wait()
	close(results)

	result := <-results

	if result.Error != nil {
		t.Fatalf("Expected no error, got: %v", result.Error)
	}
	if result.StatusCode != 404 {
		t.Errorf("Expected status code 404, got %d", result.StatusCode)
	}
	if result.Status != "404 Not Found" {
		t.Errorf("Expected status '404 Not Found', got '%s'", result.Status)
	}
	if result.BodySnippet != "" {
		t.Errorf("Expected empty body snippet, got '%s'", result.BodySnippet)
	}
}

func TestFetchURL_NetworkError(t *testing.T) {
	// Mock a network error
	mockClient := &http.Client{
		Transport: &MockRoundTripper{Error: fmt.Errorf("simulated network error")},
		Timeout:   defaultTimeout,
	}

	url := "http://example.com/error"
	results := make(chan DroneResult, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	go fetchURL(mockClient, url, results, &wg)

	wg.Wait()
	close(results)

	result := <-results

	if result.Error == nil {
		t.Fatal("Expected an error, got none")
	}
	expectedErrorMsg := "failed to fetch URL: simulated network error"
	if !strings.Contains(result.Error.Error(), expectedErrorMsg) {
		t.Errorf("Expected error message to contain '%s', got '%s'", expectedErrorMsg, result.Error.Error())
	}
	if result.URL != url {
		t.Errorf("Expected URL %s, got %s", url, result.URL)
	}
}

func TestFetchURL_Timeout(t *testing.T) {
	// Mock a response that takes longer than the client's timeout
	mockBody := "slow response"
	mockResponse := &http.Response{
		StatusCode: 200,
		Status:     "200 OK",
		Body:       ioutil.NopCloser(strings.NewReader(mockBody)),
		Header:     make(http.Header),
	}
	// Set client timeout to a very short duration, and mock delay to be longer
	mockClient := &http.Client{
		Transport: &MockRoundTripper{Response: mockResponse, Delay: 100 * time.Millisecond},
		Timeout:   50 * time.Millisecond, // Shorter than mock delay
	}

	url := "http://example.com/timeout"
	results := make(chan DroneResult, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	go fetchURL(mockClient, url, results, &wg)

	wg.Wait()
	close(results)

	result := <-results

	if result.Error == nil {
		t.Fatal("Expected a timeout error, got none")
	}
	expectedErrorMsg := "failed to fetch URL: net/http: request canceled (Client.Timeout exceeded while awaiting headers)"
	if !strings.Contains(result.Error.Error(), expectedErrorMsg) {
		t.Errorf("Expected error message to contain '%s', got '%s'", expectedErrorMsg, result.Error.Error())
	}
	if result.URL != url {
		t.Errorf("Expected URL %s, got %s", url, result.URL)
	}
}

func TestFetchURL_BodyReadError(t *testing.T) {
	// Mock a response where reading the body fails
	mockResponse := &http.Response{
		StatusCode: 200,
		Status:     "200 OK",
		Body:       ioutil.NopCloser(&errorReader{}), // Custom reader that always returns an error
		Header:     make(http.Header),
	}
	mockClient := &http.Client{
		Transport: &MockRoundTripper{Response: mockResponse},
		Timeout:   defaultTimeout,
	}

	url := "http://example.com/readerror"
	results := make(chan DroneResult, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	go fetchURL(mockClient, url, results, &wg)

	wg.Wait()
	close(results)

	result := <-results

	if result.Error == nil {
		t.Fatal("Expected a body read error, got none")
	}
	expectedErrorMsg := "failed to read response body: simulated read error"
	if !strings.Contains(result.Error.Error(), expectedErrorMsg) {
		t.Errorf("Expected error message to contain '%s', got '%s'", expectedErrorMsg, result.Error.Error())
	}
	if result.URL != url {
		t.Errorf("Expected URL %s, got %s", url, result.URL)
	}
	if result.StatusCode != 200 { // Status code should still be captured before body read
		t.Errorf("Expected status code 200, got %d", result.StatusCode)
	}
}

// errorReader is a custom io.Reader that always returns an error.
type errorReader struct{}

func (er *errorReader) Read(p []byte) (n int, err error) {
	return 0, fmt.Errorf("simulated read error")
}

func TestMainFunction_Integration(t *testing.T) {
	// This is more of an integration test, but we can use httptest.NewServer
	// to make it somewhat self-contained and offline.
	// # Mock rationale: httptest.NewServer creates a local HTTP server,
	// # allowing the main function's network interactions to be tested
	// # against controlled, local endpoints without external dependencies.

	// Create mock servers
	ts1 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, "OK 1")
	}))
	defer ts1.Close()

	ts2 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		fmt.Fprint(w, "Not Found")
	}))
	defer ts2.Close()

	// Capture stdout
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Temporarily set os.Args
	oldArgs := os.Args
	os.Args = []string{"scavenger-dispatcher", ts1.URL, ts2.URL, "http://invalid-url-for-error"}

	// Run main in a goroutine to allow capturing output and restoring os.Args
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		main()
	}()

	// Wait for main to finish and restore os.Args
	wg.Wait()
	os.Args = oldArgs
	w.Close()
	os.Stdout = oldStdout

	outBytes, _ := ioutil.ReadAll(r)
	output := string(outBytes)

	if !strings.Contains(output, fmt.Sprintf("[DRONE 1] %s - Status: 200 OK, Latency:", ts1.URL)) &&
	   !strings.Contains(output, fmt.Sprintf("[DRONE 2] %s - Status: 200 OK, Latency:", ts1.URL)) {
		t.Errorf("Expected output for %s, got:\n%s", ts1.URL, output)
	}
	if !strings.Contains(output, fmt.Sprintf("[DRONE 1] %s - Status: 404 Not Found, Latency:", ts2.URL)) &&
	   !strings.Contains(output, fmt.Sprintf("[DRONE 2] %s - Status: 404 Not Found, Latency:", ts2.URL)) {
		t.Errorf("Expected output for %s, got:\n%s", ts2.URL, output)
	}
	if !strings.Contains(output, "http://invalid-url-for-error - Error: failed to fetch URL: lookup invalid-url-for-error") &&
	   !strings.Contains(output, "http://invalid-url-for-error - Error: failed to fetch URL: dial tcp: lookup invalid-url-for-error") { // Different error messages depending on Go version/OS
		t.Errorf("Expected error output for invalid URL, got:\n%s", output)
	}
	if !strings.Contains(output, "Dispatching 3 scavenger drones...") {
		t.Errorf("Expected dispatch message, got:\n%s", output)
	}
	if !strings.Contains(output, "All scavenger drones have returned.") {
		t.Errorf("Expected completion message, got:\n%s", output)
	}
}
