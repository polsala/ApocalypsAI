package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net"
	"os"
	"strconv"
	"sync"
	"testing"
	"time"
)

// Mock rationale: We are testing a network service. Instead of mocking the 'net' package,
// we run the actual server on a local ephemeral port and connect to it with real clients.
// This tests the full network stack interaction. The "mocking" is in controlling the
// server's lifecycle using a context and the client's behavior within the test, ensuring
// determinism by using timeouts and controlled message counts.

func TestChronoSyncBeacon(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Find an available port
	listener, err := net.Listen("tcp", "127.0.0.1:0") // Listen on a random available port
	if err != nil {
		t.Fatalf("Failed to find an available port: %v", err)
	}
	port := listener.Addr().(*net.TCPAddr).Port
	listener.Close() // Close the listener, runServer will open it

	interval := 100 * time.Millisecond // Faster interval for quicker test

	// Start the server in a goroutine
	var serverErr error
	var serverWg sync.WaitGroup
	serverWg.Add(1)
	go func() {
		defer serverWg.Done()
		// Temporarily discard log output to keep test output clean
		// # Mock rationale: Suppressing logs for cleaner test output.
		// # This doesn't affect the logic being tested.
		originalStderr := os.Stderr
		r, w, _ := os.Pipe()
		os.Stderr = w
		log.SetOutput(w)

		serverErr = runServer(ctx, port, interval)

		w.Close()
		os.Stderr = originalStderr
		log.SetOutput(originalStderr) // Restore log output
		io.Copy(io.Discard, r) // Read and discard anything written to the pipe
		r.Close()
	}()

	// Give the server a moment to start
	time.Sleep(50 * time.Millisecond)

	// Test client connection and message reception
	t.Run("SingleClientMessageReception", func(t *testing.T) {
		clientConn, err := net.DialTimeout("tcp", fmt.Sprintf("127.0.0.1:%d", port), 5*time.Second)
		if err != nil {
			t.Fatalf("Failed to connect to beacon server: %v", err)
		}
		defer clientConn.Close()

		decoder := json.NewDecoder(clientConn)
		receivedMessages := make(chan BeaconMessage, 5)

		go func() {
			for {
				var msg BeaconMessage
				clientConn.SetReadDeadline(time.Now().Add(interval + 50*time.Millisecond))
				err := decoder.Decode(&msg)
				if err != nil {
					if err == io.EOF {
						t.Log("Client connection closed by server.")
					} else if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
						t.Log("Client read timeout, server might have stopped or no messages.")
					} else {
						t.Errorf("Error decoding message: %v", err)
					}
					return
				}
				receivedMessages <- msg
			}
		}()

		expectedMessages := 3
		for i := 0; i < expectedMessages; i++ {
			select {
			case msg := <-receivedMessages:
				if msg.Source != "ApocalypsAI Chrono-Sync Beacon" {
					t.Errorf("Expected source 'ApocalypsAI Chrono-Sync Beacon', got '%s'", msg.Source)
				}
				parsedTime, err := time.Parse(time.RFC3339Nano, msg.Timestamp)
				if err != nil {
					t.Errorf("Failed to parse timestamp '%s': %v", msg.Timestamp, err)
				}
				// Check if the timestamp is reasonably recent
				if time.Since(parsedTime) > 2*time.Second || time.Since(parsedTime) < -2*time.Second {
					t.Errorf("Timestamp %s is not recent enough (diff: %v)", msg.Timestamp, time.Since(parsedTime))
				}
				t.Logf("Client received message %d: %s", i+1, msg.Timestamp)
			case <-time.After(interval*time.Duration(expectedMessages) + 1*time.Second):
				t.Fatalf("Timed out waiting for message %d from beacon server", i+1)
			}
		}
	})

	// Test multiple clients concurrently
		t.Run("MultipleClientConnections", func(t *testing.T) {
		numClients := 5
		var clientWg sync.WaitGroup
		clientWg.Add(numClients)
		for i := 0; i < numClients; i++ {
			go func(clientID int) {
				defer clientWg.Done()
				conn, err := net.DialTimeout("tcp", fmt.Sprintf("127.0.0.1:%d", port), 5*time.Second)
				if err != nil {
					t.Errorf("Client %d: Failed to connect: %v", clientID, err)
					return
				}
				defer conn.Close()

				decoder := json.NewDecoder(conn)
				var msg BeaconMessage
				conn.SetReadDeadline(time.Now().Add(interval + 50*time.Millisecond))
				if err := decoder.Decode(&msg); err != nil {
					t.Errorf("Client %d: Error decoding message: %v", clientID, err)
					return
				}
				t.Logf("Client %d received first message: %s", clientID, msg.Timestamp)
			}(i)
		}
		clientWg.Wait()
	})

	// Clean up: signal server to stop
	cancel()
	serverWg.Wait() // Wait for the server goroutine to finish
	if serverErr != nil {
		t.Errorf("Server exited with error: %v", serverErr)
	}
}
