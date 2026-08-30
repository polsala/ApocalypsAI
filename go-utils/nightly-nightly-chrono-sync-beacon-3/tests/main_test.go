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

// Mock rationale: We need to control the 'current time' for deterministic drift calculations
// and simulate HTTP responses from various services without actual network calls.

func TestFetchServiceTime_Aligned(t *testing.T) {
	// Mock the beacon's start time
	mockBeaconStartTime := time.Date(2023, time.October, 27, 10, 0, 0, 0, time.UTC)

	// Mock the timeProvider to return a consistent time for beaconEndTime calculation
	// This mock is crucial for deterministic latency calculation.
	mockBeaconEndTime := mockBeaconStartTime.Add(200 * time.Millisecond) // Simulate 200ms RTT
	timeProvider = func() time.Time { return mockBeaconEndTime } // # Mock rationale: Control time.Now() for deterministic latency calculation.

	// Mock HTTP server for the service endpoint
	// The service should return a time that, when accounting for latency, is aligned.
	// beaconStartTime + latency = serviceTime
	// 10:00:00 + 100ms = 10:00:00.100
	// So, the service should return 10:00:00.100
	serviceTime := mockBeaconStartTime.Add(100 * time.Millisecond) // Expected service time after 100ms one-way latency
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, serviceTime.Format(time.RFC3339))
	})) // # Mock rationale: Simulate a service endpoint returning a specific time without actual network calls.
	defer ts.Close()

	results := make(chan string, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	fetchServiceTime(ts.URL, mockBeaconStartTime, results, &wg)

	wg.Wait()
	close(results)

	select {
	case res := <-results:
		if !strings.Contains(res, "Status: Aligned") {
			t.Errorf("Expected 'Aligned' status, got: %s", res)
		}
		if !strings.Contains(res, "Drift: 0s") {
			t.Errorf("Expected 'Drift: 0s', got: %s", res)
		}
	case <-time.After(1 * time.Second):
		t.Fatal("Test timed out")
	}
}

func TestFetchServiceTime_SlightDrift(t *testing.T) {
	mockBeaconStartTime := time.Date(2023, time.October, 27, 10, 0, 0, 0, time.UTC)
	mockBeaconEndTime := mockBeaconStartTime.Add(200 * time.Millisecond)
	timeProvider = func() time.Time { return mockBeaconEndTime } // # Mock rationale: Control time.Now() for deterministic latency calculation.

	// Service time is slightly off: beaconStartTime + latency + 150ms drift
	// 10:00:00 + 100ms + 150ms = 10:00:00.250
	serviceTime := mockBeaconStartTime.Add(100 * time.Millisecond).Add(150 * time.Millisecond)
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, serviceTime.Format(time.RFC3339))
	})) // # Mock rationale: Simulate a service endpoint returning a specific time without actual network calls.
	defer ts.Close()

	results := make(chan string, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	fetchServiceTime(ts.URL, mockBeaconStartTime, results, &wg)

	wg.Wait()
	close(results)

	select {
	case res := <-results:
		if !strings.Contains(res, "Status: Slight Drift") {
			t.Errorf("Expected 'Slight Drift' status, got: %s", res)
		}
		if !strings.Contains(res, "Drift: +150ms") {
			t.Errorf("Expected 'Drift: +150ms', got: %s", res)
		}
	case <-time.After(1 * time.Second):
		t.Fatal("Test timed out")
	}
}

func TestFetchServiceTime_SignificantDrift(t *testing.T) {
	mockBeaconStartTime := time.Date(2023, time.October, 27, 10, 0, 0, 0, time.UTC)
	mockBeaconEndTime := mockBeaconStartTime.Add(200 * time.Millisecond)
	timeProvider = func() time.Time { return mockBeaconEndTime } // # Mock rationale: Control time.Now() for deterministic latency calculation.

	// Service time is significantly off: beaconStartTime + latency + 2s drift
	// 10:00:00 + 100ms + 2s = 10:00:02.100
	serviceTime := mockBeaconStartTime.Add(100 * time.Millisecond).Add(2 * time.Second)
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, serviceTime.Format(time.RFC3339))
	})) // # Mock rationale: Simulate a service endpoint returning a specific time without actual network calls.
	defer ts.Close()

	results := make(chan string, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	fetchServiceTime(ts.URL, mockBeaconStartTime, results, &wg)

	wg.Wait()
	close(results)

	select {
	case res := <-results:
		if !strings.Contains(res, "Status: Significant Drift") {
			t.Errorf("Expected 'Significant Drift' status, got: %s", res)
		}
		if !strings.Contains(res, "Drift: +2s") {
			t.Errorf("Expected 'Drift: +2s', got: %s", res)
		}
	case <-time.After(1 * time.Second):
		t.Fatal("Test timed out")
	}
}

func TestFetchServiceTime_NetworkError(t *testing.T) {
	mockBeaconStartTime := time.Date(2023, time.October, 27, 10, 0, 0, 0, time.UTC)
	// No need to mock timeProvider for this test as it won't reach drift calculation.

	// Use an invalid URL to simulate a network error
	invalidURL := "http://localhost:99999/nonexistent"

	results := make(chan string, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	fetchServiceTime(invalidURL, mockBeaconStartTime, results, &wg)

	wg.Wait()
	close(results)

	select {
	case res := <-results:
		if !strings.Contains(res, "Error fetching time") {
			t.Errorf("Expected network error, got: %s", res)
		}
	case <-time.After(1 * time.Second):
		t.Fatal("Test timed out")
	}
}

func TestFetchServiceTime_InvalidStatusCode(t *testing.T) {
	mockBeaconStartTime := time.Date(2023, time.October, 27, 10, 0, 0, 0, time.UTC)
	mockBeaconEndTime := mockBeaconStartTime.Add(100 * time.Millisecond)
	timeProvider = func() time.Time { return mockBeaconEndTime } // # Mock rationale: Control time.Now() for deterministic latency calculation.

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprint(w, "Internal Server Error")
	})) // # Mock rationale: Simulate a service endpoint returning an error status code.
	defer ts.Close()

	results := make(chan string, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	fetchServiceTime(ts.URL, mockBeaconStartTime, results, &wg)

	wg.Wait()
	close(results)

	select {
	case res := <-results:
		if !strings.Contains(res, "Received non-OK status: 500") {
			t.Errorf("Expected non-OK status error, got: %s", res)
		}
	case <-time.After(1 * time.Second):
		t.Fatal("Test timed out")
	}
}

func TestFetchServiceTime_InvalidTimeFormat(t *testing.T) {
	mockBeaconStartTime := time.Date(2023, time.October, 27, 10, 0, 0, 0, time.UTC)
	mockBeaconEndTime := mockBeaconStartTime.Add(100 * time.Millisecond)
	timeProvider = func() time.Time { return mockBeaconEndTime } // # Mock rationale: Control time.Now() for deterministic latency calculation.

	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, "not-a-time-string")
	})) // # Mock rationale: Simulate a service endpoint returning an invalid time format.
	defer ts.Close()

	results := make(chan string, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	fetchServiceTime(ts.URL, mockBeaconStartTime, results, &wg)

	wg.Wait()
	close(results)

	select {
	case res := <-results:
		if !strings.Contains(res, "Error parsing service time") {
			t.Errorf("Expected time parsing error, got: %s", res)
		}
	case <-time.After(1 * time.Second):
		t.Fatal("Test timed out")
	}
}

// TestMain is used to set up and tear down global test state, like resetting timeProvider.
func TestMain(m *testing.M) {
	// Store original timeProvider
	originalTimeProvider := timeProvider

	// Run tests
	exitCode := m.Run()

	// Restore original timeProvider to avoid side effects on other tests/runs
	timeProvider = originalTimeProvider

	os.Exit(exitCode)
}
