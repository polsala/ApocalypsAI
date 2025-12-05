package main

import (
	"bufio"
	"bytes"
	"fmt"
	"io"
	"log"
	"net"
	"sync"
	"testing"
	"time"
)

// Mock rationale: We use a custom mockNetConn to simulate a network connection.
// This allows us to control the input (Read) and output (Write) of the connection
// and define a deterministic RemoteAddr, ensuring the test is offline and repeatable.
// The logger output is captured using bytes.Buffer.

// mockNetConn implements net.Conn for testing purposes.
type mockNetConn struct {
	io.Reader
	io.Writer
	closeOnce  sync.Once
	closedChan chan struct{}
	remoteAddr net.Addr
}

func newMockNetConn(readBuf *bytes.Buffer, writeBuf *bytes.Buffer, remoteAddr net.Addr) *mockNetConn {
	return &mockNetConn{
		Reader:     readBuf,
		Writer:     writeBuf,
		closedChan: make(chan struct{}),
		remoteAddr: remoteAddr,
	}
}

func (m *mockNetConn) Close() error {
	m.closeOnce.Do(func() {
		close(m.closedChan)
	}) // Signal that the connection is closed
	return nil
}

func (m *mockNetConn) LocalAddr() net.Addr                { return nil } // Not used by handleConnection
func (m *mockNetConn) RemoteAddr() net.Addr               { return m.remoteAddr }
func (m *mockNetConn) SetDeadline(t time.Time) error      { return nil } // Not used by handleConnection
func (m *mockNetConn) SetReadDeadline(t time.Time) error  { return nil } // Not used by handleConnection
func (m *mockNetConn) SetWriteDeadline(t time.Time) error { return nil } // Not used by handleConnection

func TestHandleConnection(t *testing.T) {
	// Input buffer for the mock connection (what the client sends)
	inputBuffer := bytes.NewBufferString("alpha particle\nbeta particle\ngamma ray\n")
	// Output buffer for the mock connection (handleConnection doesn't write back, but required by interface)
	outputBuffer := bytes.NewBuffer(nil)

	// Buffer to capture logger output
	var logBuffer bytes.Buffer
	logger := log.New(&logBuffer, "", 0) // No prefix, no flags for easier assertion

	// Define a mock remote address
	mockRemoteAddr := &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 12345}

	// Create the mock connection
	mockConn := newMockNetConn(inputBuffer, outputBuffer, mockRemoteAddr)

	// Start handleConnection in a goroutine
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		handleConnection(mockConn, logger)
		wg.Done()
	}()

	// Wait for handleConnection to finish (it will finish when inputBuffer is exhausted and scanner.Scan() returns false)
	wg.Wait()

	// Verify the captured log output
	output := logBuffer.String()
	expectedPrefix := "[Stardust Particle]"
	expectedFromAddr := mockRemoteAddr.String()

	// Check for connection start/end messages
	if !bytes.Contains(logBuffer.Bytes(), []byte(fmt.Sprintf("New stardust stream from %s", expectedFromAddr))) {
		t.Errorf("Expected 'New stardust stream' message, got:\n%s", output)
	}
	if !bytes.Contains(logBuffer.Bytes(), []byte(fmt.Sprintf("Stardust stream from %s closed.", expectedFromAddr))) {
		t.Errorf("Expected 'Stardust stream closed' message, got:\n%s", output)
	}

	// Check for processed particles
	particles := []string{"alpha particle", "beta particle", "gamma ray"}
	for _, p := range particles {
		expectedParticleLogPart := fmt.Sprintf("%s %s (received from %s at", expectedPrefix, p, expectedFromAddr)
		if !bytes.Contains(logBuffer.Bytes(), []byte(expectedParticleLogPart)) {
			t.Errorf("Expected processed particle '%s' in logs, got:\n%s", p, output)
		}
	}

	// Ensure the timestamp format is present but don't assert exact time
	// Example: "[Stardust Particle] alpha particle (received from 127.0.0.1:12345 at 2023-10-27T10:00:00Z)"
	for _, line := range bytes.Split(logBuffer.Bytes(), []byte("\n")) {
		if bytes.Contains(line, []byte(expectedPrefix)) && bytes.Contains(line, []byte(expectedFromAddr)) {
			parts := bytes.Split(line, []byte(" at "))
			if len(parts) < 2 {
				t.Errorf("Processed line missing ' at ' separator: %s", string(line))
				continue
			}
			timestampStr := bytes.TrimSuffix(parts[1], []byte(")"))
			_, err := time.Parse(time.RFC3339, string(timestampStr))
			if err != nil {
				t.Errorf("Failed to parse timestamp '%s' in line: %s, error: %v", string(timestampStr), string(line), err)
			}
		}
	}
}
