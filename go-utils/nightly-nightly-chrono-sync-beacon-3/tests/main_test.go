package main

import (
	"fmt"
	"log"
	"net"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// MockPacketConn implements net.PacketConn for testing.
// # Mock rationale: The MockPacketConn simulates network I/O using in-memory channels,
// allowing deterministic and offline testing of server and client logic without
// actual network operations or external dependencies. This ensures tests are fast,
// reliable, and do not require network access.
type MockPacketConn struct {
	readCh   chan []byte
	writeCh  chan struct {
		data []byte
		addr net.Addr
	}
	closeCh  chan struct{}
	mu       sync.Mutex
	isClosed bool
}

func NewMockPacketConn() *MockPacketConn {
	return &MockPacketConn{
		readCh:  make(chan []byte, 10), // Buffered channel
		writeCh: make(chan struct { data []byte; addr net.Addr }, 10),
		closeCh: make(chan struct{}),
	}
}

func (m *MockPacketConn) ReadFrom(p []byte) (n int, addr net.Addr, err error) {
	select {
	case <-m.closeCh:
		return 0, nil, fmt.Errorf("connection closed")
	case data := <-m.readCh:
		n = copy(p, data)
		// Mock address, not critical for this test
		return n, &net.UDPAddr{IP: net.ParseIP("127.0.0.1"), Port: 12345}, nil
	case <-time.After(500 * time.Millisecond): // Timeout for tests
		return 0, nil, fmt.Errorf("read timeout")
	}
}

func (m *MockPacketConn) WriteTo(p []byte, addr net.Addr) (n int, err error) {
	select {
	case <-m.closeCh:
		return 0, fmt.Errorf("connection closed")
	case m.writeCh <- struct { data []byte; addr net.Addr }{data: p, addr: addr}:
		return len(p), nil
	case <-time.After(500 * time.Millisecond): // Timeout for tests
		return 0, fmt.Errorf("write timeout")
	}
}

func (m *MockPacketConn) Close() error {
	m.mu.Lock()
	defer m.mu.Unlock()
	if !m.isClosed {
		close(m.closeCh)
		m.isClosed = true
	}
	return nil
}

func (m *MockPacketConn) LocalAddr() net.Addr {
	return &net.UDPAddr{IP: net.ParseIP("127.0.0.1"), Port: 9000}
}

func (m *MockPacketConn) SetDeadline(t time.Time) error { return nil }
func (m *MockPacketConn) SetReadDeadline(t time.Time) error { return nil }
func (m *MockPacketConn) SetWriteDeadline(t time.Time) error { return nil }

func TestRunServer(t *testing.T) {
	mockConn := NewMockPacketConn()
	defer mockConn.Close()

	// Use a context to control the server's infinite loop for testing
	stopServer := make(chan struct{})
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		// runServer has an infinite loop, so we need to simulate its termination
		// For this test, we'll let it run for one cycle and then signal to stop.
		// In a real app, runServer would take a context.Context.
		// For this test, we'll just let it run until the test finishes or times out.
		runServer(mockConn)
	}()

	// Wait for a message to be written
	select {
	case written := <-mockConn.writeCh:
		message := string(written.data)
		// Check if the message contains one of the whimsical phrases
		foundPhrase := false
		for _, phrase := range whimsicalPhrases {
			if strings.HasPrefix(message, phrase) {
				foundPhrase = true
				break
			}
		}
		if !foundPhrase {
			t.Errorf("Server broadcasted an unexpected message format: %s", message)
		}
		// Check if it contains a valid RFC3339 timestamp
		parts := strings.Split(message, " ")
		foundTime := false
		for i := len(parts) - 1; i >= 0; i-- {
			if _, err := time.Parse(time.RFC3339, parts[i]); err == nil {
				foundTime = true
				break
			}
		}
		if !foundTime {
			t.Errorf("Server broadcasted message without a valid RFC3339 timestamp: %s", message)
		}
		if written.addr.String() != multicastAddr {
			t.Errorf("Server broadcasted to wrong address: got %s, want %s", written.addr.String(), multicastAddr)
		}
	case <-time.After(broadcastInterval + 500*time.Millisecond): // Give it a bit more time than interval
		t.Fatal("Server did not broadcast message within expected time")
	}

	// Signal to stop the server goroutine (by closing the mock connection, which will cause ReadFrom/WriteTo to error)
	close(stopServer)
	// We don't wait for wg.Wait() here because runServer is an infinite loop and won't naturally exit.
	// The test's purpose is to verify it *sends* a message.
}

func TestRunClient(t *testing.T) {
	mockConn := NewMockPacketConn()
	defer mockConn.Close()

	// Capture log output to verify client's print statements
	var logOutput strings.Builder
	log.SetOutput(&logOutput)
	defer log.SetOutput(os.Stderr) // Reset log output after test

	// Simulate a message being received by the client
	testTime := time.Now().UTC()
	testMessage := fmt.Sprintf("The void whispers the precise moment: %s", testTime.Format(time.RFC3339))
	
	// Run client in a goroutine
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		runClient(mockConn)
	}()

	// Send the message to the mock connection's read channel
	mockConn.readCh <- []byte(testMessage)

	// Wait for the client to process the message and print
	time.Sleep(100 * time.Millisecond) // Give client goroutine time to process

	// Verify log output
	output := logOutput.String()
	
	if !strings.Contains(output, "Received: \""+testMessage+"\"") {
		t.Errorf("Client did not log the received message correctly. Output:\n%s", output)
	}
	expectedSyncTimeLog := fmt.Sprintf("Synchronized Time: %s (UTC)", testTime.Format(time.RFC3339))
	if !strings.Contains(output, expectedSyncTimeLog) {
		t.Errorf("Client did not log the synchronized time correctly. Expected to find '%s'. Output:\n%s", expectedSyncTimeLog, output)
	}

	// To stop the client goroutine, we'd typically use a context.Context.
	// For this test, we've verified its behavior for one message.
	// Closing the mockConn will eventually cause ReadFrom to return an error,
	// but the loop in runClient will just log it and continue.
}

func TestGetRandomWhimsicalMessage(t *testing.T) {
	testTime := time.Date(2023, time.October, 27, 10, 30, 0, 0, time.UTC)
	message := getRandomWhimsicalMessage(testTime)

	if !strings.Contains(message, testTime.Format(time.RFC3339)) {
		t.Errorf("Message '%s' does not contain the correct timestamp '%s'", message, testTime.Format(time.RFC3339))
	}

	foundPhrase := false
	for _, phrase := range whimsicalPhrases {
		if strings.HasPrefix(message, phrase) {
			foundPhrase = true
			break
		}
	}
	if !foundPhrase {
		t.Errorf("Message '%s' does not start with a known whimsical phrase", message)
	}
}
