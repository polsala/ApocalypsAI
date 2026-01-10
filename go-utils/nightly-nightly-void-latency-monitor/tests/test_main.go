package main

import (
	"errors"
	"testing"
	"time"
)

// MockPinger implements the Pinger interface for testing
type MockPinger struct {
	Results   map[string][]PingResult // Map of address to a slice of results to return
	CallCount map[string]int          // To track how many times Ping is called for an address
}

func (m *MockPinger) Ping(address string, timeout time.Duration) PingResult {
	m.CallCount[address]++
	if results, ok := m.Results[address]; ok && len(results) >= m.CallCount[address] {
		return results[m.CallCount[address]-1]
	}
	// Default fallback if not enough results are provided for an address
	return PingResult{
		Latency:      10 * time.Millisecond,
		Success:      true,
		Error:        nil,
	}
}

func TestMonitor(t *testing.T) {
	// Mock rationale: To ensure deterministic and offline testing, the actual network ping operation is mocked.
	// This allows testing the concurrent execution and result aggregation logic without relying on external network availability or varying latency.

	endpoints := []Endpoint{
		{Name: "Stable Void", Address: "void.stable.com:80"},
		{Name: "Unstable Rift", Address: "rift.unstable.com:80"},
	}
	timeout := 1 * time.Second
	pingCount := 2

	mockPinger := &MockPinger{
		Results: map[string][]PingResult{
			"void.stable.com:80": {
				{Latency: 10 * time.Millisecond, Success: true},
				{Latency: 12 * time.Millisecond, Success: true},
			},
			"rift.unstable.com:80": {
				{Latency: 500 * time.Millisecond, Success: true},
				{Latency: 0, Success: false, Error: errors.New("connection refused")},
			},
		},
		CallCount: make(map[string]int),
	}

	results := Monitor(endpoints, mockPinger, timeout, pingCount)

	// Test Stable Void
	stableResults := results["Stable Void"]
	if len(stableResults) != pingCount {
		t.Errorf("Expected %d results for Stable Void, got %d", pingCount, len(stableResults))
	}
	if !stableResults[0].Success || stableResults[0].Latency != 10*time.Millisecond {
		t.Errorf("Stable Void first ping failed or wrong latency: %+v", stableResults[0])
	}
	if !stableResults[1].Success || stableResults[1].Latency != 12*time.Millisecond {
		t.Errorf("Stable Void second ping failed or wrong latency: %+v", stableResults[1])
	}

	// Test Unstable Rift
	unstableResults := results["Unstable Rift"]
	if len(unstableResults) != pingCount {
		t.Errorf("Expected %d results for Unstable Rift, got %d", pingCount, len(unstableResults))
	}
	if !unstableResults[0].Success || unstableResults[0].Latency != 500*time.Millisecond {
		t.Errorf("Unstable Rift first ping failed or wrong latency: %+v", unstableResults[0])
	}
	if unstableResults[1].Success || unstableResults[1].Error == nil {
		t.Errorf("Unstable Rift second ping expected to fail, but succeeded or no error: %+v", unstableResults[1])
	}

	// Verify call counts
	if mockPinger.CallCount["void.stable.com:80"] != pingCount {
		t.Errorf("Expected pinger to be called %d times for void.stable.com:80, got %d", pingCount, mockPinger.CallCount["void.stable.com:80"])
	}
	if mockPinger.CallCount["rift.unstable.com:80"] != pingCount {
		t.Errorf("Expected pinger to be called %d times for rift.unstable.com:80, got %d", pingCount, mockPinger.CallCount["rift.unstable.com:80"])
	}
}

func TestMonitorEmptyEndpoints(t *testing.T) {
	mockPinger := &MockPinger{
		Results:   make(map[string][]PingResult),
		CallCount: make(map[string]int),
	}
	results := Monitor([]Endpoint{}, mockPinger, 1*time.Second, 1)
	if len(results) != 0 {
		t.Errorf("Expected no results for empty endpoints, got %d", len(results))
	}
}

func TestMonitorZeroPingCount(t *testing.T) {
	endpoints := []Endpoint{
		{Name: "Test", Address: "test.com:80"},
	}
	mockPinger := &MockPinger{
		Results:   make(map[string][]PingResult),
		CallCount: make(map[string]int),
	}
	results := Monitor(endpoints, mockPinger, 1*time.Second, 0)
	if len(results) != 0 { // No pings, so no results should be aggregated
		t.Errorf("Expected no results for zero ping count, got %d", len(results))
	}
	if mockPinger.CallCount["test.com:80"] != 0 {
		t.Errorf("Expected pinger not to be called for zero ping count, but was called %d times", mockPinger.CallCount["test.com:80"])
	}
}
