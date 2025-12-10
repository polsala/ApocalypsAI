package main

import (
	"context"
	"net"
	"testing"
	"time"
)

// MockDialer implements a mock dialer for testing
type MockDialer struct {
	ShouldFail    bool
	FailureReason string
	Latency       time.Duration
}

// DialContext implements the net.Dialer interface for mocking
func (m *MockDialer) DialContext(ctx context.Context, network, address string) (net.Conn, error) {
	if m.Latency > 0 {
		time.Sleep(m.Latency)
	}

	if m.ShouldFail {
		return nil, fmt.Errorf("mock connection failed: %s", m.FailureReason)
	}

	// Return a mock connection (nil is fine for our tests since we close it immediately)
	return nil, nil
}

func TestParseTarget(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expectedHost string
		expectedPort int
		wantErr  bool
	}{
		{
			name: "host with port",
			input: "example.com:8080",
			expectedHost: "example.com",
			expectedPort: 8080,
			wantErr: false,
		},
		{
			name: "host without port",
			input: "example.com",
			expectedHost: "example.com",
			expectedPort: 80,
			wantErr: false,
		},
		{
			name: "localhost with port",
			input: "localhost:3000",
			expectedHost: "localhost",
			expectedPort: 3000,
			wantErr: false,
		},
		{
			name: "invalid port",
			input: "example.com:abc",
			wantErr: true,
		},
		{
			name: "empty target",
			input: "",
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			host, port, err := parseTarget(tt.input)

			if tt.wantErr {
				if err == nil {
					t.Errorf("Expected error but got nil")
				}
				return
			}

			if err != nil {
				t.Errorf("Unexpected error: %v", err)
				return
			}

			if host != tt.expectedHost {
				t.Errorf("Expected host %s, got %s", tt.expectedHost, host)
			}

			if port != tt.expectedPort {
				t.Errorf("Expected port %d, got %d", tt.expectedPort, port)
			}
		})
	}
}

func TestShouldDropPacket(t *testing.T) {
	// Test with 0% packet loss (should never drop)
	for i := 0; i < 100; i++ {
		if shouldDropPacket(0) {
			t.Errorf("Packet should not be dropped with 0%% packet loss")
			break
		}
	}

	// Test with 100% packet loss (should always drop)
	for i := 0; i < 100; i++ {
		if !shouldDropPacket(100) {
			t.Errorf("Packet should be dropped with 100%% packet loss")
			break
		}
	}

	// Test with 50% packet loss (statistical test)
	drops := 0
	total := 1000
	for i := 0; i < total; i++ {
		if shouldDropPacket(50) {
			drops++
		}
	}

	dropRate := float64(drops) / float64(total)
	// Allow some variance in random testing
	if dropRate < 0.4 || dropRate > 0.6 {
		t.Errorf("Expected drop rate around 50%%, got %.2f%%", dropRate*100)
	}
}

func TestGetLatency(t *testing.T) {
	tests := []struct {
		name      string
		baseLatency int
		jitter    int
		minLatency time.Duration
		maxLatency time.Duration
	}{
		{
			name: "no latency or jitter",
			baseLatency: 0,
			jitter: 0,
			minLatency: 0,
			maxLatency: 0,
		},
		{
			name: "latency without jitter",
			baseLatency: 100,
			jitter: 0,
			minLatency: 100 * time.Millisecond,
			maxLatency: 100 * time.Millisecond,
		},
		{
			name: "latency with jitter",
			baseLatency: 100,
			jitter: 50,
			minLatency: 50 * time.Millisecond, // 100 - 50
			maxLatency: 150 * time.Millisecond, // 100 + 50
		},
		{
			name: "high jitter",
			baseLatency: 50,
			jitter: 100,
			minLatency: 0, // clamped to 0
			maxLatency: 150 * time.Millisecond, // 50 + 100
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var minObserved, maxObserved time.Duration = time.Duration(1<<63 - 1), 0
			observations := 1000

			for i := 0; i < observations; i++ {
				latency := getLatency(tt.baseLatency, tt.jitter)
				if latency < minObserved {
					minObserved = latency
				}
				if latency > maxObserved {
					maxObserved = latency
				}
			}

			// Check that observed values are within expected bounds
			if minObserved < tt.minLatency {
				t.Errorf("Min observed latency %v is less than expected %v", minObserved, tt.minLatency)
			}
			if maxObserved > tt.maxLatency {
				t.Errorf("Max observed latency %v is greater than expected %v", maxObserved, tt.maxLatency)
			}

			// For zero jitter cases, check that we get consistent values
			if tt.jitter == 0 && tt.baseLatency > 0 {
				if minObserved != maxObserved {
					t.Errorf("Expected consistent latency with 0 jitter, got range %v-%v", minObserved, maxObserved)
				}
				if minObserved != tt.minLatency {
					t.Errorf("Expected latency %v, got %v", tt.minLatency, minObserved)
				}
			}
		})
	}
}

func TestGetWhimsicalMessage(t *testing.T) {
	// Test success messages
	successMsg := getWhimsicalMessage(true)
	if successMsg == "" {
		t.Error("Expected non-empty success message")
	}

	// Test failure messages
	failureMsg := getWhimsicalMessage(false)
	if failureMsg == "" {
		t.Error("Expected non-empty failure message")
	}

	// Test that we get different messages with repeated calls (probabilistic)
	var successMessages, failureMessages []string
	for i := 0; i < 100; i++ {
		successMessages = append(successMessages, getWhimsicalMessage(true))
		failureMessages = append(failureMessages, getWhimsicalMessage(false))
	}

	// Check we get some variety (not 100% the same message)
	successUnique := make(map[string]bool)
	for _, msg := range successMessages {
		successUnique[msg] = true
	}

	failureUnique := make(map[string]bool)
	for _, msg := range failureMessages {
		failureUnique[msg] = true
	}

	if len(successUnique) < 2 {
		t.Error("Expected more variety in success messages")
	}

	if len(failureUnique) < 2 {
		t.Error("Expected more variety in failure messages")
	}
}

func TestValidateConfig(t *testing.T) {
	tests := []struct {
		name    string
		config  ChaosConfig
		wantErr bool
	}{
		{
			name: "valid config",
			config: ChaosConfig{
				Target:     "example.com",
				Latency:    100,
				PacketLoss: 10,
				Jitter:     50,
				Requests:   10,
				Timeout:    5000,
			},
			wantErr: false,
		},
		{
			name: "missing target",
			config: ChaosConfig{
				Target:     "",
				Latency:    100,
				PacketLoss: 10,
				Jitter:     50,
				Requests:   10,
				Timeout:    5000,
			},
			wantErr: true,
		},
		{
			name: "negative latency",
			config: ChaosConfig{
				Target:     "example.com",
				Latency:    -100,
				PacketLoss: 10,
				Jitter:     50,
				Requests:   10,
				Timeout:    5000,
			},
			wantErr: true,
		},
		{
			name: "invalid packet loss",
			config: ChaosConfig{
				Target:     "example.com",
				Latency:    100,
				PacketLoss: 150,
				Jitter:     50,
				Requests:   10,
				Timeout:    5000,
			},
			wantErr: true,
		},
		{
			name: "negative packet loss",
			config: ChaosConfig{
				Target:     "example.com",
				Latency:    100,
				PacketLoss: -10,
				Jitter:     50,
				Requests:   10,
				Timeout:    5000,
			},
			wantErr: true,
		},
		{
			name: "negative jitter",
			config: ChaosConfig{
				Target:     "example.com",
				Latency:    100,
				PacketLoss: 10,
				Jitter:     -50,
				Requests:   10,
				Timeout:    5000,
			},
			wantErr: true,
		},
		{
			name: "zero requests",
			config: ChaosConfig{
				Target:     "example.com",
				Latency:    100,
				PacketLoss: 10,
				Jitter:     50,
				Requests:   0,
				Timeout:    5000,
			},
			wantErr: true,
		},
		{
			name: "negative timeout",
			config: ChaosConfig{
				Target:     "example.com",
				Latency:    100,
				PacketLoss: 10,
				Jitter:     50,
				Requests:   10,
				Timeout:    -1000,
			},
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := validateConfig(&tt.config)
			if tt.wantErr {
				if err == nil {
					t.Errorf("Expected error but got nil")
				}
				return
			}
			if err != nil {
				t.Errorf("Unexpected error: %v", err)
			}
		})
	}
}

func TestCalculateAverage(t *testing.T) {
	tests := []struct {
		name     string
		latencies []time.Duration
		expected time.Duration
	}{
		{
			name: "single latency",
			latencies: []time.Duration{100 * time.Millisecond},
			expected: 100 * time.Millisecond,
		},
		{
			name: "multiple latencies",
			latencies: []time.Duration{
				100 * time.Millisecond,
				200 * time.Millisecond,
				300 * time.Millisecond,
			},
			expected: 200 * time.Millisecond,
		},
		{
			name: "zero latencies",
			latencies: []time.Duration{0, 0, 0},
			expected: 0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := calculateAverage(tt.latencies)
			if result != tt.expected {
				t.Errorf("Expected average %v, got %v", tt.expected, result)
			}
		})
	}
}

func TestCalculateMin(t *testing.T) {
	tests := []struct {
		name     string
		latencies []time.Duration
		expected time.Duration
	}{
		{
			name: "single latency",
			latencies: []time.Duration{100 * time.Millisecond},
			expected: 100 * time.Millisecond,
		},
		{
			name: "multiple latencies",
			latencies: []time.Duration{
				300 * time.Millisecond,
				100 * time.Millisecond,
				200 * time.Millisecond,
			},
			expected: 100 * time.Millisecond,
		},
		{
			name: "zero latency",
			latencies: []time.Duration{
				100 * time.Millisecond,
				0,
				200 * time.Millisecond,
			},
			expected: 0,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := calculateMin(tt.latencies)
			if result != tt.expected {
				t.Errorf("Expected min %v, got %v", tt.expected, result)
			}
		})
	}
}

func TestCalculateMax(t *testing.T) {
	tests := []struct {
		name     string
		latencies []time.Duration
		expected time.Duration
	}{
		{
			name: "single latency",
			latencies: []time.Duration{100 * time.Millisecond},
			expected: 100 * time.Millisecond,
		},
		{
			name: "multiple latencies",
			latencies: []time.Duration{
				100 * time.Millisecond,
				300 * time.Millisecond,
				200 * time.Millisecond,
			},
			expected: 300 * time.Millisecond,
		},
		{
			name: "zero latency",
			latencies: []time.Duration{
				0,
				100 * time.Millisecond,
				200 * time.Millisecond,
			},
			expected: 200 * time.Millisecond,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := calculateMax(tt.latencies)
			if result != tt.expected {
				t.Errorf("Expected max %v, got %v", tt.expected, result)
			}
		})
	}
}

func TestFormatLatency(t *testing.T) {
	tests := []struct {
		name     string
		duration time.Duration
		expected string
	}{
		{
			name: "zero latency",
			duration: 0,
			expected: "0ms",
		},
		{
			name: "small latency",
			duration: 5 * time.Millisecond,
			expected: "5ms",
		},
		{
			name: "medium latency",
			duration: 150 * time.Millisecond,
			expected: "150ms",
		},
		{
			name: "large latency",
			duration: 5 * time.Second,
			expected: "5000ms",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := formatLatency(tt.duration)
			if result != tt.expected {
				t.Errorf("Expected %s, got %s", tt.expected, result)
			}
		})
	}
}

// Benchmark tests
func BenchmarkShouldDropPacket(b *testing.B) {
	for i := 0; i < b.N; i++ {
		shouldDropPacket(10)
	}
}

func BenchmarkGetLatency(b *testing.B) {
	for i := 0; i < b.N; i++ {
		getLatency(100, 50)
	}
}

func BenchmarkGetWhimsicalMessage(b *testing.B) {
	for i := 0; i < b.N; i++ {
		getWhimsicalMessage(true)
	}
}

func BenchmarkCalculateAverage(b *testing.B) {
	latencies := []time.Duration{
		100 * time.Millisecond,
		200 * time.Millisecond,
		300 * time.Millisecond,
		400 * time.Millisecond,
		500 * time.Millisecond,
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		calculateAverage(latencies)
	}
}

func BenchmarkCalculateMin(b *testing.B) {
	latencies := []time.Duration{
		300 * time.Millisecond,
		100 * time.Millisecond,
		200 * time.Millisecond,
		400 * time.Millisecond,
		500 * time.Millisecond,
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		calculateMin(latencies)
	}
}

func BenchmarkCalculateMax(b *testing.B) {
	latencies := []time.Duration{
		100 * time.Millisecond,
		200 * time.Millisecond,
		300 * time.Millisecond,
		400 * time.Millisecond,
		500 * time.Millisecond,
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		calculateMax(latencies)
	}
}
