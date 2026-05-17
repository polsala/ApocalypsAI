package main

import (
	"errors"
	"fmt"
	"sync"
	"testing"
	"time"
)

// MockPinger implements the Pinger interface for testing.
type MockPinger struct {
	results map[string]struct {
		duration time.Duration
		err      error
	}
	mu sync.Mutex // To protect concurrent map access if needed, though tests are usually sequential.
}

// NewMockPinger creates a new MockPinger with predefined results.
func NewMockPinger(mockResults map[string]struct {
	duration time.Duration
	err      error
}) *MockPinger {
	return &MockPinger{results: mockResults}
}

// Ping returns the predefined result for a given host.
// # Mock rationale: Simulates network responses (success/failure/latency) without actual network calls.
func (m *MockPinger) Ping(host string, port int, timeout time.Duration) (time.Duration, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	key := fmt.Sprintf("%s:%d", host, port)
	if res, ok := m.results[key]; ok {
		return res.duration, res.err
	}
	// Default to a failure if not explicitly mocked
	return 0, errors.New("mock: host not found or default failure")
}

func TestRunPings(t *testing.T) {
	hosts := []string{"anchor1.com", "anchor2.com", "anchor3.com"}
	port := 80
	timeout := 1 * time.Second

	mockResults := map[string]struct {
		duration time.Duration
		err      error
	}{
		"anchor1.com:80": {duration: 10 * time.Millisecond, err: nil},
		"anchor2.com:80": {duration: 0, err: errors.New("connection refused")},
		"anchor3.com:80": {duration: 50 * time.Millisecond, err: nil},
	}
	mockPinger := NewMockPinger(mockResults)

	results := runPings(hosts, port, timeout, mockPinger)

	if len(results) != len(hosts) {
		t.Fatalf("Expected %d results, got %d", len(hosts), len(results))
	}

	// Check results
	for _, res := range results {
		key := fmt.Sprintf("%s:%d", res.Host, res.Port)
		expected := mockResults[key]

		if res.Error != nil && expected.err == nil {
			t.Errorf("Host %s: Expected success, got error: %v", res.Host, res.Error)
		}
		if res.Error == nil && expected.err != nil {
			t.Errorf("Host %s: Expected error '%v', got success", res.Host, expected.err)
		}
		if res.Error == nil && res.Duration != expected.duration {
			t.Errorf("Host %s: Expected duration %s, got %s", res.Host, expected.duration, res.Duration)
		}
		if res.Error != nil && res.Error.Error() != expected.err.Error() {
			t.Errorf("Host %s: Expected error '%v', got '%v'", res.Host, expected.err, res.Error)
		}
	}
}

func TestRunPingsAllSuccess(t *testing.T) {
	hosts := []string{"a.com", "b.com"}
	port := 443
	timeout := 2 * time.Second

	mockResults := map[string]struct {
		duration time.Duration
		err      error
	}{
		"a.com:443": {duration: 20 * time.Millisecond, err: nil},
		"b.com:443": {duration: 30 * time.Millisecond, err: nil},
	}
	mockPinger := NewMockPinger(mockResults)

	results := runPings(hosts, port, timeout, mockPinger)

	if len(results) != len(hosts) {
		t.Fatalf("Expected %d results, got %d", len(hosts), len(results))
	}

	for _, res := range results {
		if res.Error != nil {
			t.Errorf("Host %s: Expected success, got error: %v", res.Host, res.Error)
		}
	}
}

func TestRunPingsAllFailure(t *testing.T) {
	hosts := []string{"c.com", "d.com"}
	port := 22
	timeout := 1 * time.Second

	mockResults := map[string]struct {
		duration time.Duration
		err      error
	}{
		"c.com:22": {duration: 0, err: errors.New("timeout")},
		"d.com:22": {duration: 0, err: errors.New("host unreachable")},
	}
	mockPinger := NewMockPinger(mockResults)

	results := runPings(hosts, port, timeout, mockPinger)

	if len(results) != len(hosts) {
		t.Fatalf("Expected %d results, got %d", len(hosts), len(results))
	}

	for _, res := range results {
		if res.Error == nil {
			t.Errorf("Host %s: Expected failure, got success", res.Host)
		}
	}
}
