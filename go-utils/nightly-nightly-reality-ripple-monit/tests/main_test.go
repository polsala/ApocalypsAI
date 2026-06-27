package main

import (
	"bytes"
	"errors"
	"io"
	"net/http"
	"net/url"
	"strings"
	"sync"
	"testing"
	"time"
)

// MockHTTPClient is a mock implementation of the HTTPClient interface.
type MockHTTPClient struct {
	Responses map[string]struct {
		StatusCode int
		Body       string
		Err        error
		Delay      time.Duration
	}
}

// Get simulates an HTTP GET request based on predefined responses.
func (m *MockHTTPClient) Get(urlStr string) (*http.Response, error) {
	config, ok := m.Responses[urlStr]
	if !ok {
		return nil, errors.New("mock: URL not configured for testing") // # Mock rationale: Simulate unconfigured URL
	}

	time.Sleep(config.Delay) // # Mock rationale: Simulate network latency

	if config.Err != nil {
		return nil, config.Err // # Mock rationale: Simulate network errors (e.g., connection refused, timeout)
	}

	// # Mock rationale: Create a mock HTTP response
	resp := &http.Response{
		StatusCode: config.StatusCode,
		Body:       io.NopCloser(bytes.NewBufferString(config.Body)),
		Header:     make(http.Header),
		Request:    &http.Request{Method: "GET", URL: &url.URL{Scheme: "http", Host: "mockhost", Path: "/"}}, // Minimal request for response
	}
	return resp, nil
}

// TestCheckRipple_Success tests a successful HTTP 200 response.
func TestCheckRipple_Success(t *testing.T) {
	mockClient := &MockHTTPClient{
		Responses: map[string]struct {
			StatusCode int
			Body       string
			Err        error
			Delay      time.Duration
		}{
			"http://example.com/ok": {StatusCode: 200, Body: "OK", Delay: 10 * time.Millisecond},
		},
	}

	var wg sync.WaitGroup
	results := make(chan RippleResult, 1)

	wg.Add(1)
	go checkRipple(mockClient, "http://example.com/ok", results, &wg)

	wg.Wait()
	close(results)

	res := <-results

	if res.URL != "http://example.com/ok" {
		t.Errorf("Expected URL http://example.com/ok, got %s", res.URL)
	}
	if res.Status != "OK" {
		t.Errorf("Expected status OK, got %s", res.Status)
	}
	if res.Error != nil {
		t.Errorf("Expected no error, got %v", res.Error)
	}
	if res.Latency == 0 {
		t.Errorf("Expected non-zero latency, got %v", res.Latency)
	}
}

// TestCheckRipple_Failure_StatusCode tests an HTTP error status code (e.g., 404).
func TestCheckRipple_Failure_StatusCode(t *testing.T) {
	mockClient := &MockHTTPClient{
		Responses: map[string]struct {
			StatusCode int
			Body       string
			Err        error
			Delay      time.Duration
		}{
			"http://example.com/404": {StatusCode: 404, Body: "Not Found", Delay: 5 * time.Millisecond},
		},
	}

	var wg sync.WaitGroup
	results := make(chan RippleResult, 1)

	wg.Add(1)
	go checkRipple(mockClient, "http://example.com/404", results, &wg)

	wg.Wait()
	close(results)

	res := <-results

	if res.Status != "ERROR 404" {
		t.Errorf("Expected status ERROR 404, got %s", res.Status)
	}
	if res.Error != nil {
		t.Errorf("Expected no error, got %v", res.Error)
	}
}

// TestCheckRipple_Failure_NetworkError tests a simulated network error.
func TestCheckRipple_Failure_NetworkError(t *testing.T) {
	mockClient := &MockHTTPClient{
		Responses: map[string]struct {
			StatusCode int
			Body       string
			Err        error
			Delay      time.Duration
		}{
			"http://example.com/fail": {Err: errors.New("dial tcp 127.0.0.1:80: connect: connection refused"), Delay: 1 * time.Millisecond}, // # Mock rationale: Simulate connection refused
		},
	}

	var wg sync.WaitGroup
	results := make(chan RippleResult, 1)

	wg.Add(1)
	go checkRipple(mockClient, "http://example.com/fail", results, &wg)

	wg.Wait()
	close(results)

	res := <-results

	if res.Status != "FAILED" {
		t.Errorf("Expected status FAILED, got %s", res.Status)
	}
	if res.Error == nil || !strings.Contains(res.Error.Error(), "connection refused") {
		t.Errorf("Expected 'connection refused' error, got %v", res.Error)
	}
}

// TestCheckRipple_Timeout tests a simulated timeout.
func TestCheckRipple_Timeout(t *testing.T) {
	mockClient := &MockHTTPClient{
		Responses: map[string]struct {
			StatusCode int
			Body       string
			Err        error
			Delay      time.Duration
		}{
			"http://example.com/timeout": {Err: errors.New("Get \"http://example.com/timeout\": context deadline exceeded"), Delay: 6 * time.Second}, // # Mock rationale: Simulate timeout error
		},
	}

	var wg sync.WaitGroup
	results := make(chan RippleResult, 1)

	wg.Add(1)
	go checkRipple(mockClient, "http://example.com/timeout", results, &wg)

	wg.Wait()
	close(results)

	res := <-results

	if res.Status != "TIMEOUT" {
		t.Errorf("Expected status TIMEOUT, got %s", res.Status)
	}
	if res.Error == nil || !strings.Contains(res.Error.Error(), "context deadline exceeded") {
		t.Errorf("Expected timeout error, got %v", res.Error)
	}
}

// TestCheckRipple_Concurrent tests multiple URLs concurrently.
func TestCheckRipple_Concurrent(t *testing.T) {
	mockClient := &MockHTTPClient{
		Responses: map[string]struct {
			StatusCode int
			Body       string
			Err        error
			Delay      time.Duration
		}{
			"http://example.com/1": {StatusCode: 200, Body: "OK1", Delay: 20 * time.Millisecond},
			"http://example.com/2": {StatusCode: 400, Body: "Bad Request", Delay: 10 * time.Millisecond},
			"http://example.com/3": {Err: errors.New("dial tcp 127.0.0.1:80: connect: connection refused"), Delay: 5 * time.Millisecond},
		},
	}

	urls := []string{
		"http://example.com/1",
		"http://example.com/2",
		"http://example.com/3",
	}

	var wg sync.WaitGroup
	results := make(chan RippleResult, len(urls))

	for _, url := range urls {
		wg.Add(1)
		go checkRipple(mockClient, url, results, &wg)
	}

	wg.Wait()
	close(results)

	// Collect results and verify
	found := make(map[string]RippleResult)
	for res := range results {
		found[res.URL] = res
	}

	if len(found) != len(urls) {
		t.Fatalf("Expected %d results, got %d", len(urls), len(found))
	}

	// Verify specific results
	if res, ok := found["http://example.com/1"]; !ok || res.Status != "OK" {
		t.Errorf("URL 1 failed: %+v", res)
	}
	if res, ok := found["http://example.com/2"]; !ok || res.Status != "ERROR 400" {
		t.Errorf("URL 2 failed: %+v", res)
	}
	if res, ok := found["http://example.com/3"]; !ok || res.Status != "FAILED" || !strings.Contains(res.Error.Error(), "connection refused") {
		t.Errorf("URL 3 failed: %+v", res)
	}
}
