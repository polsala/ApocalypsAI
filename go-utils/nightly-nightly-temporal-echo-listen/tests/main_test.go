package main

import (
	"sort"
	"testing"
	""time"
)

// Mock rationale: `time.Sleep` and `math/rand.Intn` are non-deterministic.
// `mockSleep` replaces `time.Sleep` with a no-op to ensure tests run instantly.
// `mockRandIntn` replaces `math/rand.Intn` with a controlled sequence of values
// to deterministically trigger or prevent anomalies based on `AnomalyChance`.

// mockSleep function for deterministic tests
func mockSleep(d time.Duration) {
	// Do nothing, or record that sleep was called if needed for more complex tests
}

// mockRandIntn function for deterministic tests
type mockRandIntn struct {
	values []int
	index  int
}

func (m *mockRandIntn) Intn(n int) int {
	if m.index >= len(m.values) {
		// If we run out of predefined values, return a default (e.g., 0 for no anomaly)
		return 0
	}
	val := m.values[m.index]
	m.index++
	return val
}

// setupMocks sets up the mock functions and returns a cleanup function.
func setupMocks(randValues []int) func() {
	originalSleepFunc := sleepFunc
	originalRandIntnFunc := randIntnFunc

	sleepFunc = mockSleep
	mockRand := &mockRandIntn{values: randValues}
	randIntnFunc = mockRand.Intn

	return func() {
		sleepFunc = originalSleepFunc
		randIntnFunc = originalRandIntnFunc
	}
}

func TestListenToAnchor_Stable(t *testing.T) {
	cleanup := setupMocks([]int{0}) // Mock rationale: Force no anomaly by returning 0, which is less than any positive AnomalyChance.
	defer cleanup()

	anchor := TemporalAnchor{
		Name:             "Test Anchor",
		SimulatedDelayMs: 100,
		AnomalyChance:    10, // Should not trigger with mockRand.Intn returning 0
	}

	report := listenToAnchor(anchor)

	if report.AnchorName != "Test Anchor" {
		t.Errorf("Expected AnchorName 'Test Anchor', got '%s'", report.AnchorName)
	}
	if report.Status != "STABLE" {
		t.Errorf("Expected Status 'STABLE', got '%s'", report.Status)
	}
	if report.Error != "" {
		t.Errorf("Expected no error, got '%s'", report.Error)
	}
	if report.DurationMs < 0 { // Duration will be near 0 because mockSleep does nothing.
		t.Errorf("Expected non-negative duration, got %d", report.DurationMs)
	}
}

func TestListenToAnchor_Anomaly(t *testing.T) {
	cleanup := setupMocks([]int{5}) // Mock rationale: Force anomaly by returning 5, which is less than AnomalyChance 10.
	defer cleanup()

	anchor := TemporalAnchor{
		Name:             "Anomaly Anchor",
		SimulatedDelayMs: 100,
		AnomalyChance:    10, // Should trigger with mockRand.Intn returning 5
	}

	report := listenToAnchor(anchor)

	if report.AnchorName != "Anomaly Anchor" {
		t.Errorf("Expected AnchorName 'Anomaly Anchor', got '%s'", report.AnchorName)
	}
	if report.Status != "ANOMALY DETECTED" {
		t.Errorf("Expected Status 'ANOMALY DETECTED', got '%s'", report.Status)
	}
	if report.Error == "" {
		t.Errorf("Expected an error message, got empty")
	}
	if report.DurationMs < 0 { // Duration will be near 0 because mockSleep does nothing.
		t.Errorf("Expected non-negative duration, got %d", report.DurationMs)
	}
}

func TestRunListener_ConcurrencyAndReporting(t *testing.T) {
	// Mock rationale: We need to mock sleep and rand.Intn to ensure deterministic
	// behavior and prevent actual delays during testing. The `mockRandIntn` values
	// are chosen to produce a mix of stable and anomalous reports for the predefined anchors.
	cleanup := setupMocks([]int{
		0,  // Alpha Stream: Stable (0 < 5 is false)
		15, // Beta Nexus: Stable (15 < 10 is false)
		0,  // Gamma Chronos: Stable (0 < 2 is false)
		10, // Delta Rift: Anomaly (10 < 25 is true)
		0,  // Epsilon Echo: Stable (0 < 8 is false)
	})
	defer cleanup()

	reports := runListener()

	if len(reports) != 5 {
		t.Fatalf("Expected 5 reports, got %d", len(reports))
	}

	// Sort reports by name for deterministic checking, as goroutine completion order is not guaranteed.
	sort.Slice(reports, func(i, j int) bool {
		return reports[i].AnchorName < reports[j].AnchorName
	})

	// Define expected results in sorted order of AnchorName
	expectedSorted := []struct {
		name   string
		status string
		hasErr bool
	}{
		{"Alpha Stream", "STABLE", false},
		{"Beta Nexus", "STABLE", false},
		{"Delta Rift", "ANOMALY DETECTED", true},
		{"Epsilon Echo", "STABLE", false},
		{"Gamma Chronos", "STABLE", false},
	}

	for i, r := range reports {
		if r.AnchorName != expectedSorted[i].name {
			t.Errorf("Report %d: Expected AnchorName '%s', got '%s'", i, expectedSorted[i].name, r.AnchorName)
		}
		if r.Status != expectedSorted[i].status {
			t.Errorf("Report %d: Expected Status '%s' for '%s', got '%s'", i, expectedSorted[i].status, r.AnchorName, r.Status)
		}
		if (r.Error != "") != expectedSorted[i].hasErr {
			t.Errorf("Report %d: Expected hasErr %t for '%s', got hasErr %t (Error: '%s')", i, expectedSorted[i].hasErr, r.AnchorName, (r.Error != ""), r.Error)
		}
		if r.DurationMs < 0 {
			t.Errorf("Report %d: Expected non-negative duration for '%s', got %d", i, r.AnchorName, r.DurationMs)
		}
	}
}
