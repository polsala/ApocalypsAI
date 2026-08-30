package main

import (
	"bufio"
	"bytes"
	"fmt"
	"log"
	"net"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock rationale: This test starts a real TCP server (the chrono-sync-beacon)
// in a separate goroutine on a dynamically assigned local port. It then acts
// as a client, connecting to this local server to verify its functionality.
// This approach is deterministic and offline as it does not rely on any
// external network resources or services, performing all network communication
// within the test's local loopback interface.
// The server's logging is redirected to a buffer to prevent test output clutter
// and allow inspection if needed, ensuring test isolation.

func TestChronoSyncBeacon(t *testing.T) {
	// Create a buffer to capture server logs during the test
	var serverLogBuffer bytes.Buffer
	testLogger := log.New(&serverLogBuffer, "[TEST_SERVER] ", log.Ldate|log.Ltime|log.Lshortfile)

	// Find an available port for the test server
	listener, err := net.Listen("tcp", "127.0.0.1:0") // Listen on a random available port
	if err != nil {
		t.Fatalf("Failed to find an available port: %v", err)
	}
	testPort := listener.Addr().(*net.TCPAddr).Port
	serverAddr := fmt.Sprintf("127.0.0.1:%d", testPort)

	var wg sync.WaitGroup
	wg.Add(1) // For the server goroutine

	// Start the server in a goroutine
	go func() {
		defer wg.Done()
		// The runServer function now takes a listener and logger, making it testable.
		// The listener is passed directly, and will be closed by the test.
		if err := runServer(listener, testLogger); err != nil {
			testLogger.Printf("Server goroutine exited with error: %v", err)
		}
	}()

	// Give the server a moment to start accepting connections
	// A short sleep is used here. For more critical applications, a channel-based
	// readiness signal would be more robust, but for a simple TCP listener,
	// `net.Dial`'s internal retries often make this sufficient.
	time.Sleep(50 * time.Millisecond)

	// Connect to the server
	conn, err := net.Dial("tcp", serverAddr)
	if err != nil {
		t.Fatalf("Failed to connect to server at %s: %v. Server logs:\n%s", serverAddr, err, serverLogBuffer.String())
	}
	defer conn.Close()

	// Send "TIME" command
	_, err = conn.Write([]byte("TIME\n"))
	if err != nil {
		t.Fatalf("Failed to send command: %v", err)
	}

	// Read response
	reader := bufio.NewReader(conn)
	conn.SetReadDeadline(time.Now().Add(1 * time.Second)) // Set a read deadline for client
	response, err := reader.ReadString('\n')
	if err != nil {
		t.Fatalf("Failed to read response: %v. Server logs:\n%s", err, serverLogBuffer.String())
	}

	trimmedResponse := strings.TrimSpace(response)
	parsedTime, err := time.Parse(time.RFC3339, trimmedResponse)
	if err != nil {
		t.Errorf("Response '%s' is not a valid RFC3339 timestamp: %v. Server logs:\n%s", trimmedResponse, err, serverLogBuffer.String())
	}

	// Verify the time is recent (within a few seconds of test execution)
	now := time.Now().UTC()
	// Allow a small window for execution time differences
	if parsedTime.Before(now.Add(-5*time.Second)) || parsedTime.After(now.Add(5*time.Second)) {
		t.Errorf("Returned time %s is not close to current UTC time %s. Server logs:\n%s", parsedTime.String(), now.String(), serverLogBuffer.String())
	}

	// Test unknown command
	_, err = conn.Write([]byte("UNKNOWN_CMD\n"))
	if err != nil {
		t.Fatalf("Failed to send unknown command: %v", err)
	}

	conn.SetReadDeadline(time.Now().Add(1 * time.Second)) // Set a read deadline for client
	errorResponse, err := reader.ReadString('\n')
	if err != nil {
		t.Fatalf("Failed to read error response: %v. Server logs:\n%s", err, serverLogBuffer.String())
	}
	expectedError := "ERROR: Unknown command. Send 'TIME'"
	if strings.TrimSpace(errorResponse) != expectedError {
		t.Errorf("Expected error response '%s', got '%s'. Server logs:\n%s", expectedError, strings.TrimSpace(errorResponse), serverLogBuffer.String())
	}

	// Close the listener to signal the server goroutine to shut down
	listener.Close()
	wg.Wait() // Wait for the server goroutine to finish

	// Optionally print server logs if test failed for debugging
	if t.Failed() {
		fmt.Printf("Server logs during test:\n%s", serverLogBuffer.String())
	}
}
