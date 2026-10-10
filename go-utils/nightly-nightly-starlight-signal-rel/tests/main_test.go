package main

import (
	"bytes"
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

// MockConn implements net.Conn for testing purposes.
// # Mock rationale: This allows simulating network connections without actual network I/O,
// # making tests deterministic and offline. It provides control over what is read and written.
type MockConn struct {
	bytes.Buffer
	readBuffer  bytes.Buffer
	closeCalled bool
	mu          sync.Mutex
}

func (m *MockConn) Read(b []byte) (n int, err error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	return m.readBuffer.Read(b)
}

func (m *MockConn) Write(b []byte) (n int, err error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	return m.Buffer.Write(b)
}

func (m *MockConn) Close() error {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.closeCalled = true
	return nil
}

func (m *MockConn) LocalAddr() net.Addr {
	return &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 8080}
}

func (m *MockConn) RemoteAddr() net.Addr {
	return &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 12345}
}

func (m *MockConn) SetDeadline(t time.Time) error {
	return nil
}

func (m *MockConn) SetReadDeadline(t time.Time) error {
	return nil
}

func (m *MockConn) SetWriteDeadline(t time.Time) error {
	return nil
}

// TestHandleConnection_Success tests that a message is processed after a simulated delay.
func TestHandleConnection_Success(t *testing.T) {
	// # Mock rationale: Overriding sleepFunc to capture the delay duration and prevent actual time.Sleep.
	// # This makes the test deterministic and fast.
	var actualDelay time.Duration
	var sleepCalled bool
	var wg sync.WaitGroup
	wg.Add(1) // Expect one call to sleepFunc
	sleepFunc = func(d time.Duration) {
		sleepCalled = true
		actualDelay = d
		wg.Done() // Signal that sleep was called
	}
	defer func() { sleepFunc = time.Sleep }() // Reset global variable after test

	// # Mock rationale: Overriding nowFunc to provide a fixed, deterministic time for timestamps.
	// # This ensures consistent output regardless of when the test is run.
	fixedTime := time.Date(2023, time.October, 27, 10, 0, 0, 0, time.UTC)
	nowFunc = func() time.Time { return fixedTime }
	defer func() { nowFunc = time.Now }() // Reset global variable after test

	// Capture log output to verify messages.
	// # Mock rationale: Redirecting log.Printf output to a buffer to assert its content.
	// # This avoids polluting test console and allows programmatic verification.
	var logBuffer bytes.Buffer
	log.SetOutput(&logBuffer)
	defer func() { log.SetOutput(os.Stderr) }() // Restore default log output

	// Capture fmt.Printf output (for logMessage) to verify messages.
	// # Mock rationale: Redirecting fmt.Printf output to a buffer to assert its content.
	// # This allows programmatic verification of the final relayed message.
	var printBuffer bytes.Buffer
	originalStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	defer func() {
		os.Stdout = originalStdout
		w.Close()
	}()

	mockConn := &MockConn{}
	inputMessage := "Hello, Starlight!\n"
	mockConn.readBuffer.WriteString(inputMessage)

	configuredDelay := 3 * time.Second

	handleConnection(mockConn, configuredDelay)

	wg.Wait() // Wait for the internal goroutine to finish its 'sleep'

	// Read from the pipe to get the fmt.Printf output
	w.Close()
	io.Copy(&printBuffer, r)

	// Assertions
	if !sleepCalled {
		t.Errorf("Expected sleepFunc to be called, but it wasn't.")
	}
	if actualDelay != configuredDelay {
		t.Errorf("Expected sleepFunc to be called with delay %v, got %v", configuredDelay, actualDelay)
	}

	if !mockConn.closeCalled {
		t.Errorf("Expected connection to be closed, but it wasn't.")
	}

	expectedLogOutput := fmt.Sprintf("📥 Message received from 127.0.0.1:12345 at %s: 'Hello, Starlight!'", fixedTime.Format(time.RFC3339))
	if !strings.Contains(logBuffer.String(), expectedLogOutput) {
		t.Errorf("Log output missing expected message.\nExpected substring: %s\nActual log: %s", expectedLogOutput, logBuffer.String())
	}

	expectedPrintOutput := fmt.Sprintf("[%s] Starlight Relay: Message received at %s, traversing cosmic dust for %s... Relayed at %s: 'Hello, Starlight!'",
		fixedTime.Format("2006-01-02 15:04:05"),
		fixedTime.Format("2006-01-02 15:04:05"),
		configuredDelay,
		fixedTime.Format("2006-01-02 15:04:05"),
		strings.TrimRight(inputMessage, "\n"),
	)
	if !strings.Contains(printBuffer.String(), expectedPrintOutput) {
		t.Errorf("Print output missing expected message.\nExpected substring: %s\nActual print: %s", expectedPrintOutput, printBuffer.String())
	}
}

// TestHandleConnection_ReadError tests error handling during message reading.
func TestHandleConnection_ReadError(t *testing.T) {
	// # Mock rationale: Overriding sleepFunc to prevent actual time.Sleep.
	sleepFunc = func(d time.Duration) {}
	defer func() { sleepFunc = time.Sleep }()

	// # Mock rationale: Overriding nowFunc to provide a fixed, deterministic time.
	nowFunc = func() time.Time { return time.Date(2023, time.October, 27, 10, 0, 0, 0, time.UTC) }
	defer func() { nowFunc = time.Now }()

	// Capture log output to verify error messages.
	// # Mock rationale: Redirecting log.Printf output to a buffer to assert its content.
	var logBuffer bytes.Buffer
	log.SetOutput(&logBuffer)
	defer func() { log.SetOutput(os.Stderr) }()

	mockConn := &MockConn{}
	// Simulate an error by making the read buffer return an error immediately after partial read
	mockConn.readBuffer.WriteString("partial message") // Not ending with newline

	configuredDelay := 1 * time.Second

	handleConnection(mockConn, configuredDelay)

	// Give a moment for the goroutine to potentially start and finish if it doesn't sleep
	time.Sleep(10 * time.Millisecond) // Small wait to allow handleConnection's goroutine to run if it doesn't sleep

	if !mockConn.closeCalled {
		t.Errorf("Expected connection to be closed, but it wasn't.")
	}

	expectedErrorLog := "❌ Error reading signal from 127.0.0.1:12345: EOF"
	if !strings.Contains(logBuffer.String(), expectedErrorLog) {
		t.Errorf("Log output missing expected error message.\nExpected substring: %s\nActual log: %s", expectedErrorLog, logBuffer.String())
	}

	// Ensure no message was 'relayed' if there was a read error
	var printBuffer bytes.Buffer
	originalStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	defer func() {
		os.Stdout = originalStdout
		w.Close()
	}()
	w.Close()
	io.Copy(&printBuffer, r)
	if strings.Contains(printBuffer.String(), "Starlight Relay") {
		t.Errorf("Unexpected 'Starlight Relay' message in stdout after read error: %s", printBuffer.String())
	}
}

// TestHandleConnection_EmptyMessage tests handling of an empty message (just a newline).
func TestHandleConnection_EmptyMessage(t *testing.T) {
	// # Mock rationale: Overriding sleepFunc to capture the delay duration and prevent actual time.Sleep.
	var actualDelay time.Duration
	var wg sync.WaitGroup
	wg.Add(1)
	sleepFunc = func(d time.Duration) {
		actualDelay = d
		wg.Done()
	}
	defer func() { sleepFunc = time.Sleep }()

	// # Mock rationale: Overriding nowFunc to provide a fixed, deterministic time.
	fixedTime := time.Date(2023, time.October, 27, 10, 0, 0, 0, time.UTC)
	nowFunc = func() time.Time { return fixedTime }
	defer func() { nowFunc = time.Now }()

	// Capture log output.
	// # Mock rationale: Redirecting log.Printf output to a buffer.
	var logBuffer bytes.Buffer
	log.SetOutput(&logBuffer)
	defer func() { log.SetOutput(os.Stderr) }()

	// Capture fmt.Printf output.
	// # Mock rationale: Redirecting fmt.Printf output to a buffer.
	var printBuffer bytes.Buffer
	originalStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	defer func() {
		os.Stdout = originalStdout
		w.Close()
	}()

	mockConn := &MockConn{}
	inputMessage := "\n" // Just a newline
	mockConn.readBuffer.WriteString(inputMessage)

	configuredDelay := 2 * time.Second

	handleConnection(mockConn, configuredDelay)
	wg.Wait()

	w.Close()
	io.Copy(&printBuffer, r)

	if actualDelay != configuredDelay {
		t.Errorf("Expected sleepFunc to be called with delay %v, got %v", configuredDelay, actualDelay)
	}

	expectedPrintOutput := fmt.Sprintf("[%s] Starlight Relay: Message received at %s, traversing cosmic dust for %s... Relayed at %s: ''",
		fixedTime.Format("2006-01-02 15:04:05"),
		fixedTime.Format("2006-01-02 15:04:05"),
		configuredDelay,
		fixedTime.Format("2006-01-02 15:04:05"),
	)
	if !strings.Contains(printBuffer.String(), expectedPrintOutput) {
		t.Errorf("Print output missing expected empty message.\nExpected substring: %s\nActual print: %s", expectedPrintOutput, printBuffer.String())
	}
}
