package main

import (
	"net"
	"testing"
	"time"
)

// Mock rationale: Simulate network behavior without actual network calls.
func TestBroadcastAndListen(t *testing.T) {
	group := "224.0.0.1:9998"
	message := "Test message from the void"

	addr, err := net.ResolveUDPAddr("udp", group)
	if err != nil {
		t.Fatalf("Failed to resolve address: %v", err)
	}

	// Start listener in background
	messages := make(chan string, 1)
	go func() {
		conn, err := net.ListenMulticastUDP("udp", nil, addr)
		if err != nil {
			t.Errorf("Failed to listen: %v", err)
			return
		}
		defer conn.Close()

		buffer := make([]byte, 1024)
		conn.SetReadDeadline(time.Now().Add(2 * time.Second))
		n, _, err := conn.ReadFromUDP(buffer)
		if err != nil {
			return
		}
		messages <- string(buffer[:n])
	}()

	// Give listener time to start
	time.Sleep(100 * time.Millisecond)

	// Broadcast message
	broadcastMessage(message, addr)

	// Wait for message
	select {
	case received := <-messages:
		if received != message {
			t.Errorf("Expected %q, got %q", message, received)
		}
	case <-time.After(3 * time.Second):
		t.Error("Timeout waiting for message")
	}
}
