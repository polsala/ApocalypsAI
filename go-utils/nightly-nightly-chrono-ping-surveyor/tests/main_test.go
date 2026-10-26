package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock rationale: We use httptest.NewServer to create a local HTTP server that
// simulates different network conditions (fast response, slow response, error)
// without making actual external network calls. This ensures tests are
// deterministic, fast, and offline.

func TestPingURL_Success(t *testing.T) {
	// Mock rationale: Simulate a fast responding server.
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Hello, world!")
	}))
	defer ts.Close()

	client := &http.Client{Timeout: 1 * time.Second}
	results := make(chan PingResult, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	go pingURL(client, ts.URL, 1*time.Second, 100*time.Millisecond, results, &wg)
	wg.Wait()
	close(results)

	res := <-results

	if res.Error != nil {
		t.Errorf("Expected no error, got %v", res.Error)
	}
	if res.URL != ts.URL {
		t.Errorf("Expected URL %s, got %s", ts.URL, res.URL)
	}
	if res.Duration <= 0 {
		t.Errorf("Expected positive duration, got %s", res.Duration)
	}
	if res.IsDistorted {
		t.Errorf("Expected not distorted, but it was")
	}
}

func TestPingURL_Distortion(t *testing.T) {
	// Mock rationale: Simulate a slow responding server to trigger a distortion.
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(200 * time.Millisecond) // Simulate delay
		fmt.Fprintln(w, "Slow response")
	}))
	defer ts.Close()

	client := &http.Client{Timeout: 1 * time.Second}
	results := make(chan PingResult, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	// Set a low threshold to easily trigger distortion
	go pingURL(client, ts.URL, 1*time.Second, 50*time.Millisecond, results, &wg)
	wg.Wait()
	close(results)

	res := <-results

	if res.Error != nil {
		t.Errorf("Expected no error, got %v", res.Error)
	}
	if !res.IsDistorted {
		t.Errorf("Expected distorted, but it was not")
	}
	if res.Duration < 200*time.Millisecond {
		t.Errorf("Expected duration > 200ms, got %s", res.Duration)
	}
}

func TestPingURL_Timeout(t *testing.T) {
	// Mock rationale: Simulate a server that responds slower than the client's timeout.
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(500 * time.Millisecond) // Longer than client timeout
		fmt.Fprintln(w, "Too slow")
	}))
	defer ts.Close()

	client := &http.Client{Timeout: 100 * time.Millisecond} // Short timeout
	results := make(chan PingResult, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	go pingURL(client, ts.URL, 100*time.Millisecond, 50*time.Millisecond, results, &wg)
	wg.Wait()
	close(results)

	res := <-results

	if res.Error == nil {
		t.Errorf("Expected an error due to timeout, got none")
	}
	if !strings.Contains(res.Error.Error(), "timeout") && !strings.Contains(res.Error.Error(), "canceled") {
		t.Errorf("Expected timeout error, got: %v", res.Error)
	}
}

func TestPingURL_InvalidURL(t *testing.T) {
	client := &http.Client{Timeout: 1 * time.Second}
	results := make(chan PingResult, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	invalidURL := "http://invalid-url-that-does-not-exist-12345.com"
	go pingURL(client, invalidURL, 1*time.Second, 100*time.Millisecond, results, &wg)
	wg.Wait()
	close(results)

	res := <-results

	if res.Error == nil {
		t.Errorf("Expected an error for invalid URL, got none")
	}
	if !strings.Contains(res.Error.Error(), "no such host") && !strings.Contains(res.Error.Error(), "failed to connect") {
		t.Errorf("Expected 'no such host' or 'failed to connect' error, got: %v", res.Error)
	}
}

func TestParseDuration(t *testing.T) {
	tests := []struct {
		input    string
		defaultD time.Duration
		expected time.Duration
		hasError bool
	}{
		{"1s", 0, 1 * time.Second, false},
		{"500ms", 0, 500 * time.Millisecond, false},
		{"": 10 * time.Second, 10 * time.Second, false},
		{"invalid", 0, 0, true},
	}

	for _, tt := range tests {
		d, err := parseDuration(tt.input, tt.defaultD)
		if (err != nil) != tt.hasError {
			t.Errorf("parseDuration(%q, %v) error status mismatch: expected error %v, got %v", tt.input, tt.defaultD, tt.hasError, err)
		}
		if d != tt.expected {
			t.Errorf("parseDuration(%q, %v) = %v, expected %v", tt.input, tt.defaultD, d, tt.expected)
		}
	}
}
