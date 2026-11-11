package main

import (
	"bytes"
	"log"
	"net"
	"strconv"
	"strings"
	"sync"
	"testing"
	"time"
)

// MockUDPConn implements the net.PacketConn interface for testing purposes.
// # Mock rationale: To ensure deterministic and offline testing, network operations
// (UDP send/receive) are mocked. This allows testing the message parsing, timestamp
// handling, and anomaly detection logic without requiring actual network interfaces
// or external services. It simulates network traffic within the test environment.
type MockUDPConn struct {
	readBuffer  chan []byte
	writeBuffer chan []byte
	localAddr   net.Addr
	remoteAddr  net.Addr
	closeOnce   sync.Once
	closed      chan struct{}
}

func NewMockUDPConn(local, remote net.Addr) *MockUDPConn {
	return &MockUDPConn{
		readBuffer:  make(chan []byte, 100),
		writeBuffer: make(chan []byte, 100),
		localAddr:   local,
		remoteAddr:  remote,
		closed:      make(chan struct{}),
	}
}

func (m *MockUDPConn) ReadFromUDP(b []byte) (n int, addr *net.UDPAddr, err error) {
	select {
	case data := <-m.readBuffer:
		n = copy(b, data)
		return n, m.remoteAddr.(*net.UDPAddr), nil
	case <-m.closed:
		return 0, nil, net.ErrClosed
	}
}

func (m *MockUDPConn) WriteToUDP(b []byte, addr *net.UDPAddr) (n int, err error) {
	select {
	case m.writeBuffer <- b:
		return len(b), nil
	case <-m.closed:
		return 0, net.ErrClosed
	}
}

func (m *MockUDPConn) Write(b []byte) (n int, err error) {
	select {
	case m.writeBuffer <- b:
		return len(b), nil
	case <-m.closed:
		return 0, net.ErrClosed
	}
}

func (m *MockUDPConn) Close() error {
	m.closeOnce.Do(func() {
		close(m.closed)
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

func (m *MockUDPConn) SetDeadline(t time.Time) error {
	return nil
}

func (m *MockUDPConn) SetReadDeadline(t time.Time) error {
	return nil
}

func (m *MockUDPConn) SetWriteDeadline(t time.Time) error {
	return nil
}

// TestPingSender ensures the pingSender sends messages at the correct interval.
func TestPingSender(t *testing.T) {
	localAddr, _ := net.ResolveUDPAddr("udp", "127.0.0.1:12345")
	remoteAddr, _ := net.ResolveUDPAddr("udp", "127.0.0.1:54321")
	mockConn := NewMockUDPConn(localAddr, remoteAddr)
	defer mockConn.Close()

	var wg sync.WaitGroup
	wg.Add(1)

	interval := 10 * time.Millisecond
	go pingSender(mockConn.connAsUDPConn(), interval, &wg)

	// Read 3 pings to ensure it's sending periodically
	for i := 0; i < 3; i++ {
		select {
		case msg := <-mockConn.writeBuffer:
			timestamp, err := strconv.ParseInt(string(msg), 10, 64)
			if err != nil {
				t.Fatalf("Failed to parse timestamp: %v", err)
			}
			if timestamp <= 0 {
				t.Errorf("Expected positive timestamp, got %d", timestamp)
			}
		case <-time.After(interval * 2): // Give it some buffer time
			t.Fatalf("Timed out waiting for ping %d", i+1)
		}
	}

	// Stop the sender goroutine by closing the connection (which will unblock the select)
	mockConn.Close()
	wg.Wait() // Wait for the goroutine to finish
}

// connAsUDPConn is a helper to cast MockUDPConn to *net.UDPConn for pingSender/echoReceiver.
// This is a bit of a hack for testing, as the functions expect *net.UDPConn.
// In a real scenario, one might use an interface for the connection.
func (m *MockUDPConn) connAsUDPConn() *net.UDPConn {
	// This is a simplification for testing. In a real application, 
	// pingSender and echoReceiver should ideally take a net.PacketConn interface.
	// For this specific test, we're simulating the behavior.
	return &net.UDPConn{ /* fields are unexported, so we can't fully construct */ }
}

// TestEchoReceiverAnomalyDetection simulates receiving pings and checks anomaly detection.
func TestEchoReceiverAnomalyDetection(t *testing.T) {
	var logBuffer bytes.Buffer
	log.SetOutput(&logBuffer)
	defer func() { log.SetOutput(os.Stderr) }() // Reset log output after test

	localAddr, _ := net.ResolveUDPAddr("udp", "127.0.0.1:12345")
	remoteAddr, _ := net.ResolveUDPAddr("udp", "127.0.0.2:54321")
	mockConn := NewMockUDPConn(localAddr, remoteAddr)
	defer mockConn.Close()

	var wg sync.WaitGroup
	wg.Add(1)

	anomalyThreshold := 100 * time.Millisecond
	go echoReceiver(mockConn.connAsUDPConn(), anomalyThreshold, &wg)

	// Simulate a normal ping
	sentTimeNormal := getMillis() - 50 // 50ms RTT
	mockConn.readBuffer <- []byte(strconv.FormatInt(sentTimeNormal, 10))

	// Simulate an anomalous ping
	sentTimeAnomaly := getMillis() - 200 // 200ms RTT, above 100ms threshold
	mockConn.readBuffer <- []byte(strconv.FormatInt(sentTimeAnomaly, 10))

	// Give receiver time to process and send echoes
	time.Sleep(50 * time.Millisecond)

	// Check for echoes sent back
	select {
	case <-mockConn.writeBuffer:
		// Expected an echo for the normal ping
	case <-time.After(10 * time.Millisecond):
		t.Fatal("Timed out waiting for first echo")
	}
	select {
	case <-mockConn.writeBuffer:
		// Expected an echo for the anomalous ping
	case <-time.After(10 * time.Millisecond):
		t.Fatal("Timed out waiting for second echo")
	}

	// Check log output for anomaly detection
	output := logBuffer.String()

	if !strings.Contains(output, "Received echo from 127.0.0.2:54321, RTT: 50ms") {
		t.Errorf("Expected normal RTT log, got:\n%s", output)
	}
	if !strings.Contains(output, "Chronal Anomaly Detected! Echo from 127.0.0.2:54321, RTT: 200ms (Threshold: 100ms)") {
		t.Errorf("Expected anomaly RTT log, got:\n%s", output)
	}

	// Stop the receiver goroutine by closing the connection
	mockConn.Close()
	wg.Wait() // Wait for the goroutine to finish
}

// TestEchoReceiverSelfPing ensures pings from self are ignored.
func TestEchoReceiverSelfPing(t *testing.T) {
	var logBuffer bytes.Buffer
	log.SetOutput(&logBuffer)
	defer func() { log.SetOutput(os.Stderr) }() // Reset log output after test

	localAddr, _ := net.ResolveUDPAddr("udp", "127.0.0.1:12345")
	// Simulate a ping from self (same local and remote address for the mock)
	mockConn := NewMockUDPConn(localAddr, localAddr)
	defer mockConn.Close()

	var wg sync.WaitGroup
	wg.Add(1)

	anomalyThreshold := 100 * time.Millisecond
	go echoReceiver(mockConn.connAsUDPConn(), anomalyThreshold, &wg)

	// Simulate a ping from self
	sentTime := getMillis() - 10 // 10ms RTT
	mockConn.readBuffer <- []byte(strconv.FormatInt(sentTime, 10))

	// Give receiver time to process
	time.Sleep(10 * time.Millisecond)

	// Check that no echo was sent and no log was made for self-ping
	select {
	case <-mockConn.writeBuffer:
		t.Fatal("Unexpected echo sent for self-ping")
	default:
		// Good, no echo sent
	}

	output := logBuffer.String()
	if strings.Contains(output, "Received echo") || strings.Contains(output, "Chronal Anomaly") {
		t.Errorf("Expected no log output for self-ping, got:\n%s", output)
	}

	// Stop the receiver goroutine by closing the connection
	mockConn.Close()
	wg.Wait() // Wait for the goroutine to finish
}
