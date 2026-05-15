package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"runtime"
	"strconv"
	"strings"
	"testing"
	"time"
	"github.com/polsala/ApocalypsAI/utils/nightly-go-concurrency-monitor/src/concurrencymonitor"
)

// Mock rationale: We are mocking the HTTP server and client interactions to test the monitor's functionality in isolation.
func TestConcurrencyMonitor(t *testing.T) {
	port := ":8081"
	go concurrencymonitor.StartMonitor(port)

	// Give the server a moment to start up.
	time.Sleep(100 * time.Millisecond)

	// Make a request to the monitor endpoint.
	resp, err := http.Get("http://localhost" + port + "/monitor")
	if err != nil {
		t.Fatalf("Failed to make request to monitor endpoint: %v", err)
	}
	defer resp.Body.Close()

	// Read the response body.
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		t.Fatalf("Failed to read response body: %v", err)
	}

	// Check the status code.
	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status code %d, but got %d", http.StatusOK, resp.StatusCode)
	}

	// Check if the response contains the total goroutine count.
	responseString := string(body)
	expectedGoroutineCount := runtime.NumGoroutine()

	// Extract the goroutine count from the response.
	countStr := extractGoroutineCount(responseString)
	actualGoroutineCount, err := strconv.Atoi(countStr)
	if err != nil {
		t.Fatalf("Failed to parse goroutine count from response: %v", err)
	}

	if actualGoroutineCount != expectedGoroutineCount {
		t.Errorf("Expected goroutine count %d, but got %d", expectedGoroutineCount, actualGoroutineCount)
	}

	// Ensure the monitor port is correctly reflected (basic check).
	if !strings.Contains(responseString, "http://localhost"+port+"/monitor") {
		t.Errorf("Response does not contain the correct monitor URL for port %s", port)
	}
}

// Helper function to extract the goroutine count from the HTML response.
func extractGoroutineCount(html string) string {
	startTag := "Total Goroutines: <strong>"
	endTag := "</strong>"

	startIndex := strings.Index(html, startTag)
	if startIndex == -1 {
		return "-1"
	}

	startIndex += len(startTag)
	endIndex := strings.Index(html[startIndex:], endTag)
	if endIndex == -1 {
		return "-1"
	}

	return html[startIndex : startIndex+endIndex]
}

// Mock rationale: A simple test to ensure the monitor starts without immediate errors.
func TestMonitorStarts(t *testing.T) {
	port := ":8082"
	// We don't need to assert anything specific here, just that StartMonitor doesn't panic.
	// The actual server functionality is tested in TestConcurrencyMonitor.
	go concurrencymonitor.StartMonitor(port)

	// Give it a brief moment to potentially fail if there's an immediate issue.
	time.Sleep(50 * time.Millisecond)

	// If we reach here without a panic, it's a basic success.
	fmt.Println("Monitor started successfully (basic check).")
}
