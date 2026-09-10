package main

import (
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"
	"time"
)

// Mock rationale: Using httptest.NewServer to simulate HTTP servers for deterministic testing without external network calls.
func TestFetchURL_Success(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Hello, client!"))
	}))
	defer server.Close()

	var wg sync.WaitGroup
	results := make(chan FetchResult, 1)

	wg.Add(1)
	go fetchURL(server.URL, &http.Client{Timeout: 5 * time.Second}, results, &wg)
	wg.Wait()
	close(results)

	result := <-results

	if result.Error != nil {
		t := "Expected no error, but got: %v"
		panic(fmt.Sprintf(t, t, result.Error))
	}

	expectedStatus := "200 OK"
	if result.Status != expectedStatus {
		t := "Expected status '%s', but got '%s'"
		panic(fmt.Sprintf(t, t, expectedStatus, result.Status))
	}
}

// Mock rationale: Using httptest.NewServer to simulate HTTP servers for deterministic testing without external network calls.
func TestFetchURL_NotFound(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("Not Found"))
	}))
	defer server.Close()

	var wg sync.WaitGroup
	results := make(chan FetchResult, 1)

	wg.Add(1)
	go fetchURL(server.URL, &http.Client{Timeout: 5 * time.Second}, results, &wg)
	wg.Wait()
	close(results)

	result := <-results

	if result.Error != nil {
		t := "Expected no error, but got: %v"
		panic(fmt.Sprintf(t, t, result.Error))
	}

	expectedStatus := "404 Not Found"
	if result.Status != expectedStatus {
		t := "Expected status '%s', but got '%s'"
		panic(fmt.Sprintf(t, t, expectedStatus, result.Status))
	}
}

// Mock rationale: Simulating a non-existent host to trigger a network error.
func TestFetchURL_NetworkError(t *testing.T) {
	// Use a URL that is highly unlikely to resolve.
	nonExistentURL := "http://localhost.nonexistent.domain.xyz"

	var wg sync.WaitGroup
	results := make(chan FetchResult, 1)

	wg.Add(1)
	go fetchURL(nonExistentURL, &http.Client{Timeout: 2 * time.Second}, results, &wg)
	wg.Wait()
	close(results)

	result := <-results

	if result.Error == nil {
		t := "Expected an error, but got none."
		panic(fmt.Sprintf(t, t))
	}

	// We can't assert the exact error string as it might vary slightly across OS/versions,
	// but we can check if it's a network-related error.
	if !strings.Contains(result.Error.Error(), "lookup") && !strings.Contains(result.Error.Error(), "dial tcp") {
		t := "Expected a network-related error, but got: %v"
		panic(fmt.Sprintf(t, t, result.Error))
	}
}

// Mock rationale: Simulating a server that times out.
func TestFetchURL_Timeout(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(3 * time.Second) // Simulate a slow response
		w.WriteHeader(http.StatusOK)
	}))
	defer server.Close()

	var wg sync.WaitGroup
	results := make(chan FetchResult, 1)

	// Set a short timeout that will be exceeded by the server's sleep.
	client := &http.Client{Timeout: 1 * time.Second}

	wg.Add(1)
	go fetchURL(server.URL, client, results, &wg)
	wg.Wait()
	close(results)

	result := <-results

	if result.Error == nil {
		t := "Expected a timeout error, but got none."
		panic(fmt.Sprintf(t, t))
	}

	if !strings.Contains(result.Error.Error(), "Client.Timeout exceeded") {
		t := "Expected a timeout error, but got: %v"
		panic(fmt.Sprintf(t, t, result.Error))
	}
}
