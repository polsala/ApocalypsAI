package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock rationale: To ensure deterministic and offline testing, HTTP requests to remote servers are mocked using httptest.
// This prevents reliance on external network conditions and ensures consistent test results.

func TestFetchBeaconTime_Success(t *testing.T) {
	expectedTime := time.Date(2023, time.January, 1, 12, 0, 0, 0, time.UTC)
	mockServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Date", expectedTime.Format(time.RFC1123))
		w.WriteHeader(http.StatusOK)
	}))
	defer mockServer.Close()

	client := &http.Client{}
	actualTime, err := fetchBeaconTime(client, mockServer.URL)

	if err != nil {
		t.Fatalf("Expected no error, got %v", err)
	}
	if !actualTime.Equal(expectedTime) {
		t.Errorf("Expected time %v, got %v", expectedTime, actualTime)
	}
}

func TestFetchBeaconTime_NoDateHeader(t *testing.T) {
	mockServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	}))
	defer mockServer.Close()

	client := &http.Client{}
	_, err := fetchBeaconTime(client, mockServer.URL)

	if err == nil || !strings.Contains(err.Error(), "no Date header found") {
		t.Errorf("Expected 'no Date header found' error, got %v", err)
	}
}

func TestFetchBeaconTime_InvalidDateHeader(t *testing.T) {
	mockServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Date", "Not a valid date")
		w.WriteHeader(http.StatusOK)
	}))
	defer mockServer.Close()

	client := &http.Client{}
	_, err := fetchBeaconTime(client, mockServer.URL)

	if err == nil || !strings.Contains(err.Error(), "failed to parse Date header") {
		t.Errorf("Expected 'failed to parse Date header' error, got %v", err)
	}
}

func TestCheckDrift_Success(t *testing.T) {
	// Mock server time slightly ahead of local time for a positive drift
	mockServerTime := time.Now().UTC().Add(2 * time.Second)
	mockServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Date", mockServerTime.Format(time.RFC1123))
		w.WriteHeader(http.StatusOK)
	}))
	defer mockServer.Close()

	client := &http.Client{}
	results := make(chan ChronalDrift, 1)
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		checkDrift(client, mockServer.URL, results)
	}()
	wg.Wait()
	close(results)

	res := <-results
	if res.Error != nil {
		t.Fatalf("Expected no error, got %v", res.Error)
	}
	// The drift should be close to 2 seconds, allowing for slight execution time differences.
	// We'll check if it's within a reasonable range.
	if res.Drift.Abs() < 1*time.Second || res.Drift.Abs() > 3*time.Second { // Allow for ~1s execution variance
		t.Errorf("Expected drift around 2s, got %v", res.Drift)
	}
	if res.Drift < 0 {
		t.Errorf("Expected positive drift, got %v", res.Drift)
	}
}

func TestCheckDrift_NetworkError(t *testing.T) {
	// Simulate a network error by closing the server immediately
	mockServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// This handler won't even be hit if the connection fails
	}))
	mockServer.Close() // Close it immediately to simulate connection refused

	client := &http.Client{Timeout: 100 * time.Millisecond} // Short timeout for faster test
	results := make(chan ChronalDrift, 1)
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		checkDrift(client, mockServer.URL, results)
	}()
	wg.Wait()
	close(results)

	res := <-results
	if res.Error == nil || !strings.Contains(res.Error.Error(), "failed to reach beacon") {
		t.Errorf("Expected 'failed to reach beacon' error, got %v", res.Error)
	}
}

// Helper to capture os.Exit calls and output
func captureExit(f func()) (int, string) {
	oldOsExit := os.Exit
	oldStdout := os.Stdout
	oldStderr := os.Stderr
	defer func() {
		os.Exit = oldOsExit
		os.Stdout = oldStdout
		os.Stderr = oldStderr
	}()

	var exitCode int
	os.Exit = func(code int) {
		exitCode = code
		panic("os.Exit was called") // Panic to stop execution and allow recovery
	}

	rOut, wOut, _ := os.Pipe()
	rErr, wErr, _ := os.Pipe()
	os.Stdout = wOut
	os.Stderr = wErr

	var output string
	func() {
		defer func() {
			if r := recover(); r != nil {
				// Expected panic from os.Exit
			}
		}()
		f()
	}()

	wOut.Close()
	wErr.Close()
	outBytes, _ := fmt.ReadAll(rOut)
	errBytes, _ := fmt.ReadAll(rErr)
	output = string(outBytes) + string(errBytes)

	return exitCode, output
}

func TestMainFunction_NoArgs(t *testing.T) {
	os.Args = []string{"nightly-chronal-drift-detect"}
	exitCode, output := captureExit(main)

	if exitCode != 1 { // main exits 1 for usage error
		t.Errorf("Expected exit code 1 for no args, got %d. Output:\n%s", exitCode, output)
	}
	if !strings.Contains(output, "Usage:") {
		t.Errorf("Expected usage message, got:\n%s", output)
	}
}

func TestMainFunction_Success(t *testing.T) {
	// Mock server time perfectly synchronized
	mockServerTime := time.Now().UTC()
	mockServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Date", mockServerTime.Format(time.RFC1123))
		w.WriteHeader(http.StatusOK)
	}))
	defer mockServer.Close()

	os.Args = []string{"nightly-chronal-drift-detect", mockServer.URL}
	exitCode, output := captureExit(main)

	if exitCode != 0 {
		t.Errorf("Expected exit code 0, got %d. Output:\n%s", exitCode, output)
	}
	if !strings.Contains(output, "All time-beacons appear synchronized") {
		t.Errorf("Expected success message, got:\n%s", output)
	}
	// Allow for very small drift due to execution time, but should be close to 0s
	if !strings.Contains(output, "Drift 0s") && !strings.Contains(output, "Drift -0s") && !strings.Contains(output, "Drift 1ms") && !strings.Contains(output, "Drift -1ms") {
		t.Errorf("Expected drift close to 0s, got:\n%s", output)
	}
}

func TestMainFunction_WithDrift(t *testing.T) {
	// Mock server time with significant drift
	mockServerTime := time.Now().UTC().Add(5 * time.Second)
	mockServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Date", mockServerTime.Format(time.RFC1123))
		w.WriteHeader(http.StatusOK)
	}))
	defer mockServer.Close()

	os.Args = []string{"nightly-chronal-drift-detect", mockServer.URL}
	exitCode, output := captureExit(main)

	if exitCode != 1 {
		t.Errorf("Expected exit code 1 due to drift, got %d. Output:\n%s", exitCode, output)
	}
	if !strings.Contains(output, "Warning: Significant chronal drift detected") {
		t.Errorf("Expected warning message, got:\n%s", output)
	}
	// Check for drift around 5s, allowing for slight variance
	if !strings.Contains(output, "Drift 5s") && !strings.Contains(output, "Drift 4s") && !strings.Contains(output, "Drift 6s") {
		t.Errorf("Expected drift around 5s, got:\n%s", output)
	}
}

func TestMainFunction_WithError(t *testing.T) {
	// Simulate a network error by closing the server immediately
	mockServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// This handler won't be hit
	}))
	mockServer.Close() // Close it immediately to simulate connection refused

	os.Args = []string{"nightly-chronal-drift-detect", mockServer.URL}
	exitCode, output := captureExit(main)

	// An error doesn't trigger the "significant drift" condition, so it should exit 0.
	if exitCode != 0 {
		t.Errorf("Expected exit code 0 for error without significant drift, got %d. Output:\n%s", exitCode, output)
	}
	if !strings.Contains(output, "[ERROR] Beacon") || !strings.Contains(output, "failed to reach beacon") {
		t.Errorf("Expected error message for unreachable beacon, got:\n%s", output)
	}
}
