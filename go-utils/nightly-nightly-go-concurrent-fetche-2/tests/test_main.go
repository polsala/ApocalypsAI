package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"sync"
)

func TestFetchURL_Success(t *testing.T) {
	// Mock server for successful response
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Hello, world!"))
	}))
	defer server.Close()

	var wg sync.WaitGroup
	results := make(chan FetchResult, 1)

	wg.Add(1)
	go fetchURL(server.URL, &wg, results)
	wg.Wait()
	close(results)

	res := <-results

	if res.Error != nil {
		t.Errorf("Expected no error, but got: %v", res.Error)
	}
	if res.Status != "200 OK" {
		t.Errorf("Expected status 200 OK, but got: %s", res.Status)
	}
}

func TestFetchURL_NotFound(t *testing.T) {
	// Mock server for not found response
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

	res := <-results

	if res.Error != nil {
		t.Errorf("Expected no error, but got: %v", res.Error)
	}
	if res.Status != "404 Not Found" {
		t.Errorf("Expected status 404 Not Found, but got: %s", res.Status)
	}
}

func TestFetchURL_NetworkError(t *testing.T) {
	// This URL is designed to fail DNS resolution
	url := "http://nonexistent.invalid.local"

	var wg sync.WaitGroup
	results := make(chan FetchResult, 1)

	wg.Add(1)
	go fetchURL(url, &wg, results)
	wg.Wait()
	close(results)

	res := <-results

	if res.Error == nil {
		t.Errorf("Expected an error, but got none")
	}
	if !strings.Contains(res.Error.Error(), "lookup nonexistent.invalid.local: no such host") {
		t.Errorf("Expected a network error related to host lookup, but got: %v", res.Error)
	}
}

func TestMain_NoArgs(t *testing.T) {
	// Mock os.Args to simulate no arguments passed
	originalArgs := os.Args
	defer func() { os.Args = originalArgs }()
	os.Args = []string{"concurrent_fetcher"}

	// Capture stdout to check output
	oldStdout := os.Stdout
	defer func() { os.Stdout = oldStdout }()
	
	r, w, _ := os.Pipe()
	os.Stdout = w

	main()

	w.Close()
	output, _ := io.ReadAll(r)

	expected := "Usage: concurrent_fetcher <url1> <url2> ...\n"
	if string(output) != expected {
		t.Errorf("Expected output \"%s\", but got \"%s\"", expected, string(output))
	}
}

func TestMain_WithArgs(t *testing.T) {
	// Mock server for successful response
	server1 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Success 1"))
	}))
	defer server1.Close()

	// Mock server for not found response
	server2 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("Not Found"))
	}))
	defer server2.Close()

	// Mock os.Args
	originalArgs := os.Args
	defer func() { os.Args = originalArgs }()
	os.Args = []string{"concurrent_fetcher", server1.URL, "http://invalid.url.for.testing", server2.URL}

	// Capture stdout
	oldStdout := os.Stdout
	defer func() { os.Stdout = oldStdout }()
	
	r, w, _ := os.Pipe()
	os.Stdout = w

	main()

	w.Close()
	output, _ := io.ReadAll(r)

	outputStr := string(output)

	if !strings.Contains(outputStr, "Starting concurrent fetches...") {
		t.Errorf("Output missing 'Starting concurrent fetches...'\nOutput: %s", outputStr)
	}

	if !strings.Contains(outputStr, fmt.Sprintf("Processing URL: %s", server1.URL)) {
		t.Errorf("Output missing processing for %s\nOutput: %s", server1.URL, outputStr)
	}

	if !strings.Contains(outputStr, "Processing URL: http://invalid.url.for.testing") {
		t.Errorf("Output missing processing for http://invalid.url.for.testing\nOutput: %s", outputStr)
	}

	if !strings.Contains(outputStr, fmt.Sprintf("Processing URL: %s", server2.URL)) {
		t.Errorf("Output missing processing for %s\nOutput: %s", server2.URL, outputStr)
	}

	if !strings.Contains(outputStr, fmt.Sprintf("- %s (Status: 200 OK)", server1.URL)) {
		t.Errorf("Output missing success for %s\nOutput: %s", server1.URL, outputStr)
	}

	if !strings.Contains(outputStr, "Failures:") {
		t.Errorf("Output missing 'Failures:' section\nOutput: %s", outputStr)
	}

	if !strings.Contains(outputStr, "- http://invalid.url.for.testing (Error:") {
		t.Errorf("Output missing expected failure for http://invalid.url.for.testing\nOutput: %s", outputStr)
	}

	if !strings.Contains(outputStr, fmt.Sprintf("- %s (Status: 404 Not Found)", server2.URL)) {
		t.Errorf("Output missing success for %s\nOutput: %s", server2.URL, outputStr)
	}
}
