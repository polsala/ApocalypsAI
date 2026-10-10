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

// mockDelayGenerator provides a fixed, short delay for deterministic testing.
// # Mock rationale: We want to test the *logic* of delayed broadcasting, not the randomness or actual wall-clock time.
// # A fixed, short delay allows tests to complete quickly and deterministically.
func mockDelayGenerator(min, max int) time.Duration {
	return 10 * time.Millisecond // Fixed short delay for tests
}

func TestServerStartAndShutdown(t *testing.T) {
	server := NewServer(0, 100, 200, mockDelayGenerator)
	err := server.Start(0) // Use port 0 for OS-assigned port
	if err != nil {
		t.Fatalf("Server failed to start: %v", err)
	}

	// Give a moment for listener to be ready
	time.Sleep(50 * time.Millisecond)

	server.Shutdown()

	// Verify listener is closed
	conn, err := net.Dial("tcp", server.listener.Addr().String())
	if err == nil {
		conn.Close()
		t.Fatal("Server listener still open after shutdown")
	}
}

func TestSingleClientMessageBroadcast(t *testing.T) {
	server := NewServer(0, 100, 200, mockDelayGenerator)
	err := server.Start(0)
	if err != nil {
		t.Fatalf("Server failed to start: %v", err)
	}
	defer server.Shutdown()

	serverAddr := server.listener.Addr().String()

	client1, err := net.Dial("tcp", serverAddr)
	if err != nil {
		t.Fatalf("Client 1 failed to connect: %v", err)
	}
	defer client1.Close()

	message := "Hello, Chronal World!"

	// Send message from client1
	_, err = client1.Write([]byte(message + "\n"))
	if err != nil {
		t.Fatalf("Client 1 failed to send message: %v", err)
	}

	// Expect to receive the message back on client1 after delay
	reader1 := bufio.NewReader(client1)
	receivedMsgChan := make(chan string, 1)

	go func() {
		msg, err := reader1.ReadString('\n')
		if err != nil {
			receivedMsgChan <- fmt.Sprintf("error: %v", err)
			return
		}
		receivedMsgChan <- strings.TrimSpace(msg)
	}()

	select {
	case received := <-receivedMsgChan:
		expectedPrefix := fmt.Sprintf("[%s] %s", client1.LocalAddr(), message)
		if !strings.HasPrefix(received, expectedPrefix) {
			t.Errorf("Expected message prefix '%s', got '%s'", expectedPrefix, received)
		}
	case <-time.After(500 * time.Millisecond): // Timeout longer than mock delay
		t.Fatal("Client 1 did not receive message within timeout")
	}
}

func TestMultipleClientsBroadcast(t *testing.T) {
	server := NewServer(0, 100, 200, mockDelayGenerator)
	err := server.Start(0)
	if err != nil {
		t.Fatalf("Server failed to start: %v", err)
	}
	defer server.Shutdown()

	serverAddr := server.listener.Addr().String()

	var clients []net.Conn
	var readers []*bufio.Reader
	numClients := 3

	for i := 0; i < numClients; i++ {
		conn, err := net.Dial("tcp", serverAddr)
		if err != nil {
			t.Fatalf("Client %d failed to connect: %v", i+1, err)
		}
		defer conn.Close()
		clients = append(clients, conn)
		readers = append(readers, bufio.NewReader(conn))
	}

	message := "Ripple Effect Test!"

	// Client 1 sends a message
	_, err = clients[0].Write([]byte(message + "\n"))
	if err != nil {
		t.Fatalf("Client 1 failed to send message: %v", err)
	}

	var wg sync.WaitGroup
	receivedCount := 0
	var mu sync.Mutex

	expectedPrefix := fmt.Sprintf("[%s] %s", clients[0].LocalAddr(), message)

	for i := 0; i < numClients; i++ {
		wg.Add(1)
		go func(clientIdx int, reader *bufio.Reader) {
			defer wg.Done()
			select {
			case <-time.After(500 * time.Millisecond): // Timeout longer than mock delay
				t.Errorf("Client %d did not receive message within timeout", clientIdx+1)
				return
			default:
				msg, err := reader.ReadString('\n')
				if err != nil {
					t.Errorf("Client %d error reading: %v", clientIdx+1, err)
					return
				}
				if !strings.HasPrefix(strings.TrimSpace(msg), expectedPrefix) {
					t.Errorf("Client %d: Expected message prefix '%s', got '%s'", clientIdx+1, expectedPrefix, strings.TrimSpace(msg))
					return
				}
				mu.Lock()
				receivedCount++
				mu.Unlock()
			}
		}(i, readers[i])
	}

	wg.Wait()

	if receivedCount != numClients {
		t.Errorf("Expected %d clients to receive message, got %d", numClients, receivedCount)
	}
}

func TestClientDisconnect(t *testing.T) {
	server := NewServer(0, 100, 200, mockDelayGenerator)
	err := server.Start(0)
	if err != nil {
		t.Fatalf("Server failed to start: %v", err)
	}
	defer server.Shutdown()

	serverAddr := server.listener.Addr().String()

	client1, err := net.Dial("tcp", serverAddr)
	if err != nil {
		t.Fatalf("Client 1 failed to connect: %v", err)
	}
	client1.Close() // Disconnect client 1 immediately

	// Give server a moment to process disconnect
	time.Sleep(50 * time.Millisecond)

	// Verify client1 is removed from server's client list
	server.mu.Lock()
	numClients := len(server.clients)
	server.mu.Unlock()

	if numClients != 0 {
		t.Errorf("Expected 0 clients after disconnect, got %d", numClients)
	}

	// Connect another client to ensure server is still operational
	client2, err := net.Dial("tcp", serverAddr)
	if err != nil {
		t.Fatalf("Client 2 failed to connect after client 1 disconnect: %v", err)
	}
	defer client2.Close()

	server.mu.Lock()
	numClients = len(server.clients)
	server.mu.Unlock()

	if numClients != 1 {
		t.Errorf("Expected 1 client after client 2 connects, got %d", numClients)
	}
}

func TestEmptyMessageIgnored(t *testing.T) {
	server := NewServer(0, 100, 200, mockDelayGenerator)
	err := server.Start(0)
	if err != nil {
		t.Fatalf("Server failed to start: %v", err)
	}
	defer server.Shutdown()

	serverAddr := server.listener.Addr().String()

	client1, err := net.Dial("tcp", serverAddr)
	if err != nil {
		t.Fatalf("Client 1 failed to connect: %v", err)
	}
	defer client1.Close()

	// Send an empty message (just a newline)
	_, err = client1.Write([]byte("\n"))
	if err != nil {
		t.Fatalf("Client 1 failed to send empty message: %v", err)
	}

	reader1 := bufio.NewReader(client1)
	readChan := make(chan string, 1)

	go func() {
		msg, err := reader1.ReadString('\n')
		if err != nil {
			readChan <- fmt.Sprintf("error: %v", err)
			return
		}
		readChan <- strings.TrimSpace(msg)
	}()

	select {
	case received := <-readChan:
		t.Errorf("Received unexpected message: '%s'", received)
	case <-time.After(200 * time.Millisecond): // Longer than mock delay, but short enough to confirm no message
		// Expected: no message received
	}
}
