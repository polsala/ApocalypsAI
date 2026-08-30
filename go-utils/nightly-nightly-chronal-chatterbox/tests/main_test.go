package main

import (
	"bufio"
	"fmt"
	"net"
	"strings"
	"testing"
	"time"
)

// TestHandleConnection verifies that the handleConnection function correctly
// reads a message, delays, and echoes it back with the expected prefix.
func TestHandleConnection(t *testing.T) {
	// Mock rationale: Using net.Pipe() to create an in-memory, bidirectional connection
	// allows testing network communication logic deterministically and offline,
	// without binding to actual network ports or relying on external network conditions.
	clientConn, serverConn := net.Pipe()
	defer clientConn.Close()
	defer serverConn.Close()

	testMessage := "Hello Chronos!\n"
	expectedPrefix := "[Echoed from Chronal Chatterbox after"

	// Start handleConnection in a goroutine to simulate server processing
	go handleConnection(serverConn)

	// Client sends a message
	_, err := clientConn.Write([]byte(testMessage))
	if err != nil {
		t.Fatalf("Client write error: %v", err)
	}

	reader := bufio.NewReader(clientConn)

	// Set a read deadline for the client to prevent the test from hanging
	// The max delay is 6 seconds, so set a deadline slightly longer.
	clientConn.SetReadDeadline(time.Now().Add(time.Duration(maxDelayMs+1000) * time.Millisecond))

	// Client reads the echoed response
	response, err := reader.ReadString('\n')
	if err != nil {
		t.Fatalf("Client read error: %v", err)
	}

	// Assertions on the received response
	if !strings.HasPrefix(response, expectedPrefix) {
		t.Errorf("Expected response to start with '%s', got '%s'", expectedPrefix, response)
	}

	// Check if the original message (trimmed) is contained in the response
	if !strings.Contains(response, strings.TrimSpace(testMessage)) {
		t.Errorf("Expected response to contain original message '%s', got '%s'", strings.TrimSpace(testMessage), response)
	}

	// Optional: Parse the delay from the response and check its range
	delayStr := response[len(expectedPrefix) : strings.Index(response, "]:")]
	duration, err := time.ParseDuration(strings.TrimSpace(delayStr))
	if err != nil {
		t.Errorf("Could not parse delay duration from response: %v, raw: '%s'", err, delayStr)
	} else {
		if duration < time.Duration(minDelayMs)*time.Millisecond || duration > time.Duration(maxDelayMs)*time.Millisecond {
			t.Errorf("Delay duration %v is out of expected range [%v, %v]", duration, time.Duration(minDelayMs)*time.Millisecond, time.Duration(maxDelayMs)*time.Millisecond)
		}
	}
}

// TestMultipleConnections verifies that the server can handle multiple concurrent connections.
func TestMultipleConnections(t *testing.T) {
	// Mock rationale: Similar to TestHandleConnection, net.Pipe() allows simulating
	// multiple concurrent client-server interactions in a controlled, offline environment.
	listener, err := net.Listen("tcp", ":0") // Listen on a random available port
	if err != nil {
		t.Fatalf("Failed to listen: %v", err)
	}
	defer listener.Close()

	// Start the main server loop in a goroutine
	go func() {
		for {
			conn, err := listener.Accept()
			if err != nil {
				// Expected error when listener is closed
				if !strings.Contains(err.Error(), "use of closed network connection") {
					t.Logf("Accept error: %v", err)
				}
				return
			}
			go handleConnection(conn)
		}
	}()

	serverAddr := listener.Addr().String()
	numClients := 3
	messages := make(chan string, numClients)

	for i := 0; i < numClients; i++ {
		go func(clientId int) {
			conn, err := net.Dial("tcp", serverAddr)
			if err != nil {
				messages <- fmt.Sprintf("Client %d dial error: %v", clientId, err)
				return
			}
			defer conn.Close()

			msg := fmt.Sprintf("Client %d message\n", clientId)
			_, err = conn.Write([]byte(msg))
			if err != nil {
				messages <- fmt.Sprintf("Client %d write error: %v", clientId, err)
				return
			}

			reader := bufio.NewReader(conn)
			conn.SetReadDeadline(time.Now().Add(time.Duration(maxDelayMs+1000) * time.Millisecond))
			response, err := reader.ReadString('\n')
			if err != nil {
				messages <- fmt.Sprintf("Client %d read error: %v", clientId, err)
				return
			}

			if !strings.HasPrefix(response, "[Echoed from Chronal Chatterbox after") || !strings.Contains(response, strings.TrimSpace(msg)) {
				messages <- fmt.Sprintf("Client %d unexpected response: %s", clientId, response)
				return
			}
			messages <- fmt.Sprintf("Client %d received OK", clientId)
		}(i)
	}

	for i := 0; i < numClients; i++ {
		select {
		case msg := <-messages:
			if !strings.HasSuffix(msg, "received OK") {
				t.Error(msg)
			}
		case <-time.After(time.Duration(maxDelayMs+2000) * time.Millisecond): // Longer timeout for multiple clients
			t.Fatalf("Timeout waiting for client %d response", i)
		}
	}
}
