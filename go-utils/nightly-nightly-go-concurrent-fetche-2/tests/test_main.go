package main

import (
	"io"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

// Mock rationale: We need to mock the http.Get function to control the responses
// and simulate different scenarios (success, errors, delays) without making actual network requests.
// This ensures deterministic and offline testing.

func TestFetchURL_Success(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Hello, client!"))
	}))
	defer server.Close()

	var wg sync.WaitGroup
	results := make(chan FetchResult, 1)

	wg.Add(1)
	go fetchURL(server.URL, &wg, results)
	wg.Wait()
	close(results)

	result := <-results

	if result.Error != nil {
		t	Error("Expected no error, but got %v", result.Error)
		}
	if result.StatusCode != http.StatusOK {
			Error("Expected status code %d, but got %d", http.StatusOK, result.StatusCode)
		}
	if result.ResponseTime < 0 {
			Error("Expected positive response time, but got %v", result.ResponseTime)
		}
}

func TestFetchURL_NotFound(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("Not Found"))
	}))
	defer server.Close()

	var wg sync.WaitGroup
	results := make(chan FetchResult, 1)

	wg.Add(1)
	go fetchURL(server.URL, &wg, results)
	wg.Wait()
	close(results)

	result := <-results

	if result.Error != nil {
			Error("Expected no error, but got %v", result.Error)
		}
	if result.StatusCode != http.StatusNotFound {
			Error("Expected status code %d, but got %d", http.StatusNotFound, result.StatusCode)
		}
	if result.ResponseTime < 0 {
			Error("Expected positive response time, but got %v", result.ResponseTime)
		}
}

func TestFetchURL_NetworkError(t *testing.T) {
	// This URL is designed to cause a network error (e.g., host not found)
	url := "http://localhost:9999/nonexistent"

	var wg sync.WaitGroup
	results := make(chan FetchResult, 1)

	wg.Add(1)
	go fetchURL(url, &wg, results)
	wg.Wait()
	close(results)

	result := <-results

	if result.Error == nil {
			Error("Expected an error, but got none")
		}
	if result.StatusCode != 0 {
			Error("Expected status code 0 for network error, but got %d", result.StatusCode)
		}
	if result.ResponseTime < 0 {
			Error("Expected positive response time, but got %v", result.ResponseTime)
		}
}

func TestFetchURL_DelayedResponse(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(100 * time.Millisecond)
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Delayed response"))
	}))
	defer server.Close()

	var wg sync.WaitGroup
	results := make(chan FetchResult, 1)

	wg.Add(1)
	go fetchURL(server.URL, &wg, results)
	wg.Wait()
	close(results)

	result := <-results

	if result.Error != nil {
			Error("Expected no error, but got %v", result.Error)
		}
	if result.StatusCode != http.StatusOK {
			Error("Expected status code %d, but got %d", http.StatusOK, result.StatusCode)
		}
	// Check if response time is at least around 100ms
	if result.ResponseTime < 90*time.Millisecond {
			Error("Expected response time around 100ms, but got %v", result.ResponseTime)
		}
}

// Helper function to simplify error reporting in tests
func Error(format string, a ...interface{}) {
	panic(fmt.Sprintf(format, a...))
}
