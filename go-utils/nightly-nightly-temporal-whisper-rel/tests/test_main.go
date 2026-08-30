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

// Mock rationale: net.Pipe() creates an in-memory, synchronous full-duplex connection pair.
// This allows us to simulate network communication without binding to actual ports,
// making tests deterministic, fast, and isolated from network conditions.
// We control both ends of the "connection" directly, which is crucial for testing
// concurrent network services reliably without external dependencies.

func TestTemporalWhisperRelay_SingleClient(t *testing.T) {
	// Suppress log output during tests for cleaner output
	log.SetOutput(new(bytes.Buffer))

	relay, err := NewTemporalWhisperRelay("0", 10*time.Millisecond, 20*time.Millisecond) // Use "0" for random available port
	if err != nil {
		t.Fatalf("Failed to create relay: %v", err)
	}
	relay.Start()
	defer relay.Stop()

	// Create a mock client connection using net.Pipe
	clientConn, serverConn := net.Pipe()
	defer clientConn.Close()
	defer serverConn.Close()

	// Manually add the server-side of the pipe to the relay's client list
	// In a real scenario, this would happen via Accept()
	relay.addClient(serverConn)
	go relay.handleConnection(serverConn) // Start handling this mock connection

	// Send a message from the client
	message := "Hello Echo!"
	_, err = clientConn.Write([]byte(message + "\n"))
	if err != nil {
		t.Fatalf("Client failed to write: %v", err)
	}

	// Since there's only one client, it shouldn't receive its own echo.
	// Wait longer than max delay to ensure no message is broadcasted back to sender.
	time.Sleep(relay.maxDelay + 50*time.Millisecond)

	// Try to read from the client, expect nothing
	clientReader := bufio.NewReader(clientConn)
	clientConn.SetReadDeadline(time.Now().Add(50 * time.Millisecond)) // Short timeout
	_, err = clientReader.ReadString('\n')
	if err == nil {
		t.Errorf("Expected no message back to sender, but received one.")
	} else if !strings.Contains(err.Error(), "timeout") {
		// net.Pipe can return io.EOF or other errors on close, but for a read with timeout, it should be timeout.
		if !strings.Contains(err.Error(), "EOF") {
			t.Errorf("Expected timeout or EOF error, got: %v", err)
		}
	}
}

func TestTemporalWhisperRelay_TwoClients(t *testing.T) {
	log.SetOutput(new(bytes.Buffer))

	relay, err := NewTemporalWhisperRelay("0", 10*time.Millisecond, 20*time.Millisecond)
	if err != nil {
		t.Fatalf("Failed to create relay: %v", err)
	}
	relay.Start()
	defer relay.Stop()

	// Client 1
	client1Conn, server1Conn := net.Pipe()
	defer client1Conn.Close()
	defer server1Conn.Close()
	relay.addClient(server1Conn)
	go relay.handleConnection(server1Conn)

	// Client 2
	client2Conn, server2Conn := net.Pipe()
	defer client2Conn.Close()
	defer server2Conn.Close()
	relay.addClient(server2Conn)
	go relay.handleConnection(server2Conn)

	var wg sync.WaitGroup
	wg.Add(1) // Wait for client 2 to receive message

	// Client 2 goroutine to read messages
	receivedMsg := make(chan string, 1)
	go func() {
		defer wg.Done()
		client2Reader := bufio.NewReader(client2Conn)
		client2Conn.SetReadDeadline(time.Now().Add(relay.maxDelay + 100*time.Millisecond)) // Long enough to receive
		msg, err := client2Reader.ReadString('\n')
		if err != nil {
			t.Errorf("Client 2 failed to read: %v", err)
			return
		}
		receivedMsg <- strings.TrimSpace(msg)
	}()

	// Send message from Client 1
	message1 := "Whisper from Client 1"
	_, err = client1Conn.Write([]byte(message1 + "\n"))
	if err != nil {
		t.Fatalf("Client 1 failed to write: %v", err)
	}

	// Wait for client 2 to receive the message
	wg.Wait()

	select {
	case msg := <-receivedMsg:
		expectedPrefix := fmt.Sprintf("Echo from the past (%s): %s", server1Conn.RemoteAddr(), message1)
		if !strings.HasPrefix(msg, expectedPrefix) {
			t.Errorf("Client 2 received unexpected message.\nExpected prefix: %s\nActual: %s", expectedPrefix, msg)
		}
	case <-time.After(relay.maxDelay + 150*time.Millisecond): // Extra buffer time
		t.Error("Client 2 did not receive message within expected time.")
	}

	// Ensure Client 1 did NOT receive its own message
	client1Reader := bufio.NewReader(client1Conn)
	client1Conn.SetReadDeadline(time.Now().Add(50 * time.Millisecond)) // Short timeout
	_, err = client1Reader.ReadString('\n')
	if err == nil {
		t.Errorf("Client 1 unexpectedly received its own message.")
	} else if !strings.Contains(err.Error(), "timeout") && !strings.Contains(err.Error(), "EOF") {
		t.Errorf("Expected timeout or EOF error for client 1, got: %v", err)
	}
}

func TestTemporalWhisperRelay_Shutdown(t *testing.T) {
	log.SetOutput(new(bytes.Buffer))

	relay, err := NewTemporalWhisperRelay("0", 10*time.Millisecond, 20*time.Millisecond)
	if err != nil {
		t.Fatalf("Failed to create relay: %v", err)
	}
	relay.Start()

	// Give it a moment to start up
	time.Sleep(50 * time.Millisecond)

	// Create a mock client connection
	clientConn, serverConn := net.Pipe()
	defer clientConn.Close()
	defer serverConn.Close()
	relay.addClient(serverConn)
	go relay.handleConnection(serverConn)

	relay.Stop()

	// Verify listener is closed by trying to dial it (should fail)
	// Note: For net.Pipe, the listener is internal. We test the effect on client connections.
	// For a real TCP listener, we'd try net.Dial.

	// Verify client connection is closed (writing should fail)
	_, err = clientConn.Write([]byte("test\n"))
	if err == nil {
		t.Error("Expected client write to fail after relay shutdown, but it succeeded.")
	} else if !strings.Contains(err.Error(), "closed pipe") && !strings.Contains(err.Error(), "broken pipe") {
		t.Errorf("Expected 'closed pipe' or 'broken pipe' error, got: %v", err)
	}
}

func TestTemporalWhisperRelay_MultipleMessages(t *testing.T) {
	log.SetOutput(new(bytes.Buffer))

	relay, err := NewTemporalWhisperRelay("0", 10*time.Millisecond, 20*time.Millisecond)
	if err != nil {
		t.Fatalf("Failed to create relay: %v", err)
	}
	relay.Start()
	defer relay.Stop()

	client1Conn, server1Conn := net.Pipe()
	defer client1Conn.Close()
	defer server1Conn.Close()
	relay.addClient(server1Conn)
	go relay.handleConnection(server1Conn)

	client2Conn, server2Conn := net.Pipe()
	defer client2Conn.Close()
	defer server2Conn.Close()
	relay.addClient(server2Conn)
	go relay.handleConnection(server2Conn)

	var wg sync.WaitGroup
	wg.Add(2) // Two messages expected by client 2

	receivedMessages := make(chan string, 2)
	go func() {
		client2Reader := bufio.NewReader(client2Conn)
		for i := 0; i < 2; i++ {
			client2Conn.SetReadDeadline(time.Now().Add(relay.maxDelay + 100*time.Millisecond))
			msg, err := client2Reader.ReadString('\n')
			if err != nil {
				t.Errorf("Client 2 failed to read message %d: %v", i+1, err)
				return
			}
			receivedMessages <- strings.TrimSpace(msg)
			wg.Done()
		}
	}()

	// Send two messages from Client 1
	message1 := "First Whisper"
	message2 := "Second Whisper"
	_, err = client1Conn.Write([]byte(message1 + "\n"))
	if err != nil {
		t.Fatalf("Client 1 failed to write message 1: %v", err)
	}
	time.Sleep(5 * time.Millisecond) // Small delay between sends to ensure they are distinct
	_, err = client1Conn.Write([]byte(message2 + "\n"))
	if err != nil {
		t.Fatalf("Client 1 failed to write message 2: %v", err)
	}

	wg.Wait() // Wait for both messages to be received by client 2

	close(receivedMessages)
	var msgs []string
	for msg := range receivedMessages {
		msgs = append(msgs, msg)
	}

	if len(msgs) != 2 {
		t.Fatalf("Expected 2 messages, got %d", len(msgs))
	}

	expectedPrefix1 := fmt.Sprintf("Echo from the past (%s): %s", server1Conn.RemoteAddr(), message1)
	expectedPrefix2 := fmt.Sprintf("Echo from the past (%s): %s", server1Conn.RemoteAddr(), message2)

	// Order might not be strictly preserved due to random delays, but content should match
	found1 := false
	found2 := false
	for _, msg := range msgs {
		if strings.HasPrefix(msg, expectedPrefix1) {
			found1 = true
		}
		if strings.HasPrefix(msg, expectedPrefix2) {
			found2 = true
		}
	}

	if !found1 {
		t.Errorf("Message '%s' not found in received messages.", message1)
	}
	if !found2 {
		t.Errorf("Message '%s' not found in received messages.", message2)
	}
}

func TestTemporalWhisperRelay_ClientDisconnect(t *testing.T) {
	log.SetOutput(new(bytes.Buffer))

	relay, err := NewTemporalWhisperRelay("0", 10*time.Millisecond, 20*time.Millisecond)
	if err != nil {
		t.Fatalf("Failed to create relay: %v", err)
	}
	relay.Start()
	defer relay.Stop()

	client1Conn, server1Conn := net.Pipe()
	defer client1Conn.Close()
	defer server1Conn.Close()
	relay.addClient(server1Conn)
	go relay.handleConnection(server1Conn)

	client2Conn, server2Conn := net.Pipe()
	defer client2Conn.Close()
	defer server2Conn.Close()
	relay.addClient(server2Conn)
	go relay.handleConnection(server2Conn)

	// Client 1 sends a message
	message := "Test disconnect"
	_, err = client1Conn.Write([]byte(message + "\n"))
	if err != nil {
		t.Fatalf("Client 1 failed to write: %v", err)
	}

	// Wait for message to be processed and broadcasted
	time.Sleep(relay.maxDelay + 50*time.Millisecond)

	// Client 2 disconnects
	client2Conn.Close()
	time.Sleep(50 * time.Millisecond) // Give time for handleConnection to detect EOF and remove client

	// Verify client 2 is removed from the relay's client list
	relay.clientsMutex.Lock()
	_, exists := relay.clients[server2Conn]
	relay.clientsMutex.Unlock()

	if exists {
		t.Errorf("Client 2 was not removed from relay's client list after disconnect.")
	}

	// Ensure Client 1 can still send and receive (if there was another client)
	// For this test, there are no other clients left to receive from Client 1.
	// We just check that the relay didn't crash.
	message2 := "Still alive?"
	_, err = client1Conn.Write([]byte(message2 + "\n"))
	if err != nil {
		t.Fatalf("Client 1 failed to write after client 2 disconnect: %v", err)
	}
	time.Sleep(relay.maxDelay + 50*time.Millisecond)

	// Client 1 should not receive its own message
	client1Reader := bufio.NewReader(client1Conn)
	client1Conn.SetReadDeadline(time.Now().Add(50 * time.Millisecond))
	_, err = client1Reader.ReadString('\n')
	if err == nil {
		t.Errorf("Client 1 unexpectedly received its own message after client 2 disconnect.")
	} else if !strings.Contains(err.Error(), "timeout") && !strings.Contains(err.Error(), "EOF") {
		t.Errorf("Expected timeout or EOF error for client 1, got: %v", err)
	}
}
