package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"runtime"
	"strings"
	"testing"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/testutil"
)

func TestStartAndStop(t *testing.T) {
	// Mock the HTTP server to avoid actual network operations during test.
	// We'll use a test server that doesn't actually listen on a port.
	testServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// This handler won't be called in this test, but it's required for NewServer.
	}))
	tdefer testServer.Close()

	// Override the default ListenAndServe to prevent it from actually starting.
	// This is a bit of a hack, but necessary for isolated testing of the monitor logic.
	originalListenAndServe := http.ListenAndServe
	defer func() {
		http.ListenAndServe = originalListenAndServe
	}()

	http.ListenAndServe = func(addr string, handler http.Handler) error {
		// Mock rationale: Prevent actual server startup during unit tests.
		// We are only interested in the metric collection logic.
		return nil
	}

	// Start the monitor with a short interval for faster testing.
	config := &MonitorConfig{
		Port:     8080, // This port won't actually be used due to the mock.
		Interval: 10 * time.Millisecond,
	}

	Start(config)
	defer Stop()

	// Give the collector a moment to run.
	time.Sleep(50 * time.Millisecond)

	// Check if metrics are registered.
	metrics, err := testutil.GatherAndFormat(prometheus.DefaultGatherer)
	if err != nil {
		t.Fatalf("Failed to gather metrics: %v", err)
	}

	// Basic checks for expected metrics.
	if !strings.Contains(metrics, "app_goroutines_total") {
		t.Error("Expected metric 'app_goroutines_total' not found")
	}
	if !strings.Contains(metrics, "app_channels_created_total") {
		t.Error("Expected metric 'app_channels_created_total' not found")
	}

	// Check if the number of goroutines is at least 1 (the main one).
	var numGoroutines float64
	for _, line := range strings.Split(metrics, "\n") {
		if strings.HasPrefix(line, "app_goroutines_total ") {
			fmt.Sscan(strings.TrimPrefix(line, "app_goroutines_total "), &numGoroutines)
			break
		}
	}

	if numGoroutines < 1 {
		t.Errorf("Expected at least 1 goroutine, got %f", numGoroutines)
	}
}

func TestChannelCreationMetric(t *testing.T) {
	// Mock the HTTP server to avoid actual network operations during test.
	testServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// This handler won't be called in this test.
	}))
	defer testServer.Close()

	http.ListenAndServe = func(addr string, handler http.Handler) error {
		// Mock rationale: Prevent actual server startup during unit tests.
		return nil
	}

	config := &MonitorConfig{
		Port:     8080,
		Interval: 10 * time.Millisecond,
	}

	Start(config)
	defer Stop()

	// Create a few mock channels.
	_ = CreateMockChannel()
	_ = CreateMockChannel()

	time.Sleep(50 * time.Millisecond) // Allow metrics to be collected.

	metrics, err := testutil.GatherAndFormat(prometheus.DefaultGatherer)
	if err != nil {
		t.Fatalf("Failed to gather metrics: %v", err)
	}

	var channelsCreated float64
	for _, line := range strings.Split(metrics, "\n") {
		if strings.HasPrefix(line, "app_channels_created_total ") {
			fmt.Sscan(strings.TrimPrefix(line, "app_channels_created_total "), &channelsCreated)
			break
		}
	}

	if channelsCreated != 2 {
		t.Errorf("Expected 2 channels created, got %f", channelsCreated)
	}
}

func TestDefaultConfig(t *testing.T) {
	// Mock the HTTP server to avoid actual network operations during test.
	testServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// This handler won't be called in this test.
	}))
	defer testServer.Close()

	http.ListenAndServe = func(addr string, handler http.Handler) error {
		// Mock rationale: Prevent actual server startup during unit tests.
		return nil
	}

	Start(nil) // Use default config
	defer Stop()

	// Give the collector a moment to run.
	time.Sleep(50 * time.Millisecond)

	metrics, err := testutil.GatherAndFormat(prometheus.DefaultGatherer)
	if err != nil {
		t.Fatalf("Failed to gather metrics: %v", err)
	}

	// Check if default interval is reflected (indirectly, by checking if metrics are updated).
	// This is hard to test directly without mocking time.Ticker. For now, we just ensure it runs.
	// We can check if goroutinesTotal is updated.
	var numGoroutines float64
	for _, line := range strings.Split(metrics, "\n") {
		if strings.HasPrefix(line, "app_goroutines_total ") {
			fmt.Sscan(strings.TrimPrefix(line, "app_goroutines_total "), &numGoroutines)
			break
		}
	}

	if numGoroutines < 1 {
		t.Errorf("Expected at least 1 goroutine with default config, got %f", numGoroutines)
	}
}

// Mock rationale: This test verifies the GetChannelsInUse function returns a predictable value.
// In a real scenario, this function would be more complex and might involve tracking active channels.
func TestGetChannelsInUse(t *testing.T) {
	// We need to ensure the monitor is started so that the metrics are initialized.
	// However, we don't need the server to run for this specific test.
	testServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// This handler won't be called in this test.
	}))
	defer testServer.Close()

	http.ListenAndServe = func(addr string, handler http.Handler) error {
		// Mock rationale: Prevent actual server startup during unit tests.
		return nil
	}

	Start(nil)
	defer Stop()

	// Call the function to get the channel usage metric.
	usage := GetChannelsInUse()

	// Assert that the returned value is the expected dummy value.
	expectedUsage := 5.0
	if usage != expectedUsage {
		t.Errorf("GetChannelsInUse() = %f; want %f", usage, expectedUsage)
	}
}
