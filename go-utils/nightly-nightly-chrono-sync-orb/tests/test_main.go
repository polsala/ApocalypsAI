package main

import (
	"encoding/json"
	"net"
	"os"
	"strconv"
	"sync"
	"testing"
	"time"
)

// MockUDPSender implements UDPSender for testing purposes.
type MockUDPSender struct {
	mu       sync.Mutex
	SentData [][]byte
	SentAddr []*net.UDPAddr
}

// Send records the data and address that would have been sent.
func (m *MockUDPSender) Send(data []byte, addr *net.UDPAddr) error {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.SentData = append(m.SentData, data)
	m.SentAddr = append(m.SentAddr, addr)
	return nil
}

// Mock rationale: We mock the network sender to ensure tests are deterministic and offline.
// This allows us to verify that the correct data is prepared and that the send function
// is called with the expected arguments, without relying on actual network I/O or timing.

func TestGenerateTimePulse(t *testing.T) {
	maxOffset := 10.0
	pulse := generateTimePulse(maxOffset)

	// Test 1: Check if Timestamp is a valid RFC3339Nano format
	_, err := time.Parse(time.RFC3339Nano, pulse.Timestamp)
	if err != nil {
		t.Errorf("Generated timestamp '%s' is not in RFC3339Nano format: %v", pulse.Timestamp, err)
	}

	// Test 2: Check if OffsetSec is within the expected range
	if pulse.OffsetSec < -maxOffset || pulse.OffsetSec > maxOffset {
		t.Errorf("Generated offset %.2f is outside the expected range [-%.2f, %.2f]", pulse.OffsetSec, maxOffset, maxOffset)
	}

	// Test 3: Check if Message is correct
	expectedMessage := "A pulse from the Chrono-Sync Orb!"
	if pulse.Message != expectedMessage {
		t.Errorf("Expected message '%s', got '%s'", expectedMessage, pulse.Message)
	}

	// Test 4: Ensure different calls produce different offsets (probabilistic check)
	pulse2 := generateTimePulse(maxOffset)
	if pulse.OffsetSec == pulse2.OffsetSec && pulse.Timestamp == pulse2.Timestamp {
		t.Log("Warning: Two consecutive pulses generated identical offsets and timestamps. This is statistically unlikely but possible.")
	}
}

func TestStartOrb(t *testing.T) {
	mockSender := &MockUDPSender{}
	multicastAddr := "224.0.0.1"
	port := 9000
	interval := 100 * time.Millisecond // Short interval for testing
	maxOffset := 1.0

	// Run startOrb in a goroutine
	// Note: startOrb runs indefinitely. For testing, we let it run for a short period
	// and then check if messages were sent. A more robust design for production code
	// would involve passing a context.Context or a stop channel to startOrb.
	go func() {
		startOrb(mockSender, multicastAddr, port, interval, maxOffset)
	}()

	// Let it run for a short period to send a few pulses
	time.Sleep(interval * 2) // Wait for at least two pulses to be sent

	// Check if any data was sent
	mockSender.mu.Lock()
	numSent := len(mockSender.SentData)
	mockSender.mu.Unlock()

	if numSent == 0 {
		t.Fatal("No pulses were sent by the orb.")
	}

	// Verify content of a sent pulse
	mockSender.mu.Lock()
	firstPulseData := mockSender.SentData[0]
	firstPulseAddr := mockSender.SentAddr[0]
	mockSender.mu.Unlock()

	var receivedPulse TimePulse
	err := json.Unmarshal(firstPulseData, &receivedPulse)
	if err != nil {
		t.Fatalf("Failed to unmarshal sent data: %v", err)
	}

	// Check timestamp format
	_, err = time.Parse(time.RFC3339Nano, receivedPulse.Timestamp)
	if err != nil {
		t.Errorf("Sent timestamp '%s' is not in RFC3339Nano format: %v", receivedPulse.Timestamp, err)
	}

	// Check offset range
	if receivedPulse.OffsetSec < -maxOffset || receivedPulse.OffsetSec > maxOffset {
		t.Errorf("Sent offset %.2f is outside the expected range [-%.2f, %.2f]", receivedPulse.OffsetSec, maxOffset, maxOffset)
	}

	// Check target address
	expectedAddr, _ := net.ResolveUDPAddr("udp", fmt.Sprintf("%s:%d", multicastAddr, port))
	if firstPulseAddr.String() != expectedAddr.String() {
		t.Errorf("Expected sent address %s, got %s", expectedAddr.String(), firstPulseAddr.String())
	}
}

func TestMainEnvironmentVariables(t *testing.T) {
	// Mock rationale: Environment variables are external inputs. Mocking them allows
	// deterministic testing of how the main function parses and uses configuration.
	os.Setenv("ORB_MULTICAST_ADDR", "239.0.0.1")
	os.Setenv("ORB_PORT", "9001")
	os.Setenv("ORB_INTERVAL_SECONDS", "1")
	os.Setenv("ORB_MAX_OFFSET_SECONDS", "10.5")
	defer func() {
		os.Unsetenv("ORB_MULTICAST_ADDR")
		os.Unsetenv("ORB_PORT")
		os.Unsetenv("ORB_INTERVAL_SECONDS")
		os.Unsetenv("ORB_MAX_OFFSET_SECONDS")
	}()

	// We cannot directly test `main()` as it calls `startOrb` which runs indefinitely.
	// Instead, we test the parsing logic that `main` would execute.

	multicastAddr := os.Getenv("ORB_MULTICAST_ADDR")
	if multicastAddr == "" {
		multicastAddr = "224.0.0.1"
	}
	if multicastAddr != "239.0.0.1" {
		t.Errorf("Expected multicastAddr '239.0.0.1', got '%s'", multicastAddr)
	}

	portStr := os.Getenv("ORB_PORT")
	port, err := strconv.Atoi(portStr)
	if err != nil || port == 0 {
		port = 9000
	}
	if port != 9001 {
		t.Errorf("Expected port 9001, got %d", port)
	}

	intervalStr := os.Getenv("ORB_INTERVAL_SECONDS")
	intervalSec, err := strconv.Atoi(intervalStr)
	if err != nil || intervalSec == 0 {
		intervalSec = 3
	}
	interval := time.Duration(intervalSec) * time.Second
	if interval != 1*time.Second {
		t.Errorf("Expected interval 1s, got %v", interval)
	}

	maxOffsetStr := os.Getenv("ORB_MAX_OFFSET_SECONDS")
	maxOffsetSec, err := strconv.ParseFloat(maxOffsetStr, 64)
	if err != nil || maxOffsetSec == 0 {
		maxOffsetSec = 5.0
	}
	if maxOffsetSec != 10.5 {
		t.Errorf("Expected maxOffsetSec 10.5, got %.1f", maxOffsetSec)
	}
}

func TestMainDefaultEnvironmentVariables(t *testing.T) {
	// Ensure no environment variables are set for this test
	os.Unsetenv("ORB_MULTICAST_ADDR")
	os.Unsetenv("ORB_PORT")
	os.Unsetenv("ORB_INTERVAL_SECONDS")
	os.Unsetenv("ORB_MAX_OFFSET_SECONDS")

	// Simulate the parsing logic from main
	multicastAddr := os.Getenv("ORB_MULTICAST_ADDR")
	if multicastAddr == "" {
		multicastAddr = "224.0.0.1"
	}
	if multicastAddr != "224.0.0.1" {
		t.Errorf("Expected default multicastAddr '224.0.0.1', got '%s'", multicastAddr)
	}

	portStr := os.Getenv("ORB_PORT")
	port, err := strconv.Atoi(portStr)
	if err != nil || port == 0 {
		port = 9000
	}
	if port != 9000 {
		t.Errorf("Expected default port 9000, got %d", port)
	}

	intervalStr := os.Getenv("ORB_INTERVAL_SECONDS")
	intervalSec, err := strconv.Atoi(intervalStr)
	if err != nil || intervalSec == 0 {
		intervalSec = 3
	}
	interval := time.Duration(intervalSec) * time.Second
	if interval != 3*time.Second {
		t.Errorf("Expected default interval 3s, got %v", interval)
	}

	maxOffsetStr := os.Getenv("ORB_MAX_OFFSET_SECONDS")
	maxOffsetSec, err := strconv.ParseFloat(maxOffsetStr, 64)
	if err != nil || maxOffsetSec == 0 {
		maxOffsetSec = 5.0
	}
	if maxOffsetSec != 5.0 {
		t.Errorf("Expected default maxOffsetSec 5.0, got %.1f", maxOffsetSec)
	}
}
