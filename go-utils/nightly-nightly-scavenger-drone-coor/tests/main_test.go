package main

import (
	"fmt"
	"sort"
	"testing"
	"time"
)

// mockScavengeSuccess is a mock ScavengeFn that always succeeds with a predictable resource.
func mockScavengeSuccess(zone string) (string, error) {
	// # Mock rationale: This mock replaces actual, potentially non-deterministic or slow
	// # I/O operations (like network calls or random delays) with a predictable,
	// # instantaneous result. This ensures tests are fast, deterministic, and
	// # isolated from external factors.
	return fmt.Sprintf("Mocked %s Resource", zone), nil
}

// mockScavengeFailure is a mock ScavengeFn that always fails for a specific zone.
func mockScavengeFailure(zone string) (string, error) {
	// # Mock rationale: Similar to mockScavengeSuccess, this mock provides a
	// # controlled failure scenario without relying on random chance or complex
	// # error conditions, making error handling logic testable.
	if zone == "ZoneC" {
		return "", fmt.Errorf("mocked failure in %s: drone lost signal", zone)
	}
	return fmt.Sprintf("Mocked %s Resource", zone), nil
}

// mockScavengeWithDelay is a mock ScavengeFn that simulates a delay.
func mockScavengeWithDelay(zone string) (string, error) {
	// # Mock rationale: This mock simulates a variable delay to test the
	// # concurrency aspects of the coordinator, ensuring that all goroutines
	// # are properly waited for, without making the test itself slow or
	// # non-deterministic due to actual I/O. The delays are fixed and small
	// # to maintain test speed and predictability.
	delay := 10 * time.Millisecond // Small, fixed delay for testing concurrency
	if zone == "ZoneB" {
		delay = 50 * time.Millisecond
	}
	time.Sleep(delay)
	return fmt.Sprintf("Delayed %s Resource", zone), nil
}


func TestCoordinateScavenging_Success(t *testing.T) {
	zones := []string{"ZoneA", "ZoneB", "ZoneC"}
	coordinator := NewScavengeCoordinator(mockScavengeSuccess)

	results := coordinator.CoordinateScavenging(zones)

	if len(results) != len(zones) {
		t.Fatalf("Expected %d results, got %d", len(zones), len(results))
	}

	// Sort results for deterministic comparison, as order of goroutine completion is not guaranteed.
	sort.Slice(results, func(i, j int) bool {
		return results[i].Zone < results[j].Zone
	} )

	expected := []ScavengeResult{
		{Zone: "ZoneA", Resource: "Mocked ZoneA Resource", Error: nil},
		{Zone: "ZoneB", Resource: "Mocked ZoneB Resource", Error: nil},
		{Zone: "ZoneC", Resource: "Mocked ZoneC Resource", Error: nil},
	}

	for i, res := range results {
		if res.Zone != expected[i].Zone || res.Resource != expected[i].Resource || res.Error != expected[i].Error {
			t.Errorf("Result mismatch for index %d. Expected %+v, got %+v", i, expected[i], res)
		}
	}
}

func TestCoordinateScavenging_PartialFailure(t *testing.T) {
	zones := []string{"ZoneA", "ZoneB", "ZoneC"}
	coordinator := NewScavengeCoordinator(mockScavengeFailure)

	results := coordinator.CoordinateScavenging(zones)

	if len(results) != len(zones) {
		t.Fatalf("Expected %d results, got %d", len(zones), len(results))
	}

	// Sort results for deterministic comparison.
	sort.Slice(results, func(i, j int) bool {
		return results[i].Zone < results[j].Zone
	})

	expectedErrors := map[string]string{
		"ZoneC": "mocked failure in ZoneC: drone lost signal",
	}

	for _, res := range results {
		if expectedErr, ok := expectedErrors[res.Zone]; ok {
			if res.Error == nil || res.Error.Error() != expectedErr {
				t.Errorf("Expected error for %s to be '%s', got '%v'", res.Zone, expectedErr, res.Error)
			}
			if res.Resource != "" {
				t.Errorf("Expected no resource for failed zone %s, got '%s'", res.Zone, res.Resource)
			}
		} else {
			if res.Error != nil {
				t.Errorf("Expected no error for %s, got '%v'", res.Zone, res.Error)
			}
			if res.Resource != fmt.Sprintf("Mocked %s Resource", res.Zone) {
				t.Errorf("Expected resource 'Mocked %s Resource' for %s, got '%s'", res.Zone, res.Zone, res.Resource)
			}
		}
	}
}

func TestCoordinateScavenging_NoZones(t *testing.T) {
	zones := []string{}
	coordinator := NewScavengeCoordinator(mockScavengeSuccess)

	results := coordinator.CoordinateScavenging(zones)

	if len(results) != 0 {
		t.Fatalf("Expected 0 results for no zones, got %d", len(results))
	}
}

func TestCoordinateScavenging_Concurrency(t *testing.T) {
	zones := []string{"ZoneA", "ZoneB", "ZoneC"}
	coordinator := NewScavengeCoordinator(mockScavengeWithDelay)

	startTime := time.Now()
	results := coordinator.CoordinateScavenging(zones)
	duration := time.Since(startTime)

	if len(results) != len(zones) {
		t.Fatalf("Expected %d results, got %d", len(zones), len(results))
	}

	// The longest delay in mockScavengeWithDelay is 50ms (for ZoneB).
	// If run sequentially, it would be roughly 10ms (ZoneA) + 50ms (ZoneB) + 10ms (ZoneC) = 70ms.
	// Concurrently, it should be closer to the maximum individual delay (50ms) plus a small overhead.
	// We allow a small buffer for scheduling and test execution time.
	expectedMinDuration := 50 * time.Millisecond
	if duration < expectedMinDuration {
		t.Errorf("Expected concurrent execution to take at least %v, but it took %v. Might not be concurrent enough.", expectedMinDuration, duration)
	}
	// Also ensure it's not excessively long, implying sequential execution.
	// A sequential run would be roughly 70ms. We expect it to be less than, say, 65ms.
	expectedMaxDuration := 65 * time.Millisecond
	if duration > expectedMaxDuration {
		t.Errorf("Expected concurrent execution to take at most %v, but it took %v. Might be running sequentially.", expectedMaxDuration, duration)
	}
}
