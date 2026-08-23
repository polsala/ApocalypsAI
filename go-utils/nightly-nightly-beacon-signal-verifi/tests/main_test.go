package main

import (
	"fmt"
	"strings"
	"testing"
	"time"
)

// MockPinger implements the Pinger interface for testing.
type MockPinger struct {
	Results map[string]PingResult // Key: "host:port"
}

// Mock rationale: This mock allows simulating network responses (success/failure, latency)
// without making actual network calls, ensuring deterministic and offline tests.
func (mp *MockPinger) Ping(host string, port int, timeout time.Duration) PingResult {
	key := fmt.Sprintf("%s:%d", host, port)
	if result, ok := mp.Results[key]; ok {
		// Ensure OriginalBeacon is set if it wasn't in the mock setup
		if result.OriginalBeacon == "" {
			result.OriginalBeacon = key
		}
		return result
	}
	// Default to failure if not explicitly mocked
	return PingResult{
		OriginalBeacon: key,
		Host:           host,
		Port:           port,
		Success:        false,
		Error:          "Mocked: Host not found or default failure",
	}
}

func TestParseBeacon(t *testing.T) {
	tests := []struct {
		input        string
		expectedHost string
		expectedPort int
		expectError  bool
	}{
		{"google.com:80", "google.com", 80, false},
		{"localhost:8080", "localhost", 8080, false},
		{"192.168.1.1:22", "192.168.1.1", 22, false},
		{"invalid-format", "", 0, true},
		{"host:port:extra", "", 0, true},
		{"host:abc", "", 0, true},
		{":80", "", 80, false}, // Valid, host can be empty
		{"google.com:", "", 0, true}, // Invalid port
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			host, port, err := parseBeacon(tt.input)

			if tt.expectError {
				if err == nil {
					t.Errorf("Expected error for input '%s', but got none", tt.input)
				}
			} else {
				if err != nil {
					t.Errorf("Did not expect error for input '%s', but got: %v", tt.input, err)
				}
				if host != tt.expectedHost {
					t.Errorf("Expected host '%s', got '%s'", tt.expectedHost, host)
				}
				if port != tt.expectedPort {
					t.Errorf("Expected port %d, got %d", tt.expectedPort, port)
				}
			}
		})
	}
}

func TestRunVerification(t *testing.T) {
	mockPinger := &MockPinger{
		Results: map[string]PingResult{
			"beacon1.com:80": {
				OriginalBeacon: "beacon1.com:80",
				Host:           "beacon1.com",
				Port:           80,
				Success:        true,
				Latency:        10 * time.Millisecond,
			},
			"beacon2.com:443": {
				OriginalBeacon: "beacon2.com:443",
				Host:           "beacon2.com",
				Port:           443,
				Success:        false,
				Error:          "connection refused",
			},
			"beacon3.com:22": {
				OriginalBeacon: "beacon3.com:22",
				Host:           "beacon3.com",
				Port:           22,
				Success:        true,
				Latency:        50 * time.Millisecond,
			},
		},
	}

	beacons := []string{
		"beacon1.com:80",
		"beacon2.com:443",
		"invalid-beacon-format", // This should be handled by parseBeacon
		"beacon3.com:22",
	}
	timeout := 1 * time.Second

	results := runVerification(mockPinger, beacons, timeout)

	if len(results) != len(beacons) {
		t.Fatalf("Expected %d results, got %d", len(beacons), len(results))
	}

	// Check results for beacon1.com:80
	found1 := false
	for _, res := range results {
		if res.OriginalBeacon == "beacon1.com:80" {
			found1 = true
			if !res.Success {
				t.Errorf("beacon1.com:80 expected success, got failure")
			}
			if res.Latency != 10*time.Millisecond {
				t.Errorf("beacon1.com:80 expected latency 10ms, got %s", res.Latency)
			}
		}
	}
	if !found1 {
		t.Errorf("Result for beacon1.com:80 not found")
	}

	// Check results for beacon2.com:443
	found2 := false
	for _, res := range results {
		if res.OriginalBeacon == "beacon2.com:443" {
			found2 = true
			if res.Success {
				t.Errorf("beacon2.com:443 expected failure, got success")
			}
			if !strings.Contains(res.Error, "connection refused") {
				t.Errorf("beacon2.com:443 expected 'connection refused' error, got '%s'", res.Error)
			}
		}
	}
	if !found2 {
		t.Errorf("Result for beacon2.com:443 not found")
	}

	// Check results for invalid-beacon-format
	foundInvalid := false
	for _, res := range results {
		if res.OriginalBeacon == "invalid-beacon-format" {
			foundInvalid = true
			if res.Success {
				t.Errorf("invalid-beacon-format expected failure, got success")
			}
			if !strings.Contains(res.Error, "Invalid beacon 'invalid-beacon-format': invalid format. Expected host:port") {
				t.Errorf("invalid-beacon-format expected specific error, got '%s'", res.Error)
			}
		}
	}
	if !foundInvalid {
		t.Errorf("Result for invalid-beacon-format not found")
	}
}

func TestRunVerification_AllDown(t *testing.T) {
	mockPinger := &MockPinger{
		Results: map[string]PingResult{
			"down1.com:80": {
				OriginalBeacon: "down1.com:80",
				Host:           "down1.com",
				Port:           80,
				Success:        false,
				Error:          "timeout",
			},
			"down2.com:443": {
				OriginalBeacon: "down2.com:443",
				Host:           "down2.com",
				Port:           443,
				Success:        false,
				Error:          "host unreachable",
			},
		},
	}

	beacons := []string{"down1.com:80", "down2.com:443"}
	timeout := 1 * time.Second

	results := runVerification(mockPinger, beacons, timeout)

	if len(results) != 2 {
		t.Fatalf("Expected 2 results, got %d", len(results))
	}

	for _, res := range results {
		if res.Success {
			t.Errorf("Expected all beacons to be down, but %s:%d was up", res.Host, res.Port)
		}
	}
}

func TestRunVerification_EmptyBeacons(t *testing.T) {
	mockPinger := &MockPinger{}
	beacons := []string{}
	timeout := 1 * time.Second

	results := runVerification(mockPinger, beacons, timeout)

	if len(results) != 0 {
		t.Errorf("Expected 0 results for empty beacons, got %d", len(results))
	}
}
