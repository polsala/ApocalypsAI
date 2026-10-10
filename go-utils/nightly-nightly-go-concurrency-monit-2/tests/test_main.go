package main

import (
	"encoding/json"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"runtime"
	"strings"
	"testing"
	"time"
)

// Mock rationale: These tests use a local HTTP server and mock channel operations to ensure deterministic and offline testing.

func TestStatusHandler(t *testing.T) {
	// Start the HTTP server in a goroutine for testing.
	go func() {
		http.HandleFunc("/status", statusHandler)
		log.Fatal(http.ListenAndServe(":8081", nil))
	}()

	// Give the server a moment to start.
	time.Sleep(100 * time.Millisecond)

	// Simulate some Goroutines and channel ops.
	go func() {
		// This Goroutine will increase the count.
		time.Sleep(500 * time.Millisecond)
	}()

	// Simulate a channel send.
	go func() {
		// This is a simplified mock; in a real scenario, you'd use a channel.
		// For testing, we directly call the recording function.
		recordChannelOperation(SendOperation)
		time.Sleep(500 * time.Millisecond)
	}()

	// Wait for Goroutines to potentially start and ops to be recorded.
	time.Sleep(1 * time.Second)

	req, err := http.NewRequest("GET", "http://localhost:8081/status", nil)
	if err != nil {
		t.Fatalf("Failed to create request: %v", err)
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		t.Fatalf("Failed to execute request: %v", err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		t.Fatalf("Failed to read response body: %v", err)
	}

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status code %d, got %d", http.StatusOK, resp.StatusCode)
	}

	var result MonitorState
	if err := json.Unmarshal(body, &result);
	err != nil {
		t.Fatalf("Failed to unmarshal response body: %v\nBody: %s", err, string(body))
	}

	// Assertions:
	// We expect at least 2 Goroutines (main + test Goroutine + status handler Goroutine).
	// The exact number can vary, so we check for a minimum.
	if result.GoroutineCount < 3 {
		t.Errorf("Expected at least 3 Goroutines, got %d", result.GoroutineCount)
	}

	// We expect at least one send operation.
	if sends, ok := result.ChannelOps[string(SendOperation)]; !ok || sends < 1 {
		t.Errorf("Expected at least 1 send operation, got %d", sends)
	}

	// Stacks should be disabled by default.
	if result.StacksEnabled {
		t.Errorf("Expected stacks to be disabled by default, but they are enabled")
	}
}

func TestStacksEnableHandler(t *testing.T) {
	recorder := httptest.NewRecorder()
	http.NewRequest("POST", "/stacks/enable", nil)

	stacksEnableHandler(recorder, httptest.NewRequest("POST", "/stacks/enable", nil))

	if recorder.Code != http.StatusOK {
		t.Errorf("Expected status code %d, got %d", http.StatusOK, recorder.Code)
	}

	body := recorder.Body.String()
	if !strings.Contains(body, "enabled") {
		t.Errorf("Expected response body to contain 'enabled', got '%s'", body)
	}

	// Verify the state change
	state.mu.Lock()
	if !state.StacksEnabled {
		t.Errorf("Expected state.StacksEnabled to be true after enable, but it is false")
	}
	state.mu.Unlock()
}

func TestStacksDisableHandler(t *testing.T) {
	// First, enable stacks to ensure we can disable them.
	state.mu.Lock()
	state.StacksEnabled = true
	state.mu.Unlock()

	recorder := httptest.NewRecorder()
	http.NewRequest("POST", "/stacks/disable", nil)

	stacksDisableHandler(recorder, httptest.NewRequest("POST", "/stacks/disable", nil))

	if recorder.Code != http.StatusOK {
		t.Errorf("Expected status code %d, got %d", http.StatusOK, recorder.Code)
	}

	body := recorder.Body.String()
	if !strings.Contains(body, "disabled") {
		t.Errorf("Expected response body to contain 'disabled', got '%s'", body)
	}

	// Verify the state change
	state.mu.Lock()
	if state.StacksEnabled {
		t.Errorf("Expected state.StacksEnabled to be false after disable, but it is true")
	}
	state.mu.Unlock()
}

// Test that NumGoroutine returns a value greater than 1 (main + at least one other Goroutine).
func TestNumGoroutineMinimum(t *testing.T) {
	// We need to ensure there's at least one other Goroutine running besides main.
	// A simple sleep in a goroutine will suffice.
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		time.Sleep(10 * time.Millisecond)
	}()

	// Give the goroutine a moment to start.
	ttime.Sleep(50 * time.Millisecond)

	numGoroutines := runtime.NumGoroutine()
	if numGoroutines < 2 {
		t.Errorf("Expected at least 2 Goroutines, but got %d. Ensure a background Goroutine is running.", numGoroutines)
	}
	wg.Wait() // Ensure the test goroutine finishes.
}
