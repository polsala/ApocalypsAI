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

// MockUDPConn implements net.PacketConn for testing purposes.
type MockUDPConn struct {
	readBuffer  chan []byte
	writeBuffer chan []byte
	closeOnce   sync.Once
	isClosed    chan struct{}
	localAddr   net.Addr
	remoteAddr  net.Addr
}

func NewMockUDPConn(local, remote net.Addr) *MockUDPConn {
	return &MockUDPConn{
		readBuffer:  make(chan []byte, 10), // Buffered channel for incoming messages
		writeBuffer: make(chan []byte, 10), // Buffered channel for outgoing messages
		isClosed:    make(chan struct{}),
		localAddr:   local,
		remoteAddr:  remote,
	}
}

func (m *MockUDPConn) ReadFrom(p []byte) (n int, addr net.Addr, err error) {
	select {
	case <-m.isClosed:
		return 0, nil, &net.OpError{Op: "read", Net: "udp", Source: m.localAddr, Addr: m.remoteAddr, Err: fmt.Errorf("use of closed network connection")}
	case data := <-m.readBuffer:
		n = copy(p, data)
		return n, m.remoteAddr, nil
	case <-time.After(500 * time.Millisecond): // Timeout for read to prevent hanging tests
		return 0, nil, fmt.Errorf("read timeout")
	}
}

func (m *MockUDPConn) WriteTo(p []byte, addr net.Addr) (n int, err error) {
	select {
	case <-m.isClosed:
		return 0, &net.OpError{Op: "write", Net: "udp", Source: m.localAddr, Addr: m.remoteAddr, Err: fmt.Errorf("use of closed network connection")}
	case m.writeBuffer <- p:
		return len(p), nil
	case <-time.After(500 * time.Millisecond): // Timeout for write to prevent hanging tests
		return 0, fmt.Errorf("write timeout")
	}
}

func (m *MockUDPConn) Close() error {
	m.closeOnce.Do(func() {
		close(m.isClosed)
		// Drain channels to prevent goroutine leaks if not all messages were processed
		for len(m.readBuffer) > 0 { <-m.readBuffer }
		for len(m.writeBuffer) > 0 { <-m.writeBuffer }
		close(m.readBuffer)
		close(m.writeBuffer)
	})
	return nil
}

func (m *MockUDPConn) LocalAddr() net.Addr {
	return m.localAddr
}

func (m *MockUDPConn) RemoteAddr() net.Addr {
	return m.remoteAddr
}

func (m *MockUDPConn) SetDeadline(t time.Time) error { return nil }
func (m *MockUDPConn) SetReadDeadline(t time.Time) error { return nil }
func (m *MockUDPConn) SetWriteDeadline(t time.Time) error { return nil }

// Mock rationale: We need to simulate network communication without actual network I/O.
// MockUDPConn allows us to control what data is "sent" and "received" by the beacon and attuner.

func TestParseBeaconMessage(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected BeaconMessage
		hasError bool
	}{
		{
			name:     "Valid message",
			input:    "1678886400000000000|TestBeacon",
			expected: BeaconMessage{Timestamp: 1678886400000000000, SourceID: "TestBeacon"},
			hasError: false,
		},
		{
			name:     "Invalid timestamp",
			input:    "not_a_timestamp|TestBeacon",
			expected: BeaconMessage{}, // Expected zero value on error
			hasError: true,
		},
		{
			name:     "Missing source ID",
			input:    "1678886400000000000",
			expected: BeaconMessage{}, // Expected zero value on error
			hasError: true,
		},
		{
			name:     "Empty message",
			input:    "",
			expected: BeaconMessage{}, // Expected zero value on error
			hasError: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			msg, err := parseBeaconMessage([]byte(tt.input))
			if (err != nil) != tt.hasError {
				t.Errorf("parseBeaconMessage() error = %v, hasError %v", err, tt.hasError)
				return
			}
			if !tt.hasError && msg != tt.expected {
				t.Errorf("parseBeaconMessage() got = %v, want %v", msg, tt.expected)
			}
		})
	}
}

func TestFormatBeaconMessage(t *testing.T) {
	msg := BeaconMessage{Timestamp: 1678886400000000000, SourceID: "TestBeacon"}
	expected := "1678886400000000000|TestBeacon"
	actual := string(formatBeaconMessage(msg))
	if actual != expected {
		t.Errorf("formatBeaconMessage() got = %s, want %s", actual, expected)
	}
}

func TestRunAttunerClient_ReceivesAndReports(t *testing.T) {
	// Mock rationale: Simulate a client receiving a beacon message and exiting gracefully.
	mockConn := NewMockUDPConn(&net.UDPAddr{Port: 1234}, &net.UDPAddr{IP: net.ParseIP("127.0.0.1"), Port: 5678})
	defer mockConn.Close()

	// Override net functions for this test
	originalListenMulticastUDP := netListenMulticastUDP
	originalResolveUDPAddr := netResolveUDPAddr
	netListenMulticastUDP = func(network string, ifi *net.Interface, gaddr *net.UDPAddr) (*net.UDPConn, error) {
		return &net.UDPConn{PacketConn: mockConn}, nil // Wrap mockConn in a net.UDPConn
	}
	netResolveUDPAddr = func(network, address string) (*net.UDPAddr, error) {
		return &net.UDPAddr{IP: net.ParseIP("224.0.0.1"), Port: 9999}, nil // Return a dummy address
	}
	defer func() {
		netListenMulticastUDP = originalListenMulticastUDP
		netResolveUDPAddr = originalResolveUDPAddr
	}()

	// Simulate a beacon message being "sent" to the client
	beaconTime := time.Now().Add(-1 * time.Second) // Beacon time is 1 second in the past
	msg := BeaconMessage{Timestamp: beaconTime.UnixNano(), SourceID: "MockBeacon"}
	mockConn.readBuffer <- formatBeaconMessage(msg)

	var wg sync.WaitGroup
	wg.Add(1)
	var output bytes.Buffer

	// Capture log output for this specific test
	originalOutputWriter := log.Writer()
	log.SetOutput(&output)
	defer log.SetOutput(originalOutputWriter) // Restore original output after test

	go func() {
		defer wg.Done()
		runAttunerClient(defaultPort, defaultMulticastAddr)
	}()

	// Give the client a moment to process the message, then close the mock connection.
	// This will cause runAttunerClient's conn.ReadFromUDP to return a closed network error,
	// which the client is designed to handle by exiting gracefully.
	time.Sleep(50 * time.Millisecond)
	mockConn.Close()
	wg.Wait() // Wait for the client goroutine to finish

	// Assertions on the captured output
	logOutput := output.String()
	if !strings.Contains(logOutput, "Received temporal pulse from MockBeacon") {
		t.Errorf("Expected log output not found: %s", logOutput)
	}
	if !strings.Contains(logOutput, "Temporal Drift:") {
		t.Errorf("Expected 'Temporal Drift' in log output: %s", logOutput)
	}
	// Check if the drift is roughly around 1 second (allowing for test execution time).
	// The actual drift will be slightly less than 1s because receivedTime is captured after beaconTime.
	// We check for "99" (milliseconds) or "1s" (second) to be robust.
	if !strings.Contains(logOutput, "99") && !strings.Contains(logOutput, "1s") {
		t.Errorf("Expected drift of ~1s in log output, got: %s", logOutput)
	}
	// Verify graceful exit message
	if !strings.Contains(logOutput, "Attuner connection closed, exiting.") {
		t.Errorf("Expected graceful exit message not found: %s", logOutput)
	}
}

func TestRunBeaconServer_BroadcastsMessages(t *testing.T) {
	// Mock rationale: Simulate a server broadcasting messages without actual network I/O.
	mockConn := NewMockUDPConn(&net.UDPAddr{Port: 1234}, &net.UDPAddr{IP: net.ParseIP("224.0.0.1"), Port: 9999})
	defer mockConn.Close()

	// Override net functions for this test
	originalListenUDP := netListenUDP
	originalResolveUDPAddr := netResolveUDPAddr
	netListenUDP = func(network string, laddr *net.UDPAddr) (*net.UDPConn, error) {
		return &net.UDPConn{PacketConn: mockConn}, nil
	}
	netResolveUDPAddr = func(network, address string) (*net.UDPAddr, error) {
		return &net.UDPAddr{IP: net.ParseIP("224.0.0.1"), Port: 9999}, nil
	}
	defer func() {
		netListenUDP = originalListenUDP
		netResolveUDPAddr = originalResolveUDPAddr
	}()

	// Run the server in a goroutine
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		// Suppress log output during this test, as we only care about the message being sent.
		originalOutputWriter := log.Writer()
		log.SetOutput(bytes.NewBuffer(nil))
		defer log.SetOutput(originalOutputWriter)

		runBeaconServer(defaultPort, defaultMulticastAddr)
	}()

	// Wait for a message to be "sent" by the server
	select {
	case data := <-mockConn.writeBuffer:
		msg, err := parseBeaconMessage(data)
		if err != nil {
			t.Fatalf("Failed to parse broadcasted message: %v", err)
		}
		if msg.SourceID == "" {
			t.Errorf("Broadcasted message has empty SourceID")
		}
		if msg.Timestamp == 0 {
			t.Errorf("Broadcasted message has empty Timestamp")
		}
		t.Logf("Successfully received broadcasted message: %v", msg)
	case <-time.After(beaconInterval + 100*time.Millisecond): // Wait slightly longer than interval
		t.Fatal("Server did not broadcast a message within expected time")
	}

	// Stop the server goroutine by closing the mock connection
	mockConn.Close()
	wg.Wait() // Ensure the goroutine exits
}

// TestMain function to set up and tear down test environment.
// It suppresses log output globally for all tests by default.
func TestMain(m *testing.M) {
	// Suppress log output during tests by default, unless explicitly redirected within a test.
	log.SetOutput(bytes.NewBuffer(nil))
	code := m.Run()
	os.Exit(code)
}
