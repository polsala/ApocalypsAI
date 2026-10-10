package main

import (
	"bufio"
	"fmt"
	"io"
	"net"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock rationale: net.Pipe creates an in-memory, bidirectional pipe that implements net.Conn.
// This allows simulating network communication between a server and multiple clients
// without actual network I/O, making tests deterministic and fast. We can write to one end
// and read from the other, mimicking client-server interaction without relying on actual ports.

func TestAmplifyMessage(t *testing.T) {
	original := "Test message from the void"
	amplified := amplifyMessage(original)

	if !strings.Contains(amplified, original) {
		t.Errorf("Amplified message should contain original: %s", amplified)
	}

	// Check for timestamp format (e.g., [YYYY-MM-DD HH:MM:SS UTC])
	if !strings.Contains(amplified, " UTC]") {
		t.Errorf("Amplified message missing UTC timestamp: %s", amplified)
	}

	// Check for cosmic signature (UUID format)
	if !strings.Contains(amplified, "[Cosmic-Sig:") || !strings.Contains(amplified, "]") {
		t.Errorf("Amplified message missing cosmic signature: %s", amplified)
	}

	// Basic check for UUID format (not a full regex, just presence of hyphens)
	sigStart := strings.Index(amplified, "[Cosmic-Sig: ")
	sigEnd := strings.Index(amplified[sigStart:], "]")
	if sigStart == -1 || sigEnd == -1 {
		t.Errorf("Could not parse cosmic signature from: %s", amplified)
	}
	signature := amplified[sigStart+len("[Cosmic-Sig: "):sigStart+sigEnd]
	if len(signature) != 36 || strings.Count(signature, "-") != 4 {
		t.Errorf("Cosmic signature does not look like a UUID: %s", signature)
	}
}

func TestAmplifierServer_SingleClient(t *testing.T) {
	server := NewAmplifierServer(0) // Port 0 is not used for net.Pipe, but required by constructor

	// Create a mock client connection using net.Pipe
	serverConn, clientConn := net.Pipe()

	// Start the server's run loop in a goroutine
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		server.run()
	}()

	// Manually register the mock client
	mockClient := &client{conn: serverConn, send: make(chan string, 256)}
	server.register <- mockClient

	// Handle the mock client connection in a goroutine
	wg.Add(1)
	go func() {
		defer wg.Done()
		server.handleClient(mockClient)
	}()

	time.Sleep(10 * time.Millisecond) // Give goroutines time to start

	// Client sends a message
	clientMessage := "Hello from client 1"
	_, err := fmt.Fprintln(clientConn, clientMessage)
	if err != nil {
		t.Fatalf("Client failed to write: %v", err)
	}

	// Client reads the amplified message
	reader := bufio.NewReader(clientConn)
	received, err := reader.ReadString('\n')
	if err != nil {
		t.Fatalf("Client failed to read: %v", err)
	}

	if !strings.Contains(received, clientMessage) {
		t.Errorf("Expected received message to contain '%s', got '%s'", clientMessage, received)
	}
	if !strings.Contains(received, "[Cosmic-Sig:") {
		t.Errorf("Expected received message to be amplified, got '%s'", received)
	}

	// Close client connection to trigger unregister
	clientConn.Close()
	time.Sleep(10 * time.Millisecond) // Give unregister time to process

	// Verify client is unregistered
	server.mu.RLock()
	if len(server.clients) != 0 {
		t.Errorf("Expected 0 clients after unregister, got %d", len(server.clients))
	}
	server.mu.RUnlock()

	// Close server channels to allow run() and handleClient to exit
	close(server.register)
	close(server.unregister)
	close(server.broadcast)
	wg.Wait() // Wait for all goroutines to finish
}

func TestAmplifierServer_MultipleClients(t *testing.T) {
	server := NewAmplifierServer(0)

	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		server.run()
	}()

	numClients := 3
	clientConns := make([]net.Conn, numClients)
	clientReaders := make([]*bufio.Reader, numClients)

	for i := 0; i < numClients; i++ {
		serverConn, clientConn := net.Pipe()
		clientConns[i] = clientConn
		clientReaders[i] = bufio.NewReader(clientConn)

		mockClient := &client{conn: serverConn, send: make(chan string, 256)}
		server.register <- mockClient

		wg.Add(1)
		go func() {
			defer wg.Done()
			server.handleClient(mockClient)
		}()
	}

	time.Sleep(50 * time.Millisecond) // Give goroutines time to start and register

	server.mu.RLock()
	if len(server.clients) != numClients {
		t.Fatalf("Expected %d clients registered, got %d", numClients, len(server.clients))
	}
	server.mu.RUnlock()

	// Client 0 sends a message
	senderIndex := 0
	sentMessage := "Broadcast from client 0"
	_, err := fmt.Fprintln(clientConns[senderIndex], sentMessage)
	if err != nil {
		t.Fatalf("Client %d failed to write: %v", senderIndex, err)
	}

	// All clients (including sender) should receive the amplified message
	for i := 0; i < numClients; i++ {
		received, err := clientReaders[i].ReadString('\n')
		if err != nil {
			t.Fatalf("Client %d failed to read: %v", i, err)
		}
		if !strings.Contains(received, sentMessage) {
			t.Errorf("Client %d: Expected received message to contain '%s', got '%s'", i, sentMessage, received)
		}
		if !strings.Contains(received, "[Cosmic-Sig:") {
			t.Errorf("Client %d: Expected received message to be amplified, got '%s'", i, received)
		}
	}

	// Test client disconnection
	clientConns[1].Close()
	time.Sleep(50 * time.Millisecond) // Give unregister time to process

	server.mu.RLock()
	if len(server.clients) != numClients-1 {
		t.Errorf("Expected %d clients after one disconnected, got %d", numClients-1, len(server.clients))
	}
	server.mu.RUnlock()

	// Client 0 sends another message
	sentMessage2 := "Second broadcast from client 0"
	_, err = fmt.Fprintln(clientConns[senderIndex], sentMessage2)
	if err != nil {
		t.Fatalf("Client %d failed to write second message: %v", senderIndex, err)
	}

	// Remaining clients (0 and 2) should receive the amplified message
	for i := 0; i < numClients; i++ {
		if i == 1 { // Client 1 is disconnected
			continue
		}
		received, err := clientReaders[i].ReadString('\n')
		if err != nil {
			t.Fatalf("Client %d failed to read second message: %v", i, err)
		}
		if !strings.Contains(received, sentMessage2) {
			t.Errorf("Client %d: Expected received message to contain '%s', got '%s'", i, sentMessage2, received)
		}
	}

	// Clean up all connections
	for _, conn := range clientConns {
		conn.Close()
	}
	time.Sleep(50 * time.Millisecond)

	server.mu.RLock()
	if len(server.clients) != 0 {
		t.Errorf("Expected 0 clients after all disconnected, got %d", len(server.clients))
	}
	server.mu.RUnlock()

	// Close server channels to allow run() to exit
	close(server.register)
	close(server.unregister)
	close(server.broadcast)
	wg.Wait() // Wait for all goroutines to finish
}

func TestAmplifierServer_EmptyMessage(t *testing.T) {
	server := NewAmplifierServer(0)

	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		server.run()
	}()

	serverConn, clientConn := net.Pipe()
	mockClient := &client{conn: serverConn, send: make(chan string, 256)}
	server.register <- mockClient

	wg.Add(1)
	go func() {
		defer wg.Done()
		server.handleClient(mockClient)
	}()

	time.Sleep(10 * time.Millisecond)

	// Client sends an empty message
	_, err := fmt.Fprintln(clientConn, "")
	if err != nil {
		t.Fatalf("Client failed to write empty message: %v", err)
	}

	// Try to read, should not receive anything (or block indefinitely if not handled)
	// Use a timeout to ensure it doesn't block forever
	readCh := make(chan string)
	go func() {
		reader := bufio.NewReader(clientConn)
		line, readErr := reader.ReadString('\n')
		if readErr != nil && readErr != io.EOF {
			readCh <- fmt.Sprintf("ERROR: %v", readErr)
			return
		}
		readCh <- line
	}()

	select {
	case received := <-readCh:
		if strings.TrimSpace(received) != "" {
			t.Errorf("Expected no message or empty message, got '%s'", received)
		}
	case <-time.After(100 * time.Millisecond):
		// This is good, means no message was broadcast
	}

	clientConn.Close()
	close(server.register)
	close(server.unregister)
	close(server.broadcast)
	wg.Wait()
}
