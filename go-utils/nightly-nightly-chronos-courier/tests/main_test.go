package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"net"
	"strings"
	"sync"
	"testing"
	"time"
)

// Helper to create a client connection to a server running on a given listener.
// # Mock rationale: Using net.Pipe() to create an in-memory, synchronous network connection
// between a simulated client and the server, avoiding actual network ports and ensuring determinism.
func createClientConn(t *testing.T, server *Server) (net.Conn, *Client, error) {
	clientConn, serverConn := net.Pipe()

	// Simulate server accepting this connection
	s.mu.Lock()
	clientID := s.nextClientID
	s.nextClientID++
	mockClient := &Client{conn: serverConn, send: make(chan string, 100), id: clientID}
	s.clients[mockClient] = true
	s.mu.Unlock()

	s.wg.Add(1)
	go s.handleClient(mockClient)

	return clientConn, mockClient, nil
}

// TestServerStartStop tests basic server startup and shutdown.
func TestServerStartStop(t *testing.T) {
	s := NewServer()
	err := s.Start(0) // Use port 0 to let the OS choose a free port
	if err != nil {
		t.Fatalf("Server failed to start: %v", err)
	}

	if s.listener == nil {
		t.Fatal("Server listener is nil after start")
	}

	s.Stop()

	// Verify listener is closed
	_, err = s.listener.Accept()
	if err == nil || !strings.Contains(err.Error(), "use of closed network connection") {
		t.Errorf("Expected listener to be closed, got: %v", err)
	}
}

// TestSingleClientImmediateMessage tests a single client sending an immediate message.
func TestSingleClientImmediateMessage(t *testing.T) {
	s := NewServer()
	err := s.Start(0)
	if err != nil {
		t.Fatalf("Server failed to start: %v", err)
	}
	defer s.Stop()

	clientConn, _, err := createClientConn(t, s)
	if err != nil {
		t.Fatalf("Failed to create client connection: %v", err)
	}
	defer clientConn.Close()

	expectedMsg := "Hello, Chronos!"
	_, err = clientConn.Write([]byte(expectedMsg + "\n"))
	if err != nil {
		t.Fatalf("Failed to write to client conn: %v", err)
	}

	reader := bufio.NewReader(clientConn)
	// # Mock rationale: Use a short timeout to prevent tests from hanging indefinitely
	// if a message isn't received, making the test deterministic.
	clientConn.SetReadDeadline(time.Now().Add(100 * time.Millisecond))
	received, err := reader.ReadString('\n')
	if err != nil {
		t.Fatalf("Failed to read from client conn: %v", err)
	}

	if strings.TrimSpace(received) != expectedMsg {
		t.Errorf("Expected to receive '%s', got '%s'", expectedMsg, strings.TrimSpace(received))
	}
}

// TestSingleClientDelayedMessage tests a single client sending a delayed message.
func TestSingleClientDelayedMessage(t *testing.T) {
	s := NewServer()
	err := s.Start(0)
	if err != nil {
		t.Fatalf("Server failed to start: %v", err)
	}
	defer s.Stop()

	clientConn, _, err := createClientConn(t, s)
	if err != nil {
		t.Fatalf("Failed to create client connection: %v", err)
	}
	defer clientConn.Close()

	delayDuration := 50 * time.Millisecond // # Mock rationale: Use a short delay for quick test execution.
	expectedMsg := "Delayed greeting!"
	sentMsg := fmt.Sprintf("DELAY=%s:%s", delayDuration.String(), expectedMsg)

	startTime := time.Now()
	_, err = clientConn.Write([]byte(sentMsg + "\n"))
	if err != nil {
		t.Fatalf("Failed to write to client conn: %v", err)
	}

	reader := bufio.NewReader(clientConn)
	// Expect no message immediately
	clientConn.SetReadDeadline(time.Now().Add(delayDuration / 2))
	_, err = reader.ReadString('\n')
	if err == nil || !strings.Contains(err.Error(), "i/o timeout") {
		t.Errorf("Expected timeout, but received message too early: %v", err)
	}

	// Now expect the message after the delay
	clientConn.SetReadDeadline(time.Now().Add(delayDuration * 2))
	received, err := reader.ReadString('\n')
	if err != nil {
		t.Fatalf("Failed to read delayed message: %v", err)
	}
	endTime := time.Now()

	if strings.TrimSpace(received) != expectedMsg {
		t.Errorf("Expected to receive '%s', got '%s'", expectedMsg, strings.TrimSpace(received))
	}

	if endTime.Sub(startTime) < delayDuration {
		t.Errorf("Message delivered too early. Expected at least %s delay, got %s", delayDuration, endTime.Sub(startTime))
	}
}

// TestMultipleClientsDelayedMessage tests a delayed message broadcast to multiple clients.
func TestMultipleClientsDelayedMessage(t *testing.T) {
	s := NewServer()
	err := s.Start(0)
	if err != nil {
		t.Fatalf("Server failed to start: %v", err)
	}
	defer s.Stop()

	var clientConns []net.Conn
	var clientReaders []*bufio.Reader
	numClients := 3

	for i := 0; i < numClients; i++ {
		clientConn, _, err := createClientConn(t, s)
		if err != nil {
			t.Fatalf("Failed to create client %d connection: %v", i, err)
		}
		defer clientConn.Close()
		clientConns = append(clientConns, clientConn)
		clientReaders = append(clientReaders, bufio.NewReader(clientConn))
	}

	delayDuration := 70 * time.Millisecond // # Mock rationale: Short delay for test efficiency.
	expectedMsg := "Broadcast from the future!"
	sentMsg := fmt.Sprintf("DELAY=%s:%s", delayDuration.String(), expectedMsg)

	// Client 0 sends the delayed message
	_, err = clientConns[0].Write([]byte(sentMsg + "\n"))
	if err != nil {
		t.Fatalf("Client 0 failed to write message: %v", err)
	}

	// Wait for the delay to pass and message to be delivered
	time.Sleep(delayDuration + 20*time.Millisecond) // # Mock rationale: Add a small buffer to ensure delivery.

	var wg sync.WaitGroup
	for i := 0; i < numClients; i++ {
		wg.Add(1)
		go func(idx int) {
			defer wg.Done()
			reader := clientReaders[idx]
			conn := clientConns[idx]

			conn.SetReadDeadline(time.Now().Add(50 * time.Millisecond)) // # Mock rationale: Timeout for reading.
			received, readErr := reader.ReadString('\n')
			if readErr != nil {
				if readErr == io.EOF {
					t.Errorf("Client %d: Connection closed unexpectedly.", idx)
				} else if !strings.Contains(readErr.Error(), "i/o timeout") {
					t.Errorf("Client %d: Failed to read message: %v", idx, readErr)
				}
				return
			}

			if strings.TrimSpace(received) != expectedMsg {
				t.Errorf("Client %d: Expected to receive '%s', got '%s'", idx, expectedMsg, strings.TrimSpace(received))
			}
		}(i)
	}
	wg.Wait()
}

// TestInvalidDelayFormat tests that messages with invalid delay formats are sent immediately.
func TestInvalidDelayFormat(t *testing.T) {
	s := NewServer()
	err := s.Start(0)
	if err != nil {
		t.Fatalf("Server failed to start: %v", err)
	}
	defer s.Stop()

	clientConn, _, err := createClientConn(t, s)
	if err != nil {
		t.Fatalf("Failed to create client connection: %v", err)
	}
	defer clientConn.Close()

	expectedMsg := "Invalid delay message"
	invalidSentMsg := fmt.Sprintf("DELAY=badtime:%s", expectedMsg)

	_, err = clientConn.Write([]byte(invalidSentMsg + "\n"))
	if err != nil {
		t.Fatalf("Failed to write invalid message: %v", err)
	}

	reader := bufio.NewReader(clientConn)
	clientConn.SetReadDeadline(time.Now().Add(100 * time.Millisecond)) // # Mock rationale: Expect immediate delivery.
	received, err := reader.ReadString('\n')
	if err != nil {
		t.Fatalf("Failed to read message with invalid delay: %v", err)
	}

	if strings.TrimSpace(received) != expectedMsg {
		t.Errorf("Expected to receive '%s', got '%s' for invalid delay message", expectedMsg, strings.TrimSpace(received))
	}
}
