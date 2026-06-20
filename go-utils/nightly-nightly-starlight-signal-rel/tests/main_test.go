package main

import (
	"bufio"
	"fmt"
	"net"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock rationale: For deterministic testing of a network service, we use actual `net.Listen`
// and `net.Dial` on `localhost` to simulate network interactions. This provides a realistic
// test environment without relying on external services. Timing is managed with `time.Sleep`
// to allow goroutines to schedule and network buffers to clear, and `SetReadDeadline` for
// non-blocking reads with timeouts. The `processMessage` function's outputs (timestamp and
// signature) are deterministic for a given input, allowing for predictable verification.

func TestServerStartAndStop(t *testing.T) {
	server := NewServer("8081") // Use a different port for tests
	err := server.Start()
	if err != nil {
		t.Fatalf("Server failed to start: %v", err)
	}
	if !server.running {
		t.Error("Server should be running after Start()")
	}

	server.Stop()
	if server.running {
		t.Error("Server should not be running after Stop()")
	}
}

func TestSingleClientMessageBroadcast(t *testing.T) {
	server := NewServer("8082")
	err := server.Start()
	if err != nil {
		t.Fatalf("Server failed to start: %v", err)
	}
	defer server.Stop()

	// Give server a moment to start listening
	time.Sleep(10 * time.Millisecond)

	clientConn, err := net.Dial("tcp", "localhost:8082")
	if err != nil {
		t.Fatalf("Client failed to connect: %v", err)
	}
	defer clientConn.Close()

	reader := bufio.NewReader(clientConn)
	writer := bufio.NewWriter(clientConn)

	// Wait for the "client joined" message
	joinedMsg, _ := reader.ReadString('\n')
	if !strings.Contains(joinedMsg, "has joined the relay.") {
		t.Errorf("Expected join message, got: %s", joinedMsg)
	}

	testMessage := "Hello Starlight!"
	_, err = writer.WriteString(testMessage + "\n")
	if err != nil {
		t.Fatalf("Failed to write message: %v", err)
	}
	writer.Flush()

	// The server broadcasts the message back to the sender (and all others)
	// We need to read until we get the actual broadcast message, skipping any other join messages
	timeout := time.After(2 * time.Second)
	var receivedMessage string
	for {
		select {
		case <-timeout:
			t.Fatalf("Client timed out waiting for broadcast message")
		default:
			clientConn.SetReadDeadline(time.Now().Add(100 * time.Millisecond)) // Short deadline for non-blocking read
			msg, err := reader.ReadString('\n')
			if err != nil {
				if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
					continue // Keep trying
				}
				if err.Error() == "EOF" { // Connection closed
					break
				}
				t.Fatalf("Failed to read message: %v", err)
			}
			if strings.Contains(msg, testMessage) && strings.Contains(msg, "Signature:") {
				receivedMessage = msg
				goto FoundMessage // Exit loop and continue test
			}
		}
	}
FoundMessage:

	if !strings.Contains(receivedMessage, testMessage) {
		t.Errorf("Received message does not contain original message. Got: %s, Expected to contain: %s", receivedMessage, testMessage)
	}
	if !strings.Contains(receivedMessage, "Signature:") {
		t.Errorf("Received message missing starlight signature. Got: %s", receivedMessage)
	}
	if !strings.Contains(receivedMessage, "From:") {
		t.Errorf("Received message missing sender ID. Got: %s", receivedMessage)
	}
	// Check for the presence of a timestamp pattern (e.g., YYYY-MM-DDTHH:MM:SS)
	if !strings.Contains(receivedMessage, time.Now().UTC().Format("2006-01-02T")) {
		t.Errorf("Received message missing cosmic timestamp. Got: %s", receivedMessage)
	}
}

func TestMultipleClientsBroadcast(t *testing.T) {
	server := NewServer("8083")
	err := server.Start()
	if err != nil {
		t.Fatalf("Server failed to start: %v", err)
	}
	defer server.Stop()

	time.Sleep(10 * time.Millisecond) // Give server a moment to start

	var wg sync.WaitGroup
	numClients := 3
	clientConns := make([]net.Conn, numClients)
	clientReaders := make([]*bufio.Reader, numClients)
	clientWriters := make([]*bufio.Writer, numClients)

	for i := 0; i < numClients; i++ {
		conn, err := net.Dial("tcp", "localhost:8083")
		if err != nil {
			t.Fatalf("Client %d failed to connect: %v", i, err)
		}
		clientConns[i] = conn
		clientReaders[i] = bufio.NewReader(conn)
		clientWriters[i] = bufio.NewWriter(conn)
		defer conn.Close()

		// Read initial join messages (one for self, others for other clients joining)
		// We'll just read until we get a message that's not a join message from another client.
		// For simplicity, let's just read the first message (self-join)
		_, _ = clientReaders[i].ReadString('\n') // Read self-join message
	}

	// Wait for all clients to connect and for their join messages to propagate
	time.Sleep(50 * time.Millisecond)

	testMessage := "Broadcast from Client 0"
	_, err = clientWriters[0].WriteString(testMessage + "\n")
	if err != nil {
		t.Fatalf("Client 0 failed to write message: %v", err)
	}
	clientWriters[0].Flush()

	// Each client should receive the broadcast message
	for i := 0; i < numClients; i++ {
		wg.Add(1)
		go func(clientIdx int) {
			defer wg.Done()
			// Read messages until we find the one we sent, or timeout
			timeout := time.After(2 * time.Second)
			for {
				select {
				case <-timeout:
					t.Errorf("Client %d timed out waiting for message", clientIdx)
					return
				default:
					clientConns[clientIdx].SetReadDeadline(time.Now().Add(100 * time.Millisecond)) // Short deadline for non-blocking read
					receivedMessage, err := clientReaders[clientIdx].ReadString('\n')
					if err != nil {
						if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
							continue // Keep trying
						}
						if err.Error() == "EOF" { // Connection closed
							return
						}
						t.Errorf("Client %d failed to read message: %v", clientIdx, err)
						return
					}

					if strings.Contains(receivedMessage, testMessage) {
						if !strings.Contains(receivedMessage, "Signature:") {
							t.Errorf("Client %d: Received message missing starlight signature. Got: %s", clientIdx, receivedMessage)
						}
						if !strings.Contains(receivedMessage, "From:") {
							t.Errorf("Client %d: Received message missing sender ID. Got: %s", clientIdx, receivedMessage)
						}
						if !strings.Contains(receivedMessage, time.Now().UTC().Format("2006-01-02T")) {
							t.Errorf("Client %d: Received message missing cosmic timestamp. Got: %s", clientIdx, receivedMessage)
						}
						return // Found the message
					}
				}
			}
		}(i)
	}
	wg.Wait()
}

func TestClientDisconnect(t *testing.T) {
	server := NewServer("8084")
	err := server.Start()
	if err != nil {
		t.Fatalf("Server failed to start: %v", err)
	}
	defer server.Stop()

	time.Sleep(10 * time.Millisecond)

	client1, err := net.Dial("tcp", "localhost:8084")
	if err != nil {
		t.Fatalf("Client 1 failed to connect: %v", err)
	}
	reader1 := bufio.NewReader(client1)
	_, _ = reader1.ReadString('\n') // Read join message

	client2, err := net.Dial("tcp", "localhost:8084")
	if err != nil {
		t.Fatalf("Client 2 failed to connect: %v", err)
	}
	reader2 := bufio.NewReader(client2)
	_, _ = reader2.ReadString('\n') // Read join message

	// Client 2 should receive client 1's join message
	// Read until client 1's join message is received by client 2
	timeout := time.After(1 * time.Second)
	foundJoin := false
	for {
		select {
		case <-timeout:
			t.Fatalf("Client 2 timed out waiting for client 1's join message")
		default:
			client2.SetReadDeadline(time.Now().Add(100 * time.Millisecond))
			msg, err := reader2.ReadString('\n')
			if err != nil {
				if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
					continue
				}
				if err.Error() == "EOF" { // Connection closed
					break
				}
				t.Fatalf("Client 2 error reading: %v", err)
			}
			if strings.Contains(msg, client1.RemoteAddr().String()+" has joined the relay.") {
				foundJoin = true
				break
			}
		}
	}
	if !foundJoin {
		t.Fatal("Client 2 did not receive client 1's join message.")
	}

	// Now, client 1 disconnects
	client1.Close()

	// Client 2 should receive a disconnect message from client 1
	timeout = time.After(1 * time.Second)
	foundDisconnect := false
	for {
		select {
		case <-timeout:
			t.Fatalf("Client 2 timed out waiting for client 1's disconnect message")
		default:
			client2.SetReadDeadline(time.Now().Add(100 * time.Millisecond))
			msg, err := reader2.ReadString('\n')
			if err != nil {
				if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
					continue
				}
				if err.Error() == "EOF" {
					break
				}
				t.Fatalf("Client 2 error reading: %v", err)
			}
			if strings.Contains(msg, client1.RemoteAddr().String()+" has left the relay.") {
				foundDisconnect = true
				break
			}
		}
	}
	if !foundDisconnect {
		t.Error("Client 2 did not receive client 1's disconnect message.")
	}
	client2.Close()
}
