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

// Helper to capture stdout and stderr from a function that takes a done channel.
// This is crucial for testing concurrent services that print output.
func captureOutput(f func(port int, key string, done <-chan struct{}), port int, key string, done <-chan struct{}) string {
	oldStdout := os.Stdout
	oldStderr := os.Stderr
	rOut, wOut, _ := os.Pipe()
	rErr, wErr, _ := os.Pipe()
	os.Stdout = wOut
	os.Stderr = wErr
	log.SetOutput(wErr) // Redirect log output too

	var wg sync.WaitGroup
	wg.Add(2)

	var stdoutBuf, stderrBuf bytes.Buffer
	go func() {
		defer wg.Done()
		io.Copy(&stdoutBuf, rOut)
	}()
	go func() {
		defer wg.Done()
		io.Copy(&stderrBuf, rErr)
	}()

	f(port, key, done)

	wOut.Close()
	wErr.Close()
	wg.Wait()

	os.Stdout = oldStdout
	os.Stderr = oldStderr
	log.SetOutput(oldStderr) // Restore log output
	return stdoutBuf.String() + stderrBuf.String()
}

// Helper to capture stdout and stderr for startBroadcaster, which has more arguments.
func captureBroadcasterOutput(f func(port int, interval time.Duration, key string, targets []string, done <-chan struct{}), port int, interval time.Duration, key string, targets []string, done <-chan struct{}) string {
	oldStdout := os.Stdout
	oldStderr := os.Stderr
	rOut, wOut, _ := os.Pipe()
	rErr, wErr, _ := os.Pipe()
	os.Stdout = wOut
	os.Stderr = wErr
	log.SetOutput(wErr) // Redirect log output too

	var wg sync.WaitGroup
	wg.Add(2)

	var stdoutBuf, stderrBuf bytes.Buffer
	go func() {
		defer wg.Done()
		io.Copy(&stdoutBuf, rOut)
	}()
	go func() {
		defer wg.Done()
		io.Copy(&stderrBuf, rErr)
	}()

	f(port, interval, key, targets, done)

	wOut.Close()
	wErr.Close()
	wg.Wait()

	os.Stdout = oldStdout
	os.Stderr = oldStderr
	log.SetOutput(oldStderr) // Restore log output
	return stdoutBuf.String() + stderrBuf.String()
}

// TestXORCipher verifies the basic XOR encryption/decryption logic.
func TestXORCipher(t *testing.T) {
	key := "testkey"
	original := []byte("Hello, World!")

	encrypted := xorCipher(original, key)
	if bytes.Equal(original, encrypted) {
		t.Errorf("Encryption failed: original and encrypted are identical")
	}

	decrypted := xorCipher(encrypted, key)
	if !bytes.Equal(original, decrypted) {
		t.Errorf("Decryption failed: expected %s, got %s", string(original), string(decrypted))
	}

	// Test with empty key
	emptyKeyEncrypted := xorCipher(original, "")
	if !bytes.Equal(original, emptyKeyEncrypted) {
		t.Errorf("Empty key encryption should return original data")
	}

	// Test with different key (should not decrypt correctly)
	differentKey := "wrongkey"
	wronglyDecrypted := xorCipher(encrypted, differentKey)
	if bytes.Equal(original, wronglyDecrypted) {
		t.Errorf("Decryption with wrong key unexpectedly succeeded")
	}
}

// TestListener verifies that the listener can receive and decrypt a message.
func TestListener(t *testing.T) {
	// Mock rationale: We need to simulate network communication without actual external dependencies.
	// We achieve this by setting up a local UDP sender within the test itself.
	// This ensures determinism and offline execution.

	listenerPort := 8081 // Use a distinct port for the listener in test
	done := make(chan struct{})
	var output string
	var wg sync.WaitGroup
	wg.Add(1)

	go func() {
		defer wg.Done()
		output = captureOutput(startListener, listenerPort, defaultKey, done)
	}()

	// Give listener a moment to start and bind to the port
	time.Sleep(100 * time.Millisecond)

	// Send a message to the listener
	conn, err := net.DialUDP("udp", nil, &net.UDPAddr{IP: net.ParseIP("127.0.0.1"), Port: listenerPort})
	if err != nil {
		t.Fatalf("Failed to dial UDP: %v", err)
	}
	defer conn.Close()

	testMessage := fmt.Sprintf("Beacon heartbeat from test at %s", time.Now().Format(time.RFC3339Nano))
	encryptedMessage := xorCipher([]byte(testMessage), defaultKey)
	_, err = conn.Write(encryptedMessage)
	if err != nil {
		t.Fatalf("Failed to send message: %v", err)
	}

	// Wait for the message to be processed and then signal listener to stop
	time.Sleep(200 * time.Millisecond) // Give time for message processing
	close(done)                        // Signal listener to stop
	wg.Wait()                          // Wait for the goroutine to finish capturing output

	// Verify output contains expected logs and decrypted message
	if !strings.Contains(output, "Received encrypted beacon:") || !strings.Contains(output, "Decrypted: "+testMessage) {
		t.Errorf("Listener output incorrect. Expected 'Received encrypted beacon:' and 'Decrypted: %s'. Got:\n%s", testMessage, output)
	}
	if !strings.Contains(output, fmt.Sprintf("Starting Beacon Listener on port %d", listenerPort)) {
		t.Errorf("Listener startup log missing. Got:\n%s", output)
	}
	if !strings.Contains(output, "Listener: Shutting down.") {
		t.Errorf("Listener shutdown log missing. Got:\n%s", output)
	}
}

// TestBroadcaster verifies that the broadcaster sends an encrypted message to a target.
func TestBroadcaster(t *testing.T) {
	// Mock rationale: We need to simulate network communication without actual external dependencies.
	// We achieve this by setting up a local UDP listener within the test itself.
	// This ensures determinism and offline execution.

	broadcasterPort := 8082 // Use a distinct port for the broadcaster in test
	listenerPort := 8083    // Use a distinct port for the test listener

	// Setup a listener to capture the broadcast
	addr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("127.0.0.1:%d", listenerPort))
	if err != nil {
		t.Fatalf("Failed to resolve UDP address: %v", err)
	}
	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		t.Fatalf("Failed to listen on UDP: %v", err)
	}
	defer conn.Close()

	targetAddr := fmt.Sprintf("127.0.0.1:%d", listenerPort)

	done := make(chan struct{})
	var broadcasterOutput string
	var wg sync.WaitGroup
	wg.Add(1)

	go func() {
		defer wg.Done()
		broadcasterOutput = captureBroadcasterOutput(startBroadcaster, broadcasterPort, 100*time.Millisecond, defaultKey, []string{targetAddr}, done)
	}()

	// Wait for a message to be sent and received
	buffer := make([]byte, 1024)
	conn.SetReadDeadline(time.Now().Add(500 * time.Millisecond)) // Timeout for receiving message
	n, _, err := conn.ReadFromUDP(buffer)
	if err != nil {
		t.Fatalf("Failed to receive message from broadcaster: %v", err)
	}

	received := buffer[:n]
	decrypted := xorCipher(received, defaultKey)

	// Assert content (should contain timestamp and hostname)
	if !bytes.Contains(decrypted, []byte("Beacon heartbeat")) {
		t.Errorf("Expected 'Beacon heartbeat' in message, got %s", string(decrypted))
	}

	// Signal broadcaster to stop and wait for its goroutine to finish
	close(done)
	wg.Wait()

	// Verify broadcaster output logs
	if !strings.Contains(broadcasterOutput, fmt.Sprintf("Starting Beacon Broadcaster on port %d", broadcasterPort)) {
		t.Errorf("Broadcaster startup log missing. Got:\n%s", broadcasterOutput)
	}
	if !strings.Contains(broadcasterOutput, fmt.Sprintf("Broadcaster: Sent beacon to %s", targetAddr)) {
		t.Errorf("Broadcaster sent log missing. Got:\n%s", broadcasterOutput)
	}
	if !strings.Contains(broadcasterOutput, "Broadcaster: Shutting down.") {
		t.Errorf("Broadcaster shutdown log missing. Got:\n%s", broadcasterOutput)
	}
}
