package main

import (
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"
	"time"
)

// Mock rationale: Using httptest.NewServer to simulate HTTP responses without making actual network calls.
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

	res := <-results

	if res.Status != "OK" {
		t.Errorf("Expected status OK, got %s", res.Status)
	}

	if res.Error != nil {
		t.Errorf("Expected no error, got %v", res.Error)
	}

	if res.Duration < 0 {
		t.Errorf("Expected non-negative duration, got %v", res.Duration)
	}
}

// Mock rationale: Using httptest.NewServer to simulate HTTP responses with an error status code.
func TestFetchURL_Error(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
	}))
	defer server.Close()

	var wg sync.WaitGroup
	results := make(chan FetchResult, 1)

	wg.Add(1)
	go fetchURL(server.URL, &wg, results)
	wg.Wait()
	close(results)

	res := <-results

	if res.Status != "OK" {
		t.Errorf("Expected status OK for server error response, got %s", res.Status)
	}

	if res.Error == nil {
		t.Errorf("Expected an error for server error response, but got none")
	}

	if res.Duration < 0 {
		t.Errorf("Expected non-negative duration, got %v", res.Duration)
	}
}

// Mock rationale: Testing with a non-existent domain to simulate a DNS resolution error.
func TestFetchURL_NonExistentDomain(t *testing.T) {
	var wg sync.WaitGroup
	results := make(chan FetchResult, 1)

	// Using a URL that is highly unlikely to resolve.
	nonExistentURL := "http://this.domain.definitely.does.not.exist.xyz"

	wg.Add(1)
	go fetchURL(nonExistentURL, &wg, results)
	wg.Wait()
	close(results)

	res := <-results

	if res.Status != "Error" {
		t.Errorf("Expected status Error for non-existent domain, got %s", res.Status)
	}

	if res.Error == nil {
		t.Errorf("Expected an error for non-existent domain, but got none")
	}

	if res.Duration < 0 {
		t.Errorf("Expected non-negative duration, got %v", res.Duration)
	}
}

// Mock rationale: Testing the timeout functionality by using a server that delays its response.
func TestFetchURL_Timeout(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(5 * time.Second) // Simulate a long-running request
		w.WriteHeader(http.StatusOK)
	}))
	defer server.Close()

	// Temporarily override the client timeout for this specific test to be shorter than the server delay.
	originalClient := http.DefaultClient
	http.DefaultClient = &http.Client{Timeout: 1 * time.Second}
	defer func() { http.DefaultClient = originalClient }()

	var wg sync.WaitGroup
	results := make(chan FetchResult, 1)

	wg.Add(1)
	go fetchURL(server.URL, &wg, results)
	wg.Wait()
	close(results)

	res := <-results

	if res.Status != "Error" {
		t.Errorf("Expected status Error due to timeout, got %s", res.Status)
	}

	if res.Error == nil {
		t.Errorf("Expected a timeout error, but got none")
	}

	if res.Duration < 1*time.Second || res.Duration > 2*time.Second { // Allow some buffer for test execution
		t.Errorf("Expected duration around 1 second (timeout), got %v", res.Duration)
	}
}
