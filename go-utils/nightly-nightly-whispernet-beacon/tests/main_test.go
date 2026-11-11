package main

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"
	"time"
)

// TestNewBeacon ensures a Beacon can be initialized correctly.
func TestNewBeacon(t *testing.T) {
	id := "test-beacon"
	port := 9000
	peers := []string{"http://peer1:8080", "http://peer2:8080"}

	beacon := NewBeacon(id, port, peers)

	if beacon.ID != id {
		t.Errorf("Expected ID %s, got %s", id, beacon.ID)
	}
	if beacon.Port != port {
		t.Errorf("Expected Port %d, got %d", port, beacon.Port)
	}
	if len(beacon.Peers) != len(peers) {
		t.Errorf("Expected %d peers, got %d", len(peers), len(beacon.Peers))
	}
	if beacon.Messages == nil {
		t.Error("Messages channel should be initialized")
	}
	if beacon.Client == nil {
		t.Error("HTTP client should be initialized")
	}
	if beacon.Server == nil {
		t.Error("HTTP server should be initialized")
	}
}

// TestHandleWhisper ensures the HTTP handler correctly processes incoming whispers.
func TestHandleWhisper(t *testing.T) {
	beacon := NewBeacon("test-receiver", 9001, nil)
	defer close(beacon.Messages)

	// Test POST request
	req := httptest.NewRequest(http.MethodPost, "/whisper", strings.NewReader("test message"))
	rec := httptest.NewRecorder()

	beacon.handleWhisper(rec, req)

	if rec.Code != http.StatusOK {
		t.Errorf("Expected status %d, got %d", http.StatusOK, rec.Code)
	}

	select {
	case msg := <-beacon.Messages:
		if msg != "test message" {
			t.Errorf("Expected message 'test message', got '%s'", msg)
		}
	case <-time.After(100 * time.Millisecond):
		t.Error("Expected message to be received on channel, but timed out")
	}

	// Test non-POST request
	req = httptest.NewRequest(http.MethodGet, "/whisper", nil)
	rec := httptest.NewRecorder()

	beacon.handleWhisper(rec, req)

	if rec.Code != http.StatusMethodNotAllowed {
		t.Errorf("Expected status %d for GET, got %d", http.StatusMethodNotAllowed, rec.Code)
	}
}

// TestSendWhisper ensures a whisper can be sent to a single target.
func TestSendWhisper(t *testing.T) {
	// Mock rationale: Use httptest.NewServer to simulate a peer beacon's HTTP server
	// and verify that the correct request is sent to it.
	var receivedMsg string
	mockServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/whisper" {
			t.Errorf("Expected path /whisper, got %s", r.URL.Path)
		}
		if r.Method != http.MethodPost {
			t.Errorf("Expected POST method, got %s", r.Method)
		}
		body, err := io.ReadAll(r.Body)
		if err != nil {
			t.Fatalf("Failed to read request body: %v", err)
		}
		receivedMsg = string(body)
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "OK")
	}))
	defer mockServer.Close()

	beacon := NewBeacon("test-sender", 9002, nil)
	message := "secret whisper"

	err := beacon.SendWhisper(mockServer.URL, message)
	if err != nil {
		t.Fatalf("SendWhisper failed: %v", err)
	}

	if receivedMsg != message {
		t.Errorf("Expected received message '%s', got '%s'", message, receivedMsg)
	}
}

// TestBroadcastWhisper ensures whispers are sent to all configured peers concurrently.
func TestBroadcastWhisper(t *testing.T) {
	// Mock rationale: Use multiple httptest.NewServer instances to simulate several peer beacons.
	// Verify that each peer receives the broadcast message concurrently.
	peers := []string{"peer1", "peer2", "peer3"}
	var wg sync.WaitGroup
	receivedMessages := make(map[string]string)
	var mu sync.Mutex

	mockServers := make([]*httptest.Server, len(peers))
	peerURLs := make([]string, len(peers))

	for i, peerID := range peers {
		idx := i // Capture loop variable
		server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			body, err := io.ReadAll(r.Body)
			if err != nil {
				t.Fatalf("Failed to read request body for %s: %v", peerID, err)
			}
			mu.Lock()
			receivedMessages[peerID] = string(body)
			mu.Unlock()
			wg.Done() // Signal that this server received a message
			w.WriteHeader(http.StatusOK)
			fmt.Fprint(w, "OK")
		}))
		mockServers[idx] = server
		peerURLs[idx] = server.URL
		wg.Add(1) // Expect one message per peer
	}

	defer func() {
		for _, s := range mockServers {
			s.Close()
		}
	}()

	beacon := NewBeacon("test-broadcaster", 9003, peerURLs)
	message := "broadcast message"

	beacon.BroadcastWhisper(message)

	// Wait for all messages to be received by mock servers
	waitCh := make(chan struct{})
	go func() {
		wg.Wait()
		close(waitCh)
	}()

	select {
	case <-waitCh:
		// All messages received
	case <-time.After(5 * time.Second):
		t.Fatal("Timed out waiting for all peers to receive broadcast")
	}

	mu.Lock()
	defer mu.Unlock()

	for _, peerID := range peers {
		if receivedMessages[peerID] != message {
			t.Errorf("Peer %s: Expected message '%s', got '%s'", peerID, message, receivedMessages[peerID])
		}
	}
}

// TestBroadcastStatus ensures the status message is correctly formatted and broadcast.
func TestBroadcastStatus(t *testing.T) {
	// Mock rationale: Override BroadcastWhisper to capture the message it attempts to send.
	beacon := NewBeacon("status-beacon", 9004, nil)

	var capturedMessage string
	var broadcastCalled bool
	var mu sync.Mutex

	// Override BroadcastWhisper for testing
	originalBroadcastWhisper := beacon.BroadcastWhisper
	beacon.BroadcastWhisper = func(msg string) {
		mu.Lock()
		defer mu.Unlock()
		capturedMessage = msg
		broadcastCalled = true
	}

	beacon.BroadcastStatus()

	mu.Lock()
	defer mu.Unlock()

	if !broadcastCalled {
		t.Error("BroadcastWhisper was not called by BroadcastStatus")
	}
	if !strings.Contains(capturedMessage, "Beacon status-beacon is online at") {
		t.Errorf("Expected status message to contain 'Beacon status-beacon is online at', got '%s'", capturedMessage)
	}

	// Restore original BroadcastWhisper
	beacon.BroadcastWhisper = originalBroadcastWhisper
}

// TestStartHeartbeat ensures StartHeartbeat initiates periodic calls to BroadcastStatus.
func TestStartHeartbeat(t *testing.T) {
	// Mock rationale: Override BroadcastStatus to count calls and signal completion.
	beacon := NewBeacon("heartbeat-beacon", 9005, nil)

	callCount := 0
	callCh := make(chan struct{}, 5) // Buffer for a few calls
	var mu sync.Mutex

	// Override BroadcastStatus for testing
	originalBroadcastStatus := beacon.BroadcastStatus
	beacon.BroadcastStatus = func() {
		mu.Lock()
		callCount++
		mu.Unlock()
		select {
		case callCh <- struct{}{}:
		default:
			// Channel full, ignore
		}
	}

	go beacon.StartHeartbeat(10 * time.Millisecond) // Very short interval for testing

	// Wait for a few heartbeats
	for i := 0; i < 3; i++ {
		select {
		case <-callCh:
			// Received a call signal
		case <-time.After(50 * time.Millisecond):
			t.Fatalf("Timed out waiting for heartbeat %d", i+1)
		}
	}

	mu.Lock()
	defer mu.Unlock()

	if callCount < 3 {
		t.Errorf("Expected at least 3 BroadcastStatus calls, got %d", callCount)
	}

	// Restore original BroadcastStatus to avoid interfering with other tests if beacon is reused
	beacon.BroadcastStatus = originalBroadcastStatus
}
