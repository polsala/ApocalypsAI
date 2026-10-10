package tests

import (
	"fmt"
	"log"
	"net"
	"nightly-beacon-broadcast/src/client"
	"nightly-beacon-broadcast/src/server"
	"os"
	"sync"
	"testing"
	"time"
)

// Mock rationale: This is an integration test, not a unit test. We are intentionally
// testing the interaction between the server and client over a real network stack.
// To ensure determinism and offline execution, we use `localhost` and dynamically
// assigned ephemeral ports. The server's received messages are captured via a Go channel
// rather than parsing log output, making the test outcome deterministic and robust.

func TestServerClientIntegration(t *testing.T) {
	// Use a random available port for the server to avoid conflicts
	serverPort := getFreePort(t)
	serverAddr := fmt.Sprintf("127.0.0.1:%d", serverPort)

	receivedMessages := make(chan string, 10) // Buffered channel for messages received by the server
	var wg sync.WaitGroup

	// Start the server in a goroutine
	serverConn, err := server.StartServer(fmt.Sprintf("%d", serverPort), receivedMessages)
	if err != nil {
		t.Fatalf("Failed to start server: %v", err)
	}
	defer func() {
		if serverConn != nil {
			serverConn.Close()
		}
	}()

	// Give server a moment to start listening
	time.Sleep(100 * time.Millisecond)

	testMessages := []string{
		"Alpha team, status report.",
		"Bravo team, proceed to sector 7.",
		"Charlie team, hold position.",
		"Delta team, rendezvous at waypoint Gamma.",
	}

	// Send messages from multiple clients concurrently
	for i, msg := range testMessages {
		wg.Add(1)
		go func(idx int, message string) {
			defer wg.Done()
			err := client.SendMessage(serverAddr, message)
			if err != nil {
				t.Errorf("Client %d failed to send message: %v", idx, err)
			}
		}(i, msg)
	}

	wg.Wait() // Wait for all clients to finish sending messages

	// Collect messages from the server's channel
	collectedMessages := make(map[string]bool)
	timeout := time.After(2 * time.Second) // Give some time for messages to be processed
	for len(collectedMessages) < len(testMessages) {
		select {
		case received := <-receivedMessages:
			// Expected format: "From 127.0.0.1:PORT: MESSAGE"
			// Extract the message content after the second colon and space
			msgContent := extractMessageContent(received)
			if msgContent == "" {
				t.Errorf("Failed to parse received message format: %s", received)
				continue
			}
			collectedMessages[msgContent] = true
		case <-timeout:
			t.Fatalf("Timeout waiting for all messages. Expected %d, got %d", len(testMessages), len(collectedMessages))
		}
	}

	// Verify all expected messages were received
	for _, expectedMsg := range testMessages {
		if !collectedMessages[expectedMsg] {
			t.Errorf("Expected message \"%s\" not received by server.", expectedMsg)
		}
	}
}

// getFreePort finds an available TCP port by listening on port 0, then returns it.
// This port can then be used for UDP, as port numbers are shared between TCP/UDP.
func getFreePort(t *testing.T) int {
	addr, err := net.ResolveTCPAddr("tcp", "localhost:0")
	if err != nil {
		t.Fatalf("Failed to resolve TCP address: %v", err)
	}
	l, err := net.ListenTCP("tcp", addr)
	if err != nil {
		t.Fatalf("Failed to listen on TCP port: %v", err)
	}
	defer l.Close()
	return l.Addr().(*net.TCPAddr).Port
}

// extractMessageContent parses the message string from the server's channel.
// Expected format: "From 127.0.0.1:PORT: MESSAGE"
func extractMessageContent(received string) string {
	firstColon := -1
	secondColon := -1
	for i, r := range received {
		if r == ':' {
			if firstColon == -1 {
				firstColon = i
			} else {
				secondColon = i
				break
			}
		}
	}

	if secondColon != -1 && secondColon+2 <= len(received) { // +2 for ": "
		return received[secondColon+2:]
	}
	return ""
}

// TestMain suppresses log output during tests to keep the console clean.
func TestMain(m *testing.M) {
	log.SetOutput(os.Stderr) // Redirect logs to stderr, or ioutil.Discard for complete silence
	exitCode := m.Run()
	os.Exit(exitCode)
}
