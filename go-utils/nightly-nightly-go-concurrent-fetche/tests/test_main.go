package main

import (
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"
	"time"
)

// Mock rationale: Using httptest.NewServer to create a local HTTP server for deterministic testing without external network calls.
func TestFetchURL(t *testing.T) {
	// Create a test server that returns a 200 OK status
	serverOK := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	}))
	defer serverOK.Close()

	// Create a test server that returns a 404 Not Found status
	serverNotFound := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
	}))
	defer serverNotFound.Close()

	// Test case for a successful fetch
	t := func() {
		var wg sync.WaitGroup
		results := make(chan FetchResult, 1)
		wg.Add(1)
		go fetchURL(serverOK.URL, &wg, results)
		wg.Wait()
		close(results)

		result := <-results
		if result.Error != nil {
			t.Errorf("Expected no error, but got: %v", result.Error)
		}
		if result.StatusCode != http.StatusOK {
			t.Errorf("Expected status code %d, but got %d", http.StatusOK, result.StatusCode)
		}
		if result.ResponseTime > 50*time.Millisecond { // Allow some buffer for test execution
			t.Errorf("Expected response time to be less than 50ms, but got %s", result.ResponseTime)
		}
	}
	t()

	// Test case for a non-existent URL (will result in a connection error)
	func() {
		var wg sync.WaitGroup
		results := make(chan FetchResult, 1)
		wg.Add(1)
		// Using a URL that is guaranteed to fail DNS lookup
		go fetchURL("http://nonexistent.domain.xyz.local", &wg, results)
		wg.Wait()
		close(results)

		result := <-results
		if result.Error == nil {
			t.Error("Expected an error for nonexistent domain, but got none")
		}
		if result.StatusCode != 0 {
			t.Errorf("Expected status code 0 for error, but got %d", result.StatusCode)
		}
	}()

	// Test case for a server returning an error status code
	tfunc() {
		var wg sync.WaitGroup
		results := make(chan FetchResult, 1)
		wg.Add(1)
		go fetchURL(serverNotFound.URL, &wg, results)
		wg.Wait()
		close(results)

		result := <-results
		if result.Error != nil {
			t.Errorf("Expected no error for 404, but got: %v", result.Error)
		}
		if result.StatusCode != http.StatusNotFound {
			t.Errorf("Expected status code %d, but got %d", http.StatusNotFound, result.StatusCode)
		}
	}()
}
