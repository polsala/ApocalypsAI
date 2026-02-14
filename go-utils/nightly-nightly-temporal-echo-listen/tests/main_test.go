package main

import (
	"bytes"
	"fmt"
	"log"
	"net"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// MockPacketConn implements net.PacketConn for testing purposes.
type MockPacketConn struct {
	readBuffer  chan []byte
	writeBuffer chan []byte
	closeOnce   sync.Once
	closed      chan struct{}
}

func NewMockPacketConn() *MockPacketConn {
	return &MockPacketConn{
		readBuffer:  make(chan []byte, 10), // Buffer for incoming data
		writeBuffer: make(chan []byte, 10), // Buffer for outgoing data (not used in this util, but good practice)
		closed:      make(chan struct{}),
	}
}

func (m *MockPacketConn) ReadFrom(p []byte) (n int, addr net.Addr, err error) {
	select {
	case data := <-m.readBuffer:
		n = copy(p, data)
		return n, &net.UDPAddr{IP: net.ParseIP("127.0.0.1"), Port: 12345}, nil
	case <-m.closed:
		return 0, nil, net.ErrClosed
	case <-time.After(100 * time.Millisecond): // Timeout to prevent tests from hanging indefinitely
		return 0, nil, fmt.Errorf("read timeout")
	}
}

func (m *MockPacketConn) WriteTo(p []byte, addr net.Addr) (n int, err error) {
	select {
	case m.writeBuffer <- p:
		return len(p), nil
	case <-m.closed:
		return 0, net.ErrClosed
	}
}

func (m *MockPacketConn) Close() error {
	m.closeOnce.Do(func() {
		close(m.closed)
	}) // Close the channel only once
	return nil
}

func (m *MockPacketConn) LocalAddr() net.Addr {
	return &net.UDPAddr{IP: net.ParseIP("127.0.0.1"), Port: 8080}
}

func (m *MockPacketConn) SetDeadline(t time.Time) error { return nil }
func (m *MockPacketConn) SetReadDeadline(t time.Time) error { return nil }
func (m *MockPacketConn) SetWriteDeadline(t time.Time) error { return nil }

// InjectData simulates receiving a UDP packet.
func (m *MockPacketConn) InjectData(data []byte) {
	m.readBuffer <- data
}

// TestParseEchoMessage tests the parsing of echo messages.
func TestParseEchoMessage(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected *EchoMessage
		err      bool
	}{
		{
			name:  "Valid message",
			input: fmt.Sprintf("%d|msg-1|Hello", time.Now().UnixMilli()),
			expected: &EchoMessage{
				MessageID: "msg-1",
				Payload:   "Hello",
			},
			err: false,
		},
		{
			name:  "Invalid format - too few parts",
			input: "123|msg-2",
			expected: nil,
			err: true,
		},
		{
			name:  "Invalid format - too many parts",
			input: "123|msg-3|Hello|Extra",
			expected: nil,
			err: true,
		},
		{
			name:  "Invalid timestamp",
			input: "not-a-timestamp|msg-4|World",
			expected: nil,
			err: true,
		},
		{
			name:  "Empty payload",
			input: fmt.Sprintf("%d|msg-5|", time.Now().UnixMilli()),
			expected: &EchoMessage{
				MessageID: "msg-5",
				Payload:   "",
			},
			err: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			echo, err := ParseEchoMessage([]byte(tt.input))

			if (err != nil) != tt.err {
				t.Errorf("ParseEchoMessage() error = %v, wantErr %v", err, tt.err)
				return
			}
			if !tt.err {
				if echo.MessageID != tt.expected.MessageID || echo.Payload != tt.expected.Payload {
					t.Errorf("ParseEchoMessage() got = %+v, want %+v", echo, tt.expected)
				}
				// Check timestamp is roughly correct (within a second of now for valid messages)
				if tt.name == "Valid message" && time.Since(echo.Timestamp) > time.Second {
					t.Errorf("ParseEchoMessage() timestamp too old: %v", echo.Timestamp)
				}
			}
		})
	}
}

// TestDetectAnomalies tests the anomaly detection logic.
func TestDetectAnomalies(t *testing.T) {
	var logBuffer bytes.Buffer
	log.SetOutput(&logBuffer)
	defer func() {
		log.SetOutput(os.Stderr) // Reset log output
	}()

	fixedTime := time.Date(2023, time.January, 1, 12, 0, 0, 0, time.UTC)
	currentTimeProvider := func() time.Time { return fixedTime } // Mock rationale: Provides a controlled current time for deterministic temporal anomaly checks.

	ep := NewEchoProcessor(temporalDriftThreshold, duplicateWindow, currentTimeProvider)

	// Test 1: No anomaly
	logBuffer.Reset()
	echo1 := &EchoMessage{Timestamp: fixedTime.Add(-1 * time.Second), MessageID: "normal-1", Payload: "hello"}
	ep.DetectAnomalies(echo1)
	if strings.Contains(logBuffer.String(), "[ANOMALY") {
		t.Errorf("Expected no anomaly, got: %s", logBuffer.String())
	}

	// Test 2: Echo from the future
	logBuffer.Reset()
	echoFuture := &EchoMessage{Timestamp: fixedTime.Add(20 * time.Second), MessageID: "future-1", Payload: "future"}
	ep.DetectAnomalies(echoFuture)
	if !strings.Contains(logBuffer.String(), "[ANOMALY: Temporal Drift] Echo from the future detected") {
		t.Errorf("Expected future anomaly, got: %s", logBuffer.String())
	}

	// Test 3: Echo from the past
	logBuffer.Reset()
	echoPast := &EchoMessage{Timestamp: fixedTime.Add(-20 * time.Second), MessageID: "past-1", Payload: "past"}
	ep.DetectAnomalies(echoPast)
	if !strings.Contains(logBuffer.String(), "[ANOMALY: Temporal Drift] Echo from the past detected") {
		t.Errorf("Expected past anomaly, got: %s", logBuffer.String())
	}

	// Test 4: Duplicate echo within window
	logBuffer.Reset()
	echoDuplicate := &EchoMessage{Timestamp: fixedTime.Add(-2 * time.Second), MessageID: "dup-1", Payload: "first"}
	ep.DetectAnomalies(echoDuplicate) // First reception, no anomaly
	if strings.Contains(logBuffer.String(), "[ANOMALY: Echo Duplication]") {
		t.Errorf("Expected no duplication anomaly on first reception, got: %s", logBuffer.String())
	}

	logBuffer.Reset()
	// Simulate a short time passing, but still within duplicate window
	fixedTime = fixedTime.Add(1 * time.Second)
	ep.currentTimeProvider = func() time.Time { return fixedTime } // Update mock time
	echoDuplicate2 := &EchoMessage{Timestamp: fixedTime.Add(-3 * time.Second), MessageID: "dup-1", Payload: "second"}
	ep.DetectAnomalies(echoDuplicate2) // Second reception, should be a duplicate
	if !strings.Contains(logBuffer.String(), "[ANOMALY: Echo Duplication] Duplicate echo detected for dup-1") {
		t.Errorf("Expected duplication anomaly, got: %s", logBuffer.String())
	}

	// Test 5: Duplicate echo outside window (should not be an anomaly)
	logBuffer.Reset()
	fixedTime = fixedTime.Add(duplicateWindow + 1*time.Second) // Move time past the duplicate window
	ep.currentTimeProvider = func() time.Time { return fixedTime } // Update mock time
	echoDuplicate3 := &EchoMessage{Timestamp: fixedTime.Add(-1 * time.Second), MessageID: "dup-1", Payload: "third"}
	ep.DetectAnomalies(echoDuplicate3)
	if strings.Contains(logBuffer.String(), "[ANOMALY: Echo Duplication]") {
		t.Errorf("Expected no duplication anomaly outside window, got: %s", logBuffer.String())
	}
}

// TestConcurrentEchoProcessing simulates concurrent reception and processing.
func TestConcurrentEchoProcessing(t *testing.T) {
	var logBuffer bytes.Buffer
	log.SetOutput(&logBuffer)
	defer func() {
		log.SetOutput(os.Stderr) // Reset log output
	}()

	mockConn := NewMockPacketConn() // Mock rationale: Simulates UDP packet reception without actual network I/O.
	processor := NewEchoProcessor(temporalDriftThreshold, duplicateWindow, time.Now) // Use real time for this test

	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		runListener(mockConn, processor) // Call the refactored listener function
	}()

	// Inject multiple echoes concurrently
	numEchoes := 100
	for i := 0; i < numEchoes; i++ {
		msgID := fmt.Sprintf("concurrent-msg-%d", i%10) // Create some duplicates
		timestamp := time.Now().Add(time.Duration(i%5)*time.Millisecond).UnixMilli() // Slightly varying timestamps
		mockConn.InjectData([]byte(fmt.Sprintf("%d|%s|Payload-%d", timestamp, msgID, i)))
	}

	// Inject a future message
	mockConn.InjectData([]byte(fmt.Sprintf("%d|future-msg|FuturePayload", time.Now().Add(20*time.Second).UnixMilli())))

	// Give some time for processing
	time.Sleep(500 * time.Millisecond)

	mockConn.Close() // Close the mock connection to stop the reader goroutine
	wg.Wait()        // Wait for the runListener goroutine to finish

	output := logBuffer.String()
	if !strings.Contains(output, "[ANOMALY: Temporal Drift] Echo from the future detected for future-msg") {
		t.Errorf("Expected future anomaly in concurrent test, got: %s", output)
	}
	// Check for at least some duplication anomalies
	if !strings.Contains(output, "[ANOMALY: Echo Duplication]") {
		t.Errorf("Expected some duplication anomalies in concurrent test, got: %s", output)
	}
	// Verify that the processor's internal state is consistent (e.g., map size)
	processor.mu.Lock()
	numUniqueEchoes := len(processor.recentEchoes)
	processor.mu.Unlock()
	if numUniqueEchoes == 0 { // Should be at least 10 unique message IDs + 1 future message
		t.Errorf("Expected processor to have processed unique echoes, but map is empty.")
	}
}
