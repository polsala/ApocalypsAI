package main

import (
	"fmt"
	"testing"
	"time"
)

// Mock rationale: We need to test the `parseBeaconTime` and `calculateDrift`
// functions independently of network operations and non-deterministic `time.Now()`.

func TestParseBeaconTime(t *testing.T) {
	testTimeStr := "2023-10-27T10:30:00.123456789Z"
	expectedTime, _ := time.Parse(time.RFC3339Nano, testTimeStr)

	parsedTime, err := parseBeaconTime([]byte(testTimeStr))
	if err != nil {
		t.Fatalf("parseBeaconTime failed: %v", err)
	}

	if !parsedTime.Equal(expectedTime) {
		t.Errorf("Expected parsed time %v, got %v", expectedTime, parsedTime)
	}

	// Test invalid format
	invalidTimeStr := "not-a-time-string"
	_, err = parseBeaconTime([]byte(invalidTimeStr))
	if err == nil {
		t.Error("Expected error for invalid time string, got nil")
	}
}

func TestCalculateDrift(t *testing.T) {
	// Mock rationale: `time.Since` relies on `time.Now()`, which is non-deterministic.
	// To make this test deterministic, we temporarily replace `time.Now` with a mock function.

	// Store original time.Now and defer its restoration
	originalNow := time.Now
	defer func() { time.Now = originalNow }()

	// Set a fixed mock time for `time.Now()`
	mockNow := time.Date(2023, time.October, 27, 10, 30, 0, 0, time.UTC)
	time.Now = func() time.Time {
		return mockNow
	}

	// Test case 1: Beacon time is in the past
	beaconTimePast := time.Date(2023, time.October, 27, 10, 29, 59, 500000000, time.UTC) // 500ms before mockNow
	expectedDriftPast := 500 * time.Millisecond

	driftPast := calculateDrift(beaconTimePast)

	// Allow for slight nanosecond differences due to internal time representation
	if driftPast < expectedDriftPast-1*time.Millisecond || driftPast > expectedDriftPast+1*time.Millisecond {
		t.Errorf("Expected drift around %v, got %v", expectedDriftPast, driftPast)
	}

	// Test case 2: Beacon time is in the future
	beaconTimeFuture := time.Date(2023, time.October, 27, 10, 30, 0, 500000000, time.UTC) // 500ms after mockNow
	expectedDriftFuture := -500 * time.Millisecond // Negative drift means beacon is ahead

	driftFuture := calculateDrift(beaconTimeFuture)
	if driftFuture > expectedDriftFuture+1*time.Millisecond || driftFuture < expectedDriftFuture-1*time.Millisecond {
		t.Errorf("Expected future drift around %v, got %v", expectedDriftFuture, driftFuture)
	}

	// Test case 3: Beacon time is exactly now
	beaconTimeNow := mockNow
	expectedDriftNow := 0 * time.Millisecond

	driftNow := calculateDrift(beaconTimeNow)
	if driftNow < expectedDriftNow-1*time.Millisecond || driftNow > expectedDriftNow+1*time.Millisecond {
		t.Errorf("Expected zero drift, got %v", driftNow)
	}
}
