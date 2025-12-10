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

// TestVoidWhisperRelay verifies that messages are correctly relayed and distorted between clients.
func TestVoidWhisperRelay(t *testing.T) {
	// Start the server in a goroutine
	go main()

	// Give the server a moment to start listening
	time.Sleep(100 * time.Millisecond)

	// Connect two clients
	client1, err := net.Dial("tcp", "localhost:"+PORT)
	if err != nil {
		t.Fatalf("Failed to connect client 1: %v", err)
	}
	defer client1.Close()

	client2, err := net.Dial("tcp", "localhost:"+PORT)
	if err != nil {
		t.Fatalf("Failed to connect client 2: %v", err)
	}
	defer client2.Close()

	// Use a WaitGroup to ensure all goroutines finish before the test exits
	var wg sync.WaitGroup

	// Reader for client 1
	client1Reader := bufio.NewReader(client1)
	client1Received := make(chan string, 1)
	wg.Add(1)
	go func() {
		defer wg.Done()
		line, err := client1Reader.ReadString('\n')
		if err == nil {
			client1Received <- strings.TrimSpace(line)
		}
	}()

	// Reader for client 2
	client2Reader := bufio.NewReader(client2)
	client2Received := make(chan string, 1)
	wg.Add(1)
	go func() {
		defer wg.Done()
		line, err := client2Reader.ReadString('\n')
		if err == nil {
			client2Received <- strings.TrimSpace(line)
		}
	}()

	// Test 1: Client 1 sends a message, Client 2 should receive it distorted
	sendMsg1 := "Hello from Client 1"
	expectedMsg1 := distortMessage(sendMsg1)

	_, err = client1.Write([]byte(sendMsg1 + "\n"))
	if err != nil {
		t.Fatalf("Client 1 failed to send message: %v", err)
	}

	select {
	case received := <-client2Received:
		if received != expectedMsg1 {
			t.Errorf("Client 2 received unexpected message. Got: %q, Want: %q", received, expectedMsg1)
		}
	case <-time.After(500 * time.Millisecond):
		t.Fatal("Client 2 did not receive message in time")
	}

	// Reset channels for next test
	client1Received = make(chan string, 1)
	client2Received = make(chan string, 1)

	// Re-add goroutines for reading, as they exit after one read
	wg.Add(1)
	go func() {
		defer wg.Done()
		line, err := client1Reader.ReadString('\n')
		if err == nil {
			client1Received <- strings.TrimSpace(line)
		}
	}()

	wg.Add(1)
	go func() {
		defer wg.Done()
		line, err := client2Reader.ReadString('\n')
		if err == nil {
			client2Received <- strings.TrimSpace(line)
		}
	}()

	// Test 2: Client 2 sends a message, Client 1 should receive it distorted
	sendMsg2 := "Greetings from Client 2"
	expectedMsg2 := distortMessage(sendMsg2)

	_, err = client2.Write([]byte(sendMsg2 + "\n"))
	if err != nil {
		t.Fatalf("Client 2 failed to send message: %v", err)
	}

	select {
	case received := <-client1Received:
		if received != expectedMsg2 {
			t.Errorf("Client 1 received unexpected message. Got: %q, Want: %q", received, expectedMsg2)
		}
	case <-time.After(500 * time.Millisecond):
		t.Fatal("Client 1 did not receive message in time")
	}

	// Ensure all reader goroutines have a chance to finish
	wg.Wait()

	// Test 3: Verify a client can disconnect gracefully
	client1.Close()
	time.Sleep(50 * time.Millisecond) // Give server time to process unregister

	// Try sending from client2 again, client1 should not receive
	sendMsg3 := "Client 1 is gone"
	expectedMsg3 := distortMessage(sendMsg3)

	// Clear client2's channel before sending
	select {
	case <-client2Received:
	default:
	}

	_, err = client2.Write([]byte(sendMsg3 + "\n"))
	if err != nil {
		t.Fatalf("Client 2 failed to send message after client 1 disconnect: %v", err)
	}

	// Client 2 should not receive its own message, but if it did, it would be here.
	// The server broadcasts to *other* clients.
	select {
	case received := <-client2Received:
		t.Errorf("Client 2 unexpectedly received its own message: %q", received)
	case <-time.After(100 * time.Millisecond):
		// This is the expected outcome: client 2 should not receive anything
	}

	// # Mock rationale: The `distortMessage` function is part of `main.go` and is designed
	// to be deterministic (always appending `~void echo~`). This ensures that test assertions
	// about the received message content are predictable and do not rely on random number generation
	// or external factors. Network interactions are confined to localhost, making tests offline.
}
