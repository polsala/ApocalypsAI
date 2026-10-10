package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// Helper to capture log output for testing
type LogCapture struct {
	mu      sync.Mutex
	builder strings.Builder
}

func (lc *LogCapture) Write(p []byte) (n int, err error) {
	lc.mu.Lock()
	defer lc.mu.Unlock()
	return lc.builder.Write(p)
}

func (lc *LogCapture) String() string {
	lc.mu.Lock()
	defer lc.mu.Unlock()
	return lc.builder.String()
}

func TestListenForEchoes(t *testing.T) {
	// Mock rationale: Using net.ListenPacket and net.DialUDP with local addresses
	// allows for deterministic, offline testing of network communication without
	// relying on external network resources.
	
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Use a random available port for the listener
	listenerAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("Failed to resolve UDP address: %v", err)
	}
	conn, err := net.ListenUDP("udp", listenerAddr)
	if err != nil {
		t.Fatalf("Failed to listen UDP: %v", err)
	}
	defer conn.Close()
	listenPort := conn.LocalAddr().(*net.UDPAddr).Port
	conn.Close() // Close the temporary listener, listenForEchoes will open its own

	logCapture := &LogCapture{}
	log.SetOutput(logCapture)
	defer log.SetOutput(os.Stderr) // Restore default stderr after test

	go listenForEchoes(ctx, listenPort)

	// Give the listener a moment to start
	time.Sleep(100 * time.Millisecond)

	// Send a test message
	testMessage := "Hello from the void!"
	senderAddr := fmt.Sprintf("127.0.0.1:%d", listenPort)
	senderConn, err := net.Dial("udp", senderAddr)
	if err != nil {
		t.Fatalf("Failed to dial sender: %v", err)
	}
	defer senderConn.Close()

	_, err = senderConn.Write([]byte(testMessage))
	if err != nil {
		t.Fatalf("Failed to send message: %v", err)
	}

	// Wait for the message to be processed and logged
	time.Sleep(200 * time.Millisecond)

	logOutput := logCapture.String()
	if !strings.Contains(logOutput, fmt.Sprintf("Received cosmic echo from 127.0.0.1:%d: \"%s\"", senderConn.LocalAddr().(*net.UDPAddr).Port, testMessage)) {
		t.Errorf("Expected log output to contain received message, got:\n%s", logOutput)
	}
}

func TestSendWhispers(t *testing.T) {
	// Mock rationale: Similar to TestListenForEchoes, using local UDP addresses
	// allows for testing the sender's ability to send messages and the receiver's
	// ability to capture them, all within a controlled, offline environment.
	
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Use a random available port for the target listener
	targetAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("Failed to resolve UDP address: %v", err)
	}
	targetConn, err := net.ListenUDP("udp", targetAddr)
	if err != nil {
		t.Fatalf("Failed to listen UDP for target: %v", err)
	}
	defer targetConn.Close()
	targetPort := targetConn.LocalAddr().(*net.UDPAddr).Port
	targetAddress := fmt.Sprintf("127.0.0.1:%d", targetPort)

	logCapture := &LogCapture{}
	log.SetOutput(logCapture)
	defer log.SetOutput(os.Stderr) // Restore default stderr after test

	testMessage := "A test whisper..."
	testInterval := 100 * time.Millisecond // Short interval for testing

	go sendWhispers(ctx, targetAddress, testInterval, testMessage)

	// Give the sender a moment to send a few whispers
	time.Sleep(3 * testInterval) // Wait for at least 2-3 whispers

	// Check if the target listener received messages
	buffer := make([]byte, 1024)
	receivedCount := 0
	for i := 0; i < 3; i++ { // Try to read a few messages
		targetConn.SetReadDeadline(time.Now().Add(testInterval / 2)) // Short deadline
		n, _, err := targetConn.ReadFrom(buffer)
		if err != nil {
			if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
				continue // No message yet, try again
			}
			t.Logf("Error reading from target: %v", err) // Log, but don't fail immediately
			continue
		}
		if string(buffer[:n]) == testMessage {
			receivedCount++
		}
	}

	if receivedCount < 2 { // Expect at least 2 whispers in 3 intervals
		t.Errorf("Expected to receive at least 2 whispers, got %d. Log:\n%s", receivedCount, logCapture.String())
	}

	logOutput := logCapture.String()
	if !strings.Contains(logOutput, fmt.Sprintf("Sent cosmic whisper to %s: \"%s\"", targetAddress, testMessage)) {
		t.Errorf("Expected log output to contain sent message, got:\n%s", logOutput)
	}
}

func TestLoadConfigFromEnv(t *testing.T) {
	// Mock rationale: Environment variables are a standard way to configure applications.
	// Setting and unsetting them directly in tests provides a deterministic way to
	// verify configuration loading logic without external dependencies.
	
	os.Setenv("LISTEN_PORT", "9000")
	os.Setenv("ECHO_TARGET", "192.168.1.1:1234")
	os.Setenv("WHISPER_INTERVAL_SECONDS", "5")
	os.Setenv("WHISPER_MESSAGE", "Test message from env")

	cfg := LoadConfigFromEnv()

	if cfg.ListenPort != 9000 {
		t.Errorf("Expected ListenPort 9000, got %d", cfg.ListenPort)
	}
	if cfg.EchoTarget != "192.168.1.1:1234" {
		t.Errorf("Expected EchoTarget 192.168.1.1:1234, got %s", cfg.EchoTarget)
	}
	if cfg.WhisperInterval != 5*time.Second {
		t.Errorf("Expected WhisperInterval 5s, got %s", cfg.WhisperInterval)
	}
	if cfg.WhisperMessage != "Test message from env" {
		t.Errorf("Expected WhisperMessage 'Test message from env', got '%s'", cfg.WhisperMessage)
	}

	// Clean up environment variables
	os.Unsetenv("LISTEN_PORT")
	os.Unsetenv("ECHO_TARGET")
	os.Unsetenv("WHISPER_INTERVAL_SECONDS")
	os.Unsetenv("WHISPER_MESSAGE")

	// Test defaults
	cfg = LoadConfigFromEnv()
	defaultCfg := NewConfig()
	if cfg.ListenPort != defaultCfg.ListenPort {
		t.Errorf("Expected default ListenPort %d, got %d", defaultCfg.ListenPort, cfg.ListenPort)
	}
	if cfg.EchoTarget != defaultCfg.EchoTarget {
		t.Errorf("Expected default EchoTarget '%s', got '%s'", defaultCfg.EchoTarget, cfg.EchoTarget)
	}
	if cfg.WhisperInterval != defaultCfg.WhisperInterval {
		t.Errorf("Expected default WhisperInterval %s, got %s", defaultCfg.WhisperInterval, cfg.WhisperInterval)
	}
	if cfg.WhisperMessage != defaultCfg.WhisperMessage {
		t.Errorf("Expected default WhisperMessage '%s', got '%s'", defaultCfg.WhisperMessage, cfg.WhisperMessage)
	}
}
