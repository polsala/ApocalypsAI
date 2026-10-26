package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

// Mock rationale: We need to test the `checkBeacon` and `monitorBeacons` functions
// without making actual network calls, which would make tests non-deterministic, slow,
// and dependent on external services. `httptest.NewServer` allows us to simulate
// HTTP responses locally, providing controlled environments for each test case.

func TestCheckBeacon_Steady(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(10 * time.Millisecond) // Simulate some latency
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "OK")
	}))
	defer server.Close()

	status := checkBeacon(server.URL, 1*time.Second)

	if status.Status != "Steady" {
		t.Errorf("Expected status 'Steady', got '%s'", status.Status)
	}
	if status.Latency == 0 {
		t.Errorf("Expected non-zero latency, got %v", status.Latency)
	}
	if status.Error != nil {
		t.Errorf("Expected no error, got %v", status.Error)
	}
}

func TestCheckBeacon_Lagging(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(600 * time.Millisecond) // Simulate high latency
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "OK")
	}))
	defer server.Close()

	status := checkBeacon(server.URL, 2*time.Second) // Longer timeout for lagging test

	if status.Status != "Lagging" {
		t.Errorf("Expected status 'Lagging', got '%s'", status.Status)
	}
	if status.Latency < 500*time.Millisecond { // Check if latency is indeed high
		t.Errorf("Expected latency > 500ms, got %v", status.Latency)
	}
	if status.Error != nil {
		t.Errorf("Expected no error, got %v", status.Error)
	}
}

func TestCheckBeacon_Silent_NotFound(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		fmt.Fprintln(w, "Not Found")
	}))
	defer server.Close()

	status := checkBeacon(server.URL, 1*time.Second)

	if status.Status != "Silent" {
		t.Errorf("Expected status 'Silent', got '%s'", status.Status)
	}
	if status.Error == nil || !strings.Contains(status.Error.Error(), "HTTP status 404") {
		t.Errorf("Expected HTTP 404 error, got %v", status.Error)
	}
}

func TestCheckBeacon_Silent_Timeout(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(2 * time.Second) // Sleep longer than client timeout
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "OK")
	}))
	defer server.Close()

	status := checkBeacon(server.URL, 100*time.Millisecond) // Short timeout

	if status.Status != "Silent" {
		t.Errorf("Expected status 'Silent', got '%s'", status.Status)
	}
	if status.Error == nil || !strings.Contains(status.Error.Error(), "context deadline exceeded") {
		t.Errorf("Expected timeout error, got %v", status.Error)
	}
}

func TestMonitorBeacons_MixedResults(t *testing.T) {
	// Mock rationale: Simulating multiple endpoints with different behaviors
	// using httptest.NewServer to ensure deterministic and isolated testing
	// of the concurrent monitoring logic. This allows us to verify that
	// `monitorBeacons` correctly handles various success and failure scenarios
	// across multiple concurrent checks.

	steadyServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(50 * time.Millisecond)
		w.WriteHeader(http.StatusOK)
	}))
	defer steadyServer.Close()

	laggingServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(600 * time.Millisecond)
		w.WriteHeader(http.StatusOK)
	}))
	defer laggingServer.Close()

	silentServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusServiceUnavailable)
	}))
	defer silentServer.Close()

	// Include a non-existent URL to test connection errors
	endpoints := []string{steadyServer.URL, laggingServer.URL, silentServer.URL, "http://localhost:9999/nonexistent"}

	results := monitorBeacons(endpoints, 2*time.Second)

	if len(results) != len(endpoints) {
		t.Fatalf("Expected %d results, got %d", len(endpoints), len(results))
	}

	statusMap := make(map[string]string)
	for _, res := range results {
		statusMap[res.URL] = res.Status
	}

	if statusMap[steadyServer.URL] != "Steady" {
		t.Errorf("Expected %s to be 'Steady', got '%s'", steadyServer.URL, statusMap[steadyServer.URL])
	}
	if statusMap[laggingServer.URL] != "Lagging" {
		t.Errorf("Expected %s to be 'Lagging', got '%s'", laggingServer.URL, statusMap[laggingServer.URL])
	}
	if statusMap[silentServer.URL] != "Silent" {
		t.Errorf("Expected %s to be 'Silent', got '%s'", silentServer.URL, statusMap[silentServer.URL])
	}
	// Check for the non-existent URL, which should result in a "Silent" status due to connection error
	if statusMap["http://localhost:9999/nonexistent"] != "Silent" {
		t.Errorf("Expected non-existent URL to be 'Silent', got '%s'", statusMap["http://localhost:9999/nonexistent"])
	}
}

func TestMonitorBeacons_EmptyEndpoints(t *testing.T) {
	// Mock rationale: Testing the behavior with an empty list of endpoints
	// ensures the function handles edge cases gracefully without panicking
	// or producing unexpected results. No actual network calls are made.

	endpoints := []string{}
	results := monitorBeacons(endpoints, 1*time.Second)

	if len(results) != 0 {
		t.Errorf("Expected 0 results for empty endpoints, got %d", len(results))
	}
}
