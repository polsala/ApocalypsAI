package main

import (
	"bytes"
	"log"
	"net"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// TestEncodeDecodeBeacon tests the serialization and deserialization of BeaconMessage.
func TestEncodeDecodeBeacon(t *testing.T) {
	originalMsg := BeaconMessage{
		ID:        "TestNode",
		Timestamp: time.Now().UnixNano(),
		Payload:   "Hello World!",
	}

	encoded, err := encodeBeacon(originalMsg)
	if err != nil {
		t.Fatalf("encodeBeacon failed: %v", err)
	}

	decodedMsg, err := decodeBeacon(encoded)
	if err != nil {
		t.Fatalf("decodeBeacon failed: %v", err)
	}

	if originalMsg.ID != decodedMsg.ID {
		t.Errorf("Expected ID %s, got %s", originalMsg.ID, decodedMsg.ID)
	}
	if originalMsg.Timestamp != decodedMsg.Timestamp {
		t.Errorf("Expected Timestamp %d, got %d", originalMsg.Timestamp, decodedMsg.Timestamp)
	}
	if originalMsg.Payload != decodedMsg.Payload {
		t.Errorf("Expected Payload %s, got %s", originalMsg.Payload, decodedMsg.Payload)
	}

	// Test with empty payload
	emptyPayloadMsg := BeaconMessage{
		ID:        "Empty",
		Timestamp: time.Now().UnixNano(),
		Payload:   "",
	}
	encodedEmpty, err := encodeBeacon(emptyPayloadMsg)
	if err != nil {
		t.Fatalf("encodeBeacon with empty payload failed: %v", err)
	}
	decodedEmpty, err := decodeBeacon(encodedEmpty)
	if err != nil {
		t.Fatalf("decodeBeacon with empty payload failed: %v", err)
	}
	if decodedEmpty.Payload != "" {
		t.Errorf("Expected empty payload, got %s", decodedEmpty.Payload)
	}
}

// TestDecodeBeaconInvalidData tests decoding with invalid data.
func TestDecodeBeaconInvalidData(t *testing.T) {
	invalidData := []byte("this is not a gob encoded message")
	_, err := decodeBeacon(invalidData)
	if err == nil {
		t.Error("Expected an error for invalid data, got nil")
	}
	// # Mock rationale: Testing error handling for malformed network data without actual network errors.
}

// TestBeaconSenderAndListenerIntegration tests sender and listener in-process.
func TestBeaconSenderAndListenerIntegration(t *testing.T) {
	// Use a free UDP port for testing
	listenerAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("Failed to resolve UDP address: %v", err)
	}
	conn, err := net.ListenUDP("udp", listenerAddr)
	if err != nil {
		t.Fatalf("Failed to listen on UDP: %v", err)
	}
	defer conn.Close()

	actualAddr := conn.LocalAddr().String()

	var wg sync.WaitGroup
	wg.Add(2) // One for sender, one for listener

	// Capture log output to verify received messages
	var logBuf bytes.Buffer
	log.SetOutput(&logBuf)
	defer func() { log.SetOutput(os.Stderr) }() // Restore default output

	// Start listener in a goroutine
	go func() {
		defer wg.Done()
		startBeaconListener(actualAddr)
	}()

	// Give listener a moment to start and join multicast if applicable
	time.Sleep(100 * time.Millisecond)

	// Start sender in a goroutine
	senderID := "TestSender"
	senderPayload := "TestPayload"
	senderInterval := 50 * time.Millisecond
	go func() {
		defer wg.Done()
		startBeaconSender(actualAddr, senderInterval, senderID, senderPayload)
	}()

	// Wait for a few beacons to be sent and received
	time.Sleep(200 * time.Millisecond)

	// Stop sender and listener (by closing the connection)
	conn.Close()

	// Wait for goroutines to finish processing the closed connection error
	wg.Wait()

	// Check log output
	output := logBuf.String()
	if !strings.Contains(output, fmt.Sprintf("Received beacon from %s (Timestamp: ", senderID)) {
		t.Errorf("Expected log output to contain received beacon from %s, got:\n%s", senderID, output)
	}
	if !strings.Contains(output, senderPayload) {
		t.Errorf("Expected log output to contain payload '%s', got:\n%s", senderPayload, output)
	}
	// # Mock rationale: This test simulates network communication entirely within the test process
	// # using ephemeral UDP ports, ensuring determinism and avoiding external dependencies.
	// # It verifies the end-to-end flow of sending and receiving beacons.
}
