package main

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestCheckURLs(t *testing.T) {
	// Setup test servers
	server200 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	}))
	defer server200.Close()

	server404 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
	}))
	defer server404.Close()

	// Invalid URL
	badURL := "http://invalid.host"

	urls := []string{server200.URL, server404.URL, badURL}
	results, err := CheckURLs(urls, 2)
	if err != nil {
		t.Fatalf("CheckURLs returned error: %v", err)
	}
	if len(results) != 3 {
		t.Fatalf("Expected 3 results, got %d", len(results))
	}

	// Verify statuses
	for _, r := range results {
		switch r.URL {
		case server200.URL:
			if r.Status != "200 OK" {
				t.Errorf("Expected 200 OK, got %s", r.Status)
			}
		case server404.URL:
			if r.Status != "404 Not Found" {
				t.Errorf("Expected 404 Not Found, got %s", r.Status)
			}
		case badURL:
			if r.Status == "" || r.Status[:6] != "error:" {
				t.Errorf("Expected error status for bad URL, got %s", r.Status)
			}
		}
	}
}
