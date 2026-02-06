package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
	"time"
)

// # Mock rationale: httptest.NewServer is used to create a local HTTP server
// # that can be controlled by the test. This allows simulating various network
// # conditions (success, error, timeout, specific status codes) deterministically
// # without relying on actual external network resources.

func TestProbeURL_Success(t *testing.T) {
	// Mock server for a successful response
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "OK")
	}))
	defer server.Close()

	result := probeURL(server.URL, 1*time.Second)

	if result.Error != nil {
		t.Errorf("Expected no error, got: %v", result.Error)
	}
	if result.Status != "OK" {
		t.Errorf("Expected status OK, got: %s", result.Status)
	}
	if result.StatusCode != http.StatusOK {
		t.Errorf("Expected status code %d, got: %d", http.StatusOK, result.StatusCode)
	}
	if result.Duration == 0 {
		t.Errorf("Expected non-zero duration")
	}
}

func TestProbeURL_NotFound(t *testing.T) {
	// Mock server for a 404 Not Found response
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		fmt.Fprintln(w, "Not Found")
	}))
	defer server.Close()

	result := probeURL(server.URL, 1*time.Second)

	if result.Error != nil {
		t.Errorf("Expected no error, got: %v", result.Error)
	}
	if result.Status != "VOID ANOMALY" {
		t.Errorf("Expected status VOID ANOMALY, got: %s", result.Status)
	}
	if result.StatusCode != http.StatusNotFound {
		t.Errorf("Expected status code %d, got: %d", http.StatusNotFound, result.StatusCode)
	}
}

func TestProbeURL_Timeout(t *testing.T) {
	// Mock server that delays beyond the timeout
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(200 * time.Millisecond) // Longer than the probe timeout
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "OK")
	}))
	defer server.Close()

	// Probe with a short timeout
	result := probeURL(server.URL, 50*time.Millisecond)

	if result.Error == nil {
		t.Errorf("Expected a timeout error, got none")
	}
	// Check for common timeout error messages across different Go versions/OS
	if !strings.Contains(result.Error.Error(), "context deadline exceeded") &&
	   !strings.Contains(result.Error.Error(), "Client.Timeout exceeded") {
		t.Errorf("Expected timeout error message, got: %v", result.Error)
	}
	if result.Status != "VOID ANOMALY" {
		t.Errorf("Expected status VOID ANOMALY, got: %s", result.Status)
	}
}

func TestProbeURL_InvalidURL(t *testing.T) {
	result := probeURL("invalid-url", 1*time.Second)

	if result.Error == nil {
		t.Errorf("Expected an error for invalid URL, got none")
	}
	if !strings.Contains(result.Error.Error(), "unsupported protocol scheme") {
		t.Errorf("Expected 'unsupported protocol scheme' error, got: %v", result.Error)
	}
	if result.Status != "VOID ANOMALY" {
		t.Errorf("Expected status VOID ANOMALY, got: %s", result.Status)
	}
}

func TestLoadURLsFromFile_Success(t *testing.T) {
	// Create a temporary file with URLs
	content := "https://url1.com\n# This is a comment\n  https://url2.com  \n\nhttps://url3.com"
	file, err := os.CreateTemp("", "urls-*.txt")
	if err != nil {
		t.Fatalf("Failed to create temp file: %v", err)
	}
	defer os.Remove(file.Name())
	defer file.Close()

	_, err = file.WriteString(content)
	if err != nil {
		t.Fatalf("Failed to write to temp file: %v", err)
	}
	file.Close()

	urls, err := loadURLsFromFile(file.Name())
	if err != nil {
		t.Errorf("Expected no error, got: %v", err)
	}

	expected := []string{"https://url1.com", "https://url2.com", "https://url3.com"}
	if len(urls) != len(expected) {
		t.Errorf("Expected %d URLs, got %d", len(expected), len(urls))
	}
	for i, u := range urls {
		if u != expected[i] {
			t.Errorf("Expected URL %s, got %s at index %d", expected[i], u, i)
		}
	}
}

func TestLoadURLsFromFile_NotFound(t *testing.T) {
	_, err := loadURLsFromFile("nonexistent-file.txt")
	if err == nil {
		t.Errorf("Expected an error for non-existent file, got none")
	}
	if !strings.Contains(err.Error(), "failed to open URL file") {
		t.Errorf("Expected 'failed to open URL file' error, got: %v", err)
	}
}
