package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net"
	"sync"
	"testing"
	"time"
)

// TestXOREncryption tests the xorEncrypt and xorDecrypt functions.
func TestXOREncryption(t *testing.T) {
	original := []byte("hello world")
	key := byte(0xAA)

	encrypted := xorEncrypt(original, key)
	if bytes.Equal(original, encrypted) {
		t.Errorf("Encryption failed: original and encrypted are identical")
	}

	decrypted := xorDecrypt(encrypted, key)
	if !bytes.Equal(original, decrypted) {
		t.Errorf("Decryption failed: expected %s, got %s", original, decrypted)
	}

	// Test with empty slice
	empty := []byte{}
	encEmpty := xorEncrypt(empty, key)
	if len(encEmpty) != 0 {
		t.Errorf("Empty slice encryption failed: expected empty, got %v", encEmpty)
	}
	decEmpty := xorDecrypt(encEmpty, key)
	if len(decEmpty) != 0 {
		t.Errorf("Empty slice decryption failed: expected empty, got %v", decEmpty)
	}
}

// TestBeaconMessageSerialization tests JSON marshalling and unmarshalling of BeaconMessage.
func TestBeaconMessageSerialization(t *testing.T) {
	msg := BeaconMessage{
		SenderID:  "TestSender",
		Message:   "Test message content",
		Timestamp: 1678886400, // Example timestamp
	}

	// Marshal
	jsonMsg, err := json.Marshal(msg)
	if err != nil {
		t.Fatalf("Failed to marshal BeaconMessage: %v", err)
	}

	// Unmarshal
	var unmarshalledMsg BeaconMessage
	err = json.Unmarshal(jsonMsg, &unmarshalledMsg)
	if err != nil {
		t.Fatalf("Failed to unmarshal BeaconMessage: %v", err)
	}

	// Verify
	if unmarshalledMsg.SenderID != msg.SenderID {
		t.Errorf("SenderID mismatch: expected %s, got %s", msg.SenderID, unmarshalledMsg.SenderID)
	}
	if unmarshalledMsg.Message != msg.Message {
		t.Errorf("Message mismatch: expected %s, got %s", msg.Message, unmarshalledMsg.Message)
	}
	if unmarshalledMsg.Timestamp != msg.Timestamp {
		t.Errorf("Timestamp mismatch: expected %d, got %d", msg.Timestamp, unmarshalledMsg.Timestamp)
	}
}

// TestEndToEndMessageProcessing simulates sending and receiving a message locally.
func TestEndToEndMessageProcessing(t *testing.T) {
	// Mock rationale: This test uses local UDP sockets (127.0.0.1) to simulate network communication
	// without relying on external network resources or actual broadcast capabilities.
	// This ensures determinism and offline execution.

	testPort := 9000 // Use a distinct port for testing
	testSenderID := "TestBeacon"
	testMessageContent := "Whisper in the dark."
	testTimestamp := time.Now().Unix()

	// 1. Setup a UDP listener
	listenAddr, err := net.ResolveUDPAddr("udp", fmt.Sprintf(":%d", testPort))
	if err != nil {
		t.Fatalf("Failed to resolve listen address: %v", err)
	}
	conn, err := net.ListenUDP("udp", listenAddr)
	if err != nil {
		t.Fatalf("Failed to listen on UDP port %d: %v", testPort, err)
	}
	defer conn.Close()

	receivedMsgChan := make(chan BeaconMessage, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	// Start a goroutine to handle incoming messages, similar to handleIncomingMessages
	go func() {
		defer wg.Done()
		buffer := make([]byte, 1024)
		conn.SetReadDeadline(time.Now().Add(5 * time.Second)) // Set a deadline for the listener
		n, _, err := conn.ReadFromUDP(buffer)
		if err != nil {
			if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
				t.Log("Listener timed out, no message received.")
				return
			}
			t.Errorf("Error reading from UDP in test listener: %v", err)
			return
		}

		decryptedData := xorDecrypt(buffer[:n], xorKey)
		var msg BeaconMessage
		if err := json.Unmarshal(decryptedData, &msg); err != nil {
			t.Errorf("Error unmarshalling received message: %v", err)
			return
		}
		receivedMsgChan <- msg
	}()

	// 2. Prepare and send a message
	originalMsg := BeaconMessage{
		SenderID:  testSenderID,
		Message:   testMessageContent,
		Timestamp: testTimestamp,
	}
	jsonMsg, err := json.Marshal(originalMsg)
	if err != nil {
		t.Fatalf("Failed to marshal original message: %v", err)
	}
	encryptedMsg := xorEncrypt(jsonMsg, xorKey)

	// Send the message to the listener
	sendAddr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("127.0.0.1:%d", testPort))
	if err != nil {
		t.Fatalf("Failed to resolve send address: %v", err)
	}
	senderConn, err := net.DialUDP("udp", nil, sendAddr)
	if err != nil {
		t.Fatalf("Failed to dial UDP for sending: %v", err)
	}
	defer senderConn.Close()

	_, err = senderConn.Write(encryptedMsg)
	if err != nil {
		t.Fatalf("Failed to send UDP message: %v", err)
	}

	// 3. Wait for the message to be received and verify
	select {
	case received := <-receivedMsgChan:
		if received.SenderID != originalMsg.SenderID {
			t.Errorf("Received SenderID mismatch: expected %s, got %s", originalMsg.SenderID, received.SenderID)
		}
		if received.Message != originalMsg.Message {
			t.Errorf("Received Message mismatch: expected %s, got %s", originalMsg.Message, received.Message)
		}
		// Allow for slight timestamp differences due to test execution time
		if received.Timestamp < originalMsg.Timestamp || received.Timestamp > originalMsg.Timestamp+2 {
			t.Errorf("Received Timestamp mismatch: expected around %d, got %d", originalMsg.Timestamp, received.Timestamp)
		}
	case <-time.After(6 * time.Second): // Give listener enough time to receive
		t.Fatal("Test timed out waiting for message reception.")
	}

	// Ensure the goroutine finishes cleanly
	conn.Close() // Close the listener to unblock ReadFromUDP
	wg.Wait()
}
