package main

import (
	"fmt"
	"io"
	"log"
	"net"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock rationale: Instead of mocking net.Conn directly, we're spinning up actual, lightweight TCP servers
// on localhost within the test. This provides a more realistic integration test while remaining
// deterministic and offline. We control the environment (ports, peers) and observe internal state (received messages).

// TestBeacon represents a testable instance of the gossip beacon.
type TestBeacon struct {
	Port          string
	Peers         []string
	ReceivedMsgs  []string
	mu            sync.Mutex
	listener      net.Listener
	serverStarted chan struct{}
}

// NewTestBeacon creates a new test beacon instance.
func NewTestBeacon(port string, peers []string) *TestBeacon {
	return &TestBeacon{
		Port:          port,
		Peers:         peers,
		ReceivedMsgs:  []string{},
		serverStarted: make(chan struct{}),
	}
}

// Start runs the beacon server in a goroutine.
func (tb *TestBeacon) Start() {
	listener, err := net.Listen("tcp", ":"+tb.Port)
	if err != nil {
		log.Fatalf("Test beacon failed to listen on port %s: %v", tb.Port, err)
	}
	tb.listener = listener

	close(tb.serverStarted) // Signal that the server has started listening

	go func() {
		defer tb.listener.Close()
		for {
			conn, err := tb.listener.Accept()
			if err != nil {
				if strings.Contains(err.Error(), "use of closed network connection") {
					return // Listener was closed, exit goroutine
				}
				log.Printf("Test beacon %s: Error accepting connection: %v", tb.Port, err)
				continue
			}
			go tb.handleTestConnection(conn)
		}
	}()
}

// Stop closes the beacon's listener.
func (tb *TestBeacon) Stop() {
	if tb.listener != nil {
		_ = tb.listener.Close()
	}
}

// handleTestConnection processes incoming messages for the test beacon.
func (tb *TestBeacon) handleTestConnection(conn net.Conn) {
	defer conn.Close()

	buf := make([]byte, 1024)
	n, err := conn.Read(buf)
	if err != nil && err != io.EOF {
		log.Printf("Test beacon %s: Error reading from connection: %v", tb.Port, err)
		return
	}

	message := strings.TrimSpace(string(buf[:n]))
	if message == "" {
		return
	}

	tb.mu.Lock()
	tb.ReceivedMsgs = append(tb.ReceivedMsgs, message)
	tb.mu.Unlock()

	// Simulate relaying to peers, but use the main's relayMessage function
	// This ensures we're testing the actual relay logic.
	if len(tb.Peers) > 0 {
		var wg sync.WaitGroup
		for _, peerAddr := range tb.Peers {
			wg.Add(1)
			go func(addr, msg string) {
				defer wg.Done()
				relayMessage(addr, msg)
			}(peerAddr, message)
		}
		wg.Wait()
	}
}

// SendMessage sends a message to this beacon.
func (tb *TestBeacon) SendMessage(message string) error {
	conn, err := net.DialTimeout("tcp", "localhost:"+tb.Port, 2*time.Second)
	if err != nil {
		return fmt.Errorf("failed to connect to test beacon %s: %w", tb.Port, err)
	}
	defer conn.Close()

	_, err = fmt.Fprintf(conn, "%s\n", message)
	if err != nil {
		return fmt.Errorf("failed to send message to test beacon %s: %w", tb.Port, err)
	}
	return nil
}

func TestGossipRelay(t *testing.T) {
	log.SetOutput(io.Discard) // Suppress server logs during test for cleaner output

	// Define ports for our test network
	portA := "8081"
	portB := "8082"
	portC := "8083"

	// Create test beacons with their respective peers
	beaconA := NewTestBeacon(portA, []string{"localhost:" + portB, "localhost:" + portC})
	beaconB := NewTestBeacon(portB, []string{"localhost:" + portA, "localhost:" + portC})
	beaconC := NewTestBeacon(portC, []string{"localhost:" + portA, "localhost:" + portB})

	// Start all beacons
	beacons := []*TestBeacon{beaconA, beaconB, beaconC}
	for _, b := range beacons {
		b.Start()
		<-b.serverStarted // Wait for the server to actually start listening
	}

	defer func() {
		for _, b := range beacons {
			b.Stop()
		}
	}()

	// Give servers a moment to fully initialize
	time.Sleep(100 * time.Millisecond)

	// Test 1: Message sent to A should reach B and C
	message1 := "The supplies are at Sector 7!"
	if err := beaconA.SendMessage(message1); err != nil {
		t.Fatalf("Failed to send message to beacon A: %v", err)
	}

	// Wait for message to propagate
	time.Sleep(500 * time.Millisecond)

	// Verify message reception
	expected := message1

	beaconB.mu.Lock()
	if !contains(beaconB.ReceivedMsgs, expected) {
		t.Errorf("Beacon B did not receive message: \"%s\" (received: %v)", expected, beaconB.ReceivedMsgs)
	}
	beaconB.mu.Unlock()

	beaconC.mu.Lock()
	if !contains(beaconC.ReceivedMsgs, expected) {
		t.Errorf("Beacon C did not receive message: \"%s\" (received: %v)", expected, beaconC.ReceivedMsgs)
	}
	beaconC.mu.Unlock()

	// Test 2: Message sent to B should reach A and C
	message2 := "Water purification unit is online!"
	if err := beaconB.SendMessage(message2); err != nil {
		t.Fatalf("Failed to send message to beacon B: %v", err)
	}

	// Wait for message to propagate
	time.Sleep(500 * time.Millisecond)

	// Verify message reception
	expected = message2

	beaconA.mu.Lock()
	if !contains(beaconA.ReceivedMsgs, expected) {
		t.Errorf("Beacon A did not receive message: \"%s\" (received: %v)", expected, beaconA.ReceivedMsgs)
	}
	beaconA.mu.Unlock()

	beaconC.mu.Lock()
	if !contains(beaconC.ReceivedMsgs, expected) {
		t.Errorf("Beacon C did not receive message: \"%s\" (received: %v)", expected, beaconC.ReceivedMsgs)
	}
	beaconC.mu.Unlock()

	// Test 3: Ensure no duplicate messages if sent multiple times to the same beacon
	message3 := "Ration drop coordinates: 34.0522 N, 118.2437 W"
	if err := beaconA.SendMessage(message3); err != nil {
		t.Fatalf("Failed to send message to beacon A: %v", err)
	}
	if err := beaconA.SendMessage(message3); err != nil {
		t.Fatalf("Failed to send duplicate message to beacon A: %v", err)
	}

	time.Sleep(500 * time.Millisecond)

	beaconB.mu.Lock()
	count := countOccurrences(beaconB.ReceivedMsgs, message3)
	if count != 1 {
		t.Errorf("Beacon B received message \"%s\" %d times, expected 1", message3, count)
	}
	beaconB.mu.Unlock()

	beaconC.mu.Lock()
	count = countOccurrences(beaconC.ReceivedMsgs, message3)
	if count != 1 {
		t.Errorf("Beacon C received message \"%s\" %d times, expected 1", message3, count)
	}
	beaconC.mu.Unlock()
}

// Helper function to check if a slice contains a string.
func contains(slice []string, item string) bool {
	for _, a := range slice {
		if a == item {
			return true
		}
	}
	return false
}

// Helper function to count occurrences of a string in a slice.
func countOccurrences(slice []string, item string) int {
	count := 0
	for _, a := range slice {
		if a == item {
			count++
		}
	}
	return count
}
