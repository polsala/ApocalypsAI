package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func TestFetchURL_Success(t *testing.T) {
	// Mock server for successful HTTP response
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Hello, client!"))
	}))
	defer server.Close()

	results := make(chan FetchResult, 1)
	go fetchURL(server.URL, results)

	select {
	case res := <-results:
		if res.Status != "OK" {
			t.Errorf("Expected status OK, got %s", res.Status)
		}
		if res.Error != nil {
			t.Errorf("Expected no error, got %v", res.Error)
		}
		if res.Time <= 0 {
			t.Errorf("Expected positive fetch time, got %s", res.Time)
		}
	case <-time.After(2 * time.Second): // Timeout for safety
		t.Fatal("Test timed out")
	}
}

func TestFetchURL_Error(t *testing.T) {
	// Mock server that returns an internal server error
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
	}))
	defer server.Close()

	results := make(chan FetchResult, 1)
	go fetchURL(server.URL, results)

	select {
	case res := <-results:
		if res.Status != "Error" {
			t.Errorf("Expected status Error, got %s", res.Status)
		}
		if res.Error == nil {
			t.Error("Expected an error, got nil")
		}
		// We don't check time here as it might be negligible or inconsistent on error paths.
	case <-time.After(2 * time.Second): // Timeout for safety
		t.Fatal("Test timed out")
	}
}

func TestFetchURL_InvalidURL(t *testing.T) {
	// Test with a URL that cannot be resolved
	invalidURL := "http://nonexistent.domain.local"
	results := make(chan FetchResult, 1)
	go fetchURL(invalidURL, results)

	select {
	case res := <-results:
		if res.Status != "Error" {
			t.Errorf("Expected status Error for invalid URL, got %s", res.Status)
		}
		if res.Error == nil {
			t.Error("Expected an error for invalid URL, got nil")
		}
	case <-time.After(2 * time.Second): // Timeout for safety
		t.Fatal("Test timed out")
	}
}
