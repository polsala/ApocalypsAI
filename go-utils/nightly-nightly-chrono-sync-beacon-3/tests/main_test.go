package main

import (
	"bytes"
	"errors"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock UDP implementation for tests
type mockUDPConn struct {
	readBuffer  chan []byte
	writeBuffer chan []byte
	closeChan   chan struct{}
	readErr     error
	writeErr    error
	mu          sync.Mutex // Protects read/write errors
}

func newMockUDPConn() *mockUDPConn {
	return &mockUDPConn{
		readBuffer:  make(chan []byte, 10),
		writeBuffer: make(chan []byte, 10),
		closeChan:   make(chan struct{}),
	}
}

func (m *mockUDPConn) WriteToUDP(b []byte, addr *net.UDPAddr) (int, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	if m.writeErr != nil {
		return 0, m.writeErr
	}
	select {
	case m.writeBuffer <- b:
		return len(b), nil
	case <-m.closeChan:
		return 0, errors.New("connection closed")
	case <-time.After(100 * time.Millisecond): // Prevent test hang
		return 0, errors.New("mock write timeout")
	}
}

func (m *mockUDPConn) ReadFromUDP(b []byte) (int, *net.UDPAddr, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	if m.readErr != nil {
		return 0, m.readErr
	}
	select {
	case data := <-m.readBuffer:
		n := copy(b, data)
		return n, &net.UDPAddr{IP: net.ParseIP("127.0.0.1"), Port: 12345}, nil // Mock sender address
	case <-m.closeChan:
		return 0, errors.New("connection closed")
	case <-time.After(100 * time.Millisecond): // Prevent test hang
		return 0, errors.New("mock read timeout")
	}
}

func (m *mockUDPConn) Close() error {
	select {
	case <-m.closeChan:
		// Already closed
	default:
		close(m.closeChan)
	}
	return nil
}

// SimulateReceive pushes data into the mock's read buffer.
func (m *mockUDPConn) SimulateReceive(data []byte) {
	m.readBuffer <- data
}

// GetSentData retrieves data from the mock's write buffer.
func (m *mockUDPConn) GetSentData() []byte {
	select {
	case data := <-m.writeBuffer:
		return data
	default:
		return nil
	}
}

// SetReadError sets an error to be returned by ReadFromUDP.
func (m *mockUDPConn) SetReadError(err error) {
	m.mu.Lock()
	m.readErr = err
	m.mu.Unlock()
}

// SetWriteError sets an error to be returned by WriteToUDP.
func (m *mockUDPConn) SetWriteError(err error) {
	m.mu.Lock()
	m.writeErr = err
	m.mu.Unlock()
}

func TestFormatAndParseBeaconMessage(t *testing.T) {
	// Mock rationale: Testing the serialization/deserialization logic of beacon messages offline.
	msg := beaconMessage{
		SenderID:  "TestNode",
		Timestamp: 1678886400000000000, // March 15, 2023 12:00:00 PM UTC in nanoseconds
	}

	formatted := formatBeaconMessage(msg)
	expected := "TestNode:1678886400000000000"
	if formatted != expected {
		t.Errorf("Expected formatted message %q, got %q", expected, formatted)
	}

	parsed, err := parseBeaconMessage(formatted)
	if err != nil {
		t.Fatalf("Failed to parse beacon message: %v", err)
	}

	if parsed.SenderID != msg.SenderID || parsed.Timestamp != msg.Timestamp {
		t.Errorf("Parsed message mismatch. Expected %+v, got %+v", msg, parsed)
	}

	// Test invalid format
	_, err = parseBeaconMessage("invalid-format")
	if err == nil {
		t.Error("Expected error for invalid format, got nil")
	}

	// Test invalid timestamp
	_, err = parseBeaconMessage("TestNode:not-a-number")
	if err == nil {
		t.Error("Expected error for invalid timestamp, got nil")
	}
}

func TestCalculateDrift(t *testing.T) {
	// Mock rationale: Testing the core drift calculation logic offline with fixed timestamps.
	// Receiver's local time
	receiveTime := time.Date(2023, time.October, 27, 10, 0, 0, 0, time.UTC)

	// Sender's time is 100ms ahead
	senderTimeAhead := receiveTime.Add(100 * time.Millisecond)
	drift := calculateDrift(senderTimeAhead.UnixNano(), receiveTime)
	if drift != 100*time.Millisecond {
		t.Errorf("Expected +100ms drift, got %s", drift)
	}

	// Sender's time is 50ms behind
	senderTimeBehind := receiveTime.Add(-50 * time.Millisecond)
	drift = calculateDrift(senderTimeBehind.UnixNano(), receiveTime)
	if drift != -50*time.Millisecond {
		t.Errorf("Expected -50ms drift, got %s", drift)
	}

	// Sender's time is perfectly synced
	senderTimeSync := receiveTime
	drift = calculateDrift(senderTimeSync.UnixNano(), receiveTime)
	if drift != 0 {
		t.Errorf("Expected 0 drift, got %s", drift)
	}
}

func TestRunEmitter(t *testing.T) {
	// Mock rationale: Using a mock UDP connection to verify that the emitter sends correctly formatted beacons
	// without actual network I/O. We check the content of the 'sent' buffer.
	mockConn := newMockUDPConn()
	defer mockConn.Close()

	id := "EmitterTest"
	port := 12345
	interval := 10 * time.Millisecond
	address := "127.0.0.1"

	done := make(chan struct{})
	go func() {
		runEmitter(id, port, interval, address, mockConn)
		close(done)
	}()

	time.Sleep(20 * time.Millisecond) // Allow emitter to send at least one beacon

	sentData := mockConn.GetSentData()
	if sentData == nil {
		t.Fatal("No data sent by emitter")
	}

	beaconStr := string(sentData)
	parts := strings.SplitN(beaconStr, ":", 2)
	if len(parts) != 2 {
		t.Fatalf("Sent data has invalid format: %q", beaconStr)
	}

	if parts[0] != id {
		t.Errorf("Expected sender ID %q, got %q", id, parts[0])
	}

	timestamp, err := strconv.ParseInt(parts[1], 10, 64)
	if err != nil {
		t.Fatalf("Failed to parse timestamp from sent data: %v", err)
	}
	if timestamp <= 0 {
		t.Errorf("Expected valid timestamp, got %d", timestamp)
	}

	// Test error handling for write
	mockConn.SetWriteError(errors.New("mock write error"))
	// Give it time to try sending again
	time.Sleep(interval + 5*time.Millisecond)
	// We can't easily assert a log message, but we ensure it doesn't crash.
}

func TestRunListener(t *testing.T) {
	// Mock rationale: Using a mock UDP connection to simulate receiving beacons and verifying
	// that the listener processes them correctly and logs the expected drift, all offline.
	mockConn := newMockUDPConn()
	defer mockConn.Close()

	port := 12345
	address := "0.0.0.0"

	// Capture log output
	oldLogOutput := log.Writer()
	var logBuffer bytes.Buffer
	log.SetOutput(&logBuffer)
	defer log.SetOutput(oldLogOutput)

	done := make(chan struct{})
	go func() {
		runListener(port, address, mockConn)
		close(done)
	}()

	// Simulate receiving a beacon with a known drift
	senderID := "ListenerTestNode"
	receiveTime := time.Now()
	senderTime := receiveTime.Add(50 * time.Millisecond) // Sender is 50ms ahead
	beaconData := formatBeaconMessage(beaconMessage{SenderID: senderID, Timestamp: senderTime.UnixNano()})
	mockConn.SimulateReceive([]byte(beaconData))

	time.Sleep(20 * time.Millisecond) // Allow listener to process

	logOutput := logBuffer.String()
	if !strings.Contains(logOutput, fmt.Sprintf("Received beacon from %s (127.0.0.1:12345). Drift: +50.000ms", senderID)) {
		t.Errorf("Expected log output containing drift, got:\n%s", logOutput)
	}

	// Simulate receiving an invalid beacon
	logBuffer.Reset()
	mockConn.SimulateReceive([]byte("invalid-beacon-data"))
	time.Sleep(20 * time.Millisecond)
	logOutput = logBuffer.String()
	if !strings.Contains(logOutput, "Error parsing beacon") {
		t.Errorf("Expected log output for parsing error, got:\n%s", logOutput)
	}

	// Simulate read error
	logBuffer.Reset()
	mockConn.SetReadError(errors.New("mock read error"))
	mockConn.SimulateReceive([]byte("any-data")) // Trigger a read attempt
	time.Sleep(20 * time.Millisecond)
	logOutput = logBuffer.String()
	if !strings.Contains(logOutput, "Error reading from UDP: mock read error") {
		t.Errorf("Expected log output for read error, got:\n%s", logOutput)
	}
}

func TestMainFunction(t *testing.T) {
	// Mock rationale: Testing the main function's argument parsing and command dispatching.
	// We use os.Exit and log.Fatal, so we capture output and check for expected errors/messages.

	// Capture os.Exit calls
	oldOsExit := osExit
	defer func() { osExit = oldOsExit }()
	exitCalled := make(chan int, 1)
	osExit = func(code int) {
		exitCalled <- code
		panic("os.Exit called") // Panic to stop execution in test
	}

	// Capture log.Fatal calls
	oldLogFatal := logFatal
	defer func() { logFatal = oldLogFatal }()
	logFatalCalled := make(chan string, 1)
	logFatal = func(v ...interface{}) {
		logFatalCalled <- fmt.Sprint(v...)
		panic("log.Fatal called") // Panic to stop execution in test
	}

	// Capture stdout
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	outC := make(chan string)
	go func() {
		var buf bytes.Buffer
		io.Copy(&buf, r)
		outC <- buf.String()
	}()
	defer func() {
		os.Stdout = oldStdout
		w.Close()
		<-outC // Ensure pipe is drained
	}()

	// Test no command
	os.Args = []string{"nightly-chrono-sync-beacon"}
	func() {
		defer func() { recover() }() // Catch panic from os.Exit
		main()
	}()
	select {
	case code := <-exitCalled:
		if code != 1 {
			t.Errorf("Expected exit code 1, got %d", code)
		}
	case <-time.After(100 * time.Millisecond):
		t.Fatal("main did not exit for no command")
	}

	// Test unknown command
	os.Args = []string{"nightly-chrono-sync-beacon", "unknown"}
	func() {
		defer func() { recover() }() // Catch panic from os.Exit
		main()
	}()
	select {
	case code := <-exitCalled:
		if code != 1 {
			t.Errorf("Expected exit code 1, got %d", code)
		}
	case <-time.After(100 * time.Millisecond):
		t.Fatal("main did not exit for unknown command")
	}

	// Test emit command with missing ID
	os.Args = []string{"nightly-chrono-sync-beacon", "emit"}
	func() {
		defer func() { recover() }() // Catch panic from log.Fatal
		main()
	}()
	select {
	case msg := <-logFatalCalled:
		if !strings.Contains(msg, "Emitter ID is required") {
			t.Errorf("Expected log.Fatal for missing ID, got %q", msg)
		}
	case <-time.After(100 * time.Millisecond):
		t.Fatal("main did not call log.Fatal for missing ID")
	}

	// Note: Testing successful `emit` or `listen` execution in `main` would require
	// mocking `net.DialUDP` and `net.ListenUDP` which is more complex and better handled
	// by testing `runEmitter` and `runListener` directly with the `UDPConn` interface.
	// The current tests cover argument parsing and error paths for `main`.
}

// Overrides for os.Exit and log.Fatal to allow testing their calls
var osExit = os.Exit
var logFatal = log.Fatal
