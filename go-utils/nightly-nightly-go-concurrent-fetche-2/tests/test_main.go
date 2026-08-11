package main

import (
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"
	"time"
)

// Mock rationale: We need to mock the HTTP server to control responses and simulate different scenarios (success, errors, delays) without making actual network requests.
func TestFetchURL(t *testing.T) {
	// Test case 1: Successful fetch
	tserverSuccess := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Hello, world!"))
	}))
	defer tserverSuccess.Close()

	var wgSuccess sync.WaitGroup
	resultsSuccess := make(chan FetchResult, 1)

	wgSuccess.Add(1)
	go fetchURL(tserverSuccess.URL, &wgSuccess, resultsSuccess)
	wgSuccess.Wait()
	close(resultsSuccess)

	resultSuccess := <-resultsSuccess
	if resultSuccess.Error != nil {
		t.Errorf("Expected no error for successful fetch, but got: %v", resultSuccess.Error)
	}
	if resultSuccess.Status != "200 OK" {
		t.Errorf("Expected status '200 OK', but got '%s'", resultSuccess.Status)
	}
	if resultSuccess.Duration < 0 {
		t.Errorf("Expected positive duration, but got %v", resultSuccess.Duration)
	}

	// Test case 2: Failed fetch (non-existent domain)
	var wgFail sync.WaitGroup
	resultsFail := make(chan FetchResult, 1)

	wgFail.Add(1)
	go fetchURL("http://localhost:9999", &wgFail, resultsFail) // Assuming port 9999 is not in use
	wgFail.Wait()
	close(resultsFail)

	resultFail := <-resultsFail
	if resultFail.Error == nil {
		t.Errorf("Expected an error for failed fetch, but got none")
	}
	if resultFail.Status == ""
		|| resultFail.Status == "200 OK" {
		t.Errorf("Expected a failure status, but got '%s'", resultFail.Status)
	}
	if resultFail.Duration < 0 {
		t.Errorf("Expected positive duration, but got %v", resultFail.Duration)
	}

	// Test case 3: Delayed fetch
	tserverDelay := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(100 * time.Millisecond)
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Delayed response"))
	}))
	defer tserverDelay.Close()

	var wgDelay sync.WaitGroup
	resultsDelay := make(chan FetchResult, 1)

	wgDelay.Add(1)
	go fetchURL(tserverDelay.URL, &wgDelay, resultsDelay)
	wgDelay.Wait()
	close(resultsDelay)

	resultDelay := <-resultsDelay
	if resultDelay.Error != nil {
		t.Errorf("Expected no error for delayed fetch, but got: %v", resultDelay.Error)
	}
	if resultDelay.Status != "200 OK" {
		t.Errorf("Expected status '200 OK', but got '%s'", resultDelay.Status)
	}
	// Check if duration is at least the simulated delay
	if resultDelay.Duration < 100*time.Millisecond {
		t.Errorf("Expected duration >= 100ms, but got %v", resultDelay.Duration)
	}
}
