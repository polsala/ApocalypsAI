package main

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

// Mock rationale: Using httptest.NewServer to simulate HTTP servers for deterministic testing.
func TestFetchURLsConcurrently(t *testing.T) {
	// Create a test server that returns a 200 OK status and a short delay
	testServerOK := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	}))
	defer testServerOK.Close()

	// Create a test server that returns a 404 Not Found status
	testServerNotFound := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("Not Found"))
	}))
	defer testServerNotFound.Close()

	// Create a test server that simulates a delay
	testServerDelayed := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(50 * time.Millisecond)
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Delayed OK"))
	}))
	defer testServerDelayed.Close()

	urls := []string{
		testServerOK.URL,
		testServerNotFound.URL,
		testServerDelayed.URL,
		"http://invalid.local.domain.for.testing", // Invalid URL
	}

	results := fetchURLsConcurrently(urls)

	// Check the number of results
	if len(results) != len(urls) {
		t.Errorf("Expected %d results, but got %d", len(urls), len(results))
	}

	// Check individual results
	for _, res := range results {
		switch {
		case strings.Contains(res.URL, testServerOK.URL):
			if res.StatusCode != http.StatusOK {
				t.Errorf("For URL %s, expected status %d, got %d", res.URL, http.StatusOK, res.StatusCode)
			}
			if res.Error != nil {
				t.Errorf("For URL %s, expected no error, but got %v", res.URL, res.Error)
			}
			if res.Duration < 1*time.Millisecond {
				t.Errorf("For URL %s, expected duration > 1ms, got %s", res.URL, res.Duration)
			}

		case strings.Contains(res.URL, testServerNotFound.URL):
			if res.StatusCode != http.StatusNotFound {
				t.Errorf("For URL %s, expected status %d, got %d", res.URL, http.StatusNotFound, res.StatusCode)
			}
			if res.Error != nil {
				t.Errorf("For URL %s, expected no error, but got %v", res.URL, res.Error)
			}

		case strings.Contains(res.URL, testServerDelayed.URL):
			if res.StatusCode != http.StatusOK {
				t.Errorf("For URL %s, expected status %d, got %d", res.URL, http.StatusOK, res.StatusCode)
			}
			if res.Error != nil {
				t.Errorf("For URL %s, expected no error, but got %v", res.URL, res.Error)
			}
			if res.Duration < 50*time.Millisecond {
				t.Errorf("For URL %s, expected duration >= 50ms, got %s", res.URL, res.Duration)
			}

		case res.URL == "http://invalid.local.domain.for.testing":
			if res.StatusCode != 0 {
				t.Errorf("For URL %s, expected status code 0 (error), got %d", res.URL, res.StatusCode)
			}
			if res.Error == nil {
				t.Errorf("For URL %s, expected an error, but got none", res.URL)
			}
			if res.Duration < 1*time.Millisecond {
				t.Errorf("For URL %s, expected duration > 1ms, got %s", res.URL, res.Duration)
			}

		default:
			t.Errorf("Unexpected URL encountered: %s", res.URL)
		}
	}
}

// Mock rationale: Testing the fetchURL function directly to ensure it handles single URL fetches correctly.
func TestFetchURL(t *testing.T) {
	// Test a valid URL
	testServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Hello, world!"))
	}))
	defer testServer.Close()

	result := fetchURL(testServer.URL)

	if result.Error != nil {
		t.Errorf("fetchURL(%s) returned an unexpected error: %v", testServer.URL, result.Error)
	}

	if result.StatusCode != http.StatusOK {
		t.Errorf("fetchURL(%s) returned status code %d, want %d", testServer.URL, result.StatusCode, http.StatusOK)
	}

	if result.Duration < 1*time.Millisecond {
		t.Errorf("fetchURL(%s) duration too short: %s", testServer.URL, result.Duration)
	}

	// Test an invalid URL
	invalidURL := "http://nonexistent.domain.test/"
	resultInvalid := fetchURL(invalidURL)

	if resultInvalid.Error == nil {
		t.Errorf("fetchURL(%s) did not return an error when expected", invalidURL)
	}

	if resultInvalid.StatusCode != 0 {
		t.Errorf("fetchURL(%s) returned status code %d, want 0", invalidURL, resultInvalid.StatusCode)
	}

	if resultInvalid.Duration < 1*time.Millisecond {
		t.Errorf("fetchURL(%s) duration too short: %s", invalidURL, resultInvalid.Duration)
	}
}
