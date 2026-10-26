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

// TestEchoProcessor_ProcessMessage ensures messages are processed correctly
func TestEchoProcessor_ProcessMessage(t *testing.T) {
	ep := NewEchoProcessor()

	msg1 := "Hello Temporal Void"
	addr1 := "127.0.0.1:12345"
	echo1 := ep.ProcessMessage(msg1, addr1)

	if echo1.ID != 1 {
		t.Errorf("Expected first echo ID to be 1, got %d", echo1.ID)
	}
	if echo1.Message != msg1 {
		t.Errorf("Expected message '%s', got '%s'", msg1, echo1.Message)
	}
	if echo1.ClientAddr != addr1 {
		t.Errorf("Expected client address '%s', got '%s'", addr1, echo1.ClientAddr)
	}
	if time.Since(echo1.Timestamp) > time.Second { // Check timestamp is recent
		t.Errorf("Timestamp is not recent enough: %v", echo1.Timestamp)
	}

	msg2 := "Another ripple"
	addr2 := "127.0.0.1:54321"
	echo2 := ep.ProcessMessage(msg2, addr2)

	if echo2.ID != 2 {
		t.Errorf("Expected second echo ID to be 2, got %d", echo2.ID)
	}
	if echo2.Message != msg2 {
		t.Errorf("Expected message '%s', got '%s'", msg2, echo2.Message)
	}
	if echo2.ClientAddr != addr2 {
		t.Errorf("Expected client address '%s', got '%s'", addr2, echo2.ClientAddr)
	}
}

// TestEchoProcessor_ConcurrentProcessing ensures thread safety and correct ID assignment
func TestEchoProcessor_ConcurrentProcessing(t *testing.T) {
	ep := NewEchoProcessor()
	numGoroutines := 100
	messagesPerGoroutine := 10
	totalMessages := numGoroutines * messagesPerGoroutine

	var wg sync.WaitGroup
	processedEchoes := make(chan Echo, totalMessages)

	for i := 0; i < numGoroutines; i++ {
		wg.Add(1)
		go func(gID int) {
			defer wg.Done()
			addr := fmt.Sprintf("192.168.1.%d:8080", gID)
			for j := 0; j < messagesPerGoroutine; j++ {
				msg := fmt.Sprintf("Goroutine %d, Message %d", gID, j)
				echo := ep.ProcessMessage(msg, addr)
				processedEchoes <- echo
			}
		}(i)
	}

	wg.Wait()
	close(processedEchoes)

	// Collect and verify IDs
	receivedIDs := make(map[int]bool)
	for echo := range processedEchoes {
		if receivedIDs[echo.ID] {
			t.Errorf("Duplicate echo ID found: %d", echo.ID)
		}
		receivedIDs[echo.ID] = true
	}

	if len(receivedIDs) != totalMessages {
		t.Errorf("Expected %d unique echoes, got %d", totalMessages, len(receivedIDs))
	}

	// Check if all IDs from 1 to totalMessages are present
	for i := 1; i <= totalMessages; i++ {
		if !receivedIDs[i] {
			t.Errorf("Missing echo ID: %d", i)
		}
	}
}

// Mock rationale: We use net.Pipe to simulate a network connection in memory
// without requiring actual network sockets, making tests deterministic and offline.
func TestServer_HandleConnection(t *testing.T) {
	// Capture log output to verify it
	var logBuffer bytes.Buffer
	log.SetOutput(&logBuffer)
	defer func() {
		log.SetOutput(os.Stderr) // Restore default output
	}()

	server := NewServer(0) // Port doesn't matter for handleConnection test
	defer server.Stop()    // Ensure cleanup

	// Create a pipe to simulate client-server connection
	clientConn, serverConn := net.Pipe()
	defer clientConn.Close()
	defer serverConn.Close()

	// Simulate client sending messages
	go func() {
		fmt.Fprintf(clientConn, "First echo\n")
		time.Sleep(10 * time.Millisecond) // Simulate network delay
		fmt.Fprintf(clientConn, "Second echo\n")
		clientConn.Close() // Client closes connection
	}()

	// Run handleConnection in a goroutine
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		server.handleConnection(serverConn)
		wg.Done()
	}()

	// Collect echoes from the server's channel
	var receivedEchoes []Echo
	collectDone := make(chan struct{})
	go func() {
		for echo := range server.echoChannel {
			receivedEchoes = append(receivedEchoes, echo)
			if len(receivedEchoes) == 2 { // Expecting 2 echoes
				close(collectDone)
				return
			}
		}
	}()

	// Wait for handleConnection to finish and echoes to be collected
	select {
	case <-collectDone:
		// Echoes collected
	case <-time.After(500 * time.Millisecond):
		t.Fatal("Timed out waiting for echoes to be collected")
	}
	wg.Wait() // Wait for handleConnection to finish

	if len(receivedEchoes) != 2 {
		t.Fatalf("Expected 2 echoes, got %d", len(receivedEchoes))
	}

	if receivedEchoes[0].Message != "First echo" {
		t.Errorf("Expected first message 'First echo', got '%s'", receivedEchoes[0].Message)
	}
	if receivedEchoes[1].Message != "Second echo" {
		t.Errorf("Expected second message 'Second echo', got '%s'", receivedEchoes[1].Message)
	}

	// Verify log output contains connection open/close messages
	logOutput := logBuffer.String()
	if !strings.Contains(logOutput, "New temporal conduit opened from pipe") {
		t.Errorf("Expected log output to contain 'New temporal conduit opened', got:\n%s", logOutput)
	}
	if !strings.Contains(logOutput, "Temporal conduit from pipe closed.") {
		t.Errorf("Expected log output to contain 'Temporal conduit from pipe closed', got:\n%s", logOutput)
	}
}

// TestServer_StartAndStop ensures the server can start and stop gracefully
func TestServer_StartAndStop(t *testing.T) {
	// Capture log output
	var logBuffer bytes.Buffer
	log.SetOutput(&logBuffer)
	defer func() {
		log.SetOutput(os.Stderr)
	}()

	// Use a real server on an ephemeral port (port 0)
	// This is deterministic for local testing as it uses a free port.
	server := NewServer(0)
	err := server.Start()
	if err != nil {
		t.Fatalf("Failed to start server: %v", err)
	}

	// Give it a moment to start listening
	time.Sleep(50 * time.Millisecond)

	// Verify server started log
	logOutput := logBuffer.String()
	if !strings.Contains(logOutput, "Temporal Echo Listener started on :") {
		t.Errorf("Expected 'Server started' log, got:\n%s", logOutput)
	}

	// Now stop the server
	server.Stop()

	// Verify server stopped log
	logOutput = logBuffer.String()
	if !strings.Contains(logOutput, "Temporal Echo Listener stopped.") {
		t.Errorf("Expected 'Server stopped' log, got:\n%s", logOutput)
	}
	if !strings.Contains(logOutput, "Echo logging goroutine stopped.") {
		t.Errorf("Expected 'Echo logging goroutine stopped' log, got:\n%s", logOutput)
	}
	if !strings.Contains(logOutput, "Server listener shutting down.") {
		t.Errorf("Expected 'Server listener shutting down' log, got:\n%s", logOutput)
	}
}

// TestServer_EndToEnd_SingleClient tests a full cycle with a real client connection
func TestServer_EndToEnd_SingleClient(t *testing.T) {
	// Capture log output
	var logBuffer bytes.Buffer
	log.SetOutput(&logBuffer)
	defer func() {
		log.SetOutput(os.Stderr)
	}()

	server := NewServer(0) // Use ephemeral port
	err := server.Start()
	if err != nil {
		t.Fatalf("Failed to start server: %v", err)
	}
	defer server.Stop()

	// Get the actual port the server is listening on
	addr := server.listener.Addr().(*net.TCPAddr)
	port := addr.Port

	// Connect a client
	clientConn, err := net.Dial("tcp", fmt.Sprintf("127.0.0.1:%d", port))
	if err != nil {
		t.Fatalf("Failed to connect client: %v", err)
	}
	defer clientConn.Close()

	// Send messages
	messages := []string{"First temporal ripple", "Second temporal ripple", "Third temporal ripple"}
	for _, msg := range messages {
		_, err := fmt.Fprintf(clientConn, "%s\n", msg)
		if err != nil {
			t.Fatalf("Failed to send message: %v", err)
		}
		time.Sleep(10 * time.Millisecond) // Give server time to process
	}

	// Close client connection to signal EOF to server
	clientConn.Close()

	// Give server time to process and close connection
	time.Sleep(100 * time.Millisecond)

	// Verify echoes were logged
	logOutput := logBuffer.String()
	for i, msg := range messages {
		expectedLogPart := fmt.Sprintf("[ECHO %d]", i+1)
		if !strings.Contains(logOutput, expectedLogPart) || !strings.Contains(logOutput, msg) {
			t.Errorf("Expected log output to contain '%s' and '%s', but it didn't:\n%s", expectedLogPart, msg, logOutput)
		}
	}
}

// TestServer_EndToEnd_MultipleClients tests concurrent client connections
func TestServer_EndToEnd_MultipleClients(t *testing.T) {
	// Capture log output
	var logBuffer bytes.Buffer
	log.SetOutput(&logBuffer)
	defer func() {
		log.SetOutput(os.Stderr)
	}()

	server := NewServer(0) // Use ephemeral port
	err := server.Start()
	if err != nil {
		t.Fatalf("Failed to start server: %v", err)
	}
	defer server.Stop()

	// Get the actual port
	addr := server.listener.Addr().(*net.TCPAddr)
	port := addr.Port

	numClients := 5
	messagesPerClient := 3
	totalExpectedEchoes := numClients * messagesPerClient

	var clientWg sync.WaitGroup
	for i := 0; i < numClients; i++ {
		clientWg.Add(1)
		go func(clientID int) {
			defer clientWg.Done()
			conn, err := net.Dial("tcp", fmt.Sprintf("127.0.0.1:%d", port))
			if err != nil {
				t.Errorf("Client %d failed to connect: %v", clientID, err)
				return
			}
			defer conn.Close()

			for j := 0; j < messagesPerClient; j++ {
				msg := fmt.Sprintf("Client %d, Message %d", clientID, j)
				_, err := fmt.Fprintf(conn, "%s\n", msg)
				if err != nil {
					t.Errorf("Client %d failed to send message: %v", clientID, err)
					return
				}
				time.Sleep(time.Duration(clientID*10+j) * time.Millisecond) // Vary delay
			}
		}(i)
	}

	clientWg.Wait() // Wait for all clients to send messages and close
	time.Sleep(500 * time.Millisecond) // Give server time to process all echoes

	// Verify all echoes were logged
	logOutput := logBuffer.String()
	foundEchoes := 0
	for i := 1; i <= totalExpectedEchoes; i++ {
		expectedLogPart := fmt.Sprintf("[ECHO %d]", i)
		if strings.Contains(logOutput, expectedLogPart) {
			foundEchoes++
		}
	}

	if foundEchoes != totalExpectedEchoes {
		t.Errorf("Expected %d echoes to be logged, found %d.\nLog:\n%s", totalExpectedEchoes, foundEchoes, logOutput)
	}
}
