package main

import (
	"context"
	"errors"
	"fmt"
	"sync"
	"testing"
	"time"
)

// MockPinger implements the Pinger interface for testing.
// # Mock rationale: This mock allows us to simulate network responses (latencies, errors)
// # without making actual network calls, ensuring tests are fast, deterministic, and offline.
type MockPinger struct {
	Latencies []time.Duration
	Errors    []error
	CallCount int
	Mu        sync.Mutex
}

// Ping returns predefined latencies or errors from its internal slices.
func (mp *MockPinger) Ping(ctx context.Context, host string, timeout time.Duration) (time.Duration, error) {
	mp.Mu.Lock()
	defer mp.Mu.Unlock()

	if mp.CallCount >= len(mp.Latencies) && mp.CallCount >= len(mp.Errors) {
		// Default to a small latency if no more predefined values
		return 10 * time.Millisecond, nil
	}

	var latency time.Duration
	if mp.CallCount < len(mp.Latencies) {
		latency = mp.Latencies[mp.CallCount]
	}

	var err error
	if mp.CallCount < len(mp.Errors) {
		err = mp.Errors[mp.CallCount]
	}

	mp.CallCount++

	select {
	case <-ctx.Done():
		return 0, ctx.Err()
	default:
		return latency, err
	}
}

func TestPingResult_calculateStats(t *testing.T) {
	tests := []struct {
		name        string
		latencies   []time.Duration
		expAvgMs    float64
		expJitterMs float64
		expScore    float64
	}{
		{
			name:        "Stable connection",
			latencies:   []time.Duration{10 * time.Millisecond, 12 * time.Millisecond, 11 * time.Millisecond, 10 * time.Millisecond},
			expAvgMs:    10.75,
			expJitterMs: 0.83,
			expScore:    86.6, // 1000 / (10.75 + 0.83 + 1) = 1000 / 12.58 = 79.49 (re-calc: 1000 / (10.75 + 0.829 + 1) = 1000 / 12.579 = 79.49)
			// Actual: 1000 / (10.75 + 0.829156 + 1) = 1000 / 12.579156 = 79.49
			// Let's use 1000 / (10.75 + 0.83 + 1) = 79.49
			// For test, let's round to 1 decimal place for score
			expScore: 79.5,
		},
		{
			name:        "Jittery connection",
			latencies:   []time.Duration{50 * time.Millisecond, 100 * time.Millisecond, 60 * time.Millisecond, 90 * time.Millisecond},
			expAvgMs:    75.00,
			expJitterMs: 19.36,
			expScore:    10.4, // 1000 / (75 + 19.36 + 1) = 1000 / 95.36 = 10.48
		},
		{
			name:        "No pings",
			latencies:   []time.Duration{},
			expAvgMs:    0,
			expJitterMs: 0,
			expScore:    0,
		},
		{
			name:        "Single ping",
			latencies:   []time.Duration{20 * time.Millisecond},
			expAvgMs:    20.00,
			expJitterMs: 0.00,
			expScore:    47.6, // 1000 / (20 + 0 + 1) = 1000 / 21 = 47.61
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			pr := PingResult{Host: "test", Latencies: tt.latencies}
			pr.calculateStats()

			if math.Abs(float64(pr.AvgLatency.Milliseconds())-tt.expAvgMs) > 0.01 {
				t.Errorf("AvgLatency got %v, want %v", pr.AvgLatency.Milliseconds(), tt.expAvgMs)
			}
			if math.Abs(float64(pr.Jitter.Milliseconds())-tt.expJitterMs) > 0.01 {
				t.Errorf("Jitter got %v, want %v", pr.Jitter.Milliseconds(), tt.expJitterMs)
			}
			if math.Abs(pr.Entanglement-tt.expScore) > 0.1 {
				t.Errorf("Entanglement Score got %.1f, want %.1f", pr.Entanglement, tt.expScore)
			}
		})
	}
}

func TestRealPinger_Ping(t *testing.T) {
	// This test requires actual network access, so it's commented out by default
	// to ensure deterministic offline tests. It can be uncommented for integration testing.
	// # Mock rationale: This test is an integration test, not a unit test. For unit tests,
	// # we rely on the MockPinger. This is here to demonstrate how a real pinger would be tested.
	/*
		t.Skip("Skipping real pinger test to ensure offline determinism")
		rp := &RealPinger{}
		host := "google.com"
		timeout := 2 * time.Second
		ctx, cancel := context.WithTimeout(context.Background(), timeout)
		defer cancel()

		latency, err := rp.Ping(ctx, host, timeout)
		if err != nil {
			t.Fatalf("Ping failed: %v", err)
		}
		if latency <= 0 {
			t.Errorf("Expected positive latency, got %v", latency)
		}
		fmt.Printf("Real ping to %s: %v\n", host, latency)
	*/
}

func TestMockPinger(t *testing.T) {
	// Test successful pings
	mp := &MockPinger{
		Latencies: []time.Duration{10 * time.Millisecond, 20 * time.Millisecond},
		Errors:    []error{nil, nil},
	}

	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()

	lat1, err1 := mp.Ping(ctx, "host1", 1*time.Second)
	if err1 != nil || lat1 != 10*time.Millisecond {
		t.Errorf("Expected 10ms, nil; got %v, %v", lat1, err1)
	}

	lat2, err2 := mp.Ping(ctx, "host1", 1*time.Second)
	if err2 != nil || lat2 != 20 * time.Millisecond {
		t.Errorf("Expected 20ms, nil; got %v, %v", lat2, err2)
	}

	// Test error handling
	mp = &MockPinger{
		Latencies: []time.Duration{10 * time.Millisecond},
		Errors:    []error{errors.New("connection refused")},
	}
	mp.CallCount = 0 // Reset call count for new mock instance

	lat3, err3 := mp.Ping(ctx, "host2", 1*time.Second)
	if err3 == nil || lat3 != 10*time.Millisecond || err3.Error() != "connection refused" {
		t.Errorf("Expected 10ms, 'connection refused'; got %v, %v", lat3, err3)
	}

	// Test context cancellation
	mp = &MockPinger{
		Latencies: []time.Duration{100 * time.Millisecond},
		Errors:    []error{nil},
	}
	mp.CallCount = 0

	ctxCancel, cancelCancel := context.WithCancel(context.Background())
	cancelCancel()
	lat4, err4 := mp.Ping(ctxCancel, "host3", 1*time.Second)
	if err4 == nil || err4 != context.Canceled {
		t.Errorf("Expected context.Canceled error, got %v", err4)
	}
	_ = lat4 // latency might be 0 or the mocked value depending on timing
}
