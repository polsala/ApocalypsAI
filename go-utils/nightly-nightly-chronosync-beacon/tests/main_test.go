package main

import (
	"context"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"golang.org/x/net/websocket"
)

// TestPulseHandler verifies the /pulse HTTP endpoint.
func TestPulseHandler(t *testing.T) {
	// # Mock rationale: httptest.NewServer creates a local, in-memory HTTP server
	// # that mimics the behavior of our actual server, allowing us to test HTTP
	// # handlers without binding to a real network port or requiring an external service.
	ts := httptest.NewServer(http.HandlerFunc(pulseHandler))
	defer ts.Close()

	resp, err := http.Get(ts.URL + "/pulse")
	if err != nil {
		t.Fatalf("Failed to send GET request: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status OK, got %d", resp.StatusCode)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		t.Fatalf("Failed to read response body: %v", err)
	}

	responseStr := strings.TrimSpace(string(body))
	if !strings.HasPrefix(responseStr, "Temporal Pulse: ") {
		t.Errorf("Response body has unexpected prefix: %s", responseStr)
	}

	timestampStr := strings.TrimPrefix(responseStr, "Temporal Pulse: ")
	parsedTime, err := time.Parse(time.RFC3339Nano, timestampStr)
	if err != nil {
		t.Fatalf("Failed to parse timestamp '%s': %v", timestampStr, err)
	}

	// Check if the timestamp is recent (within a small window of test execution).
	// This makes the test deterministic enough for time-based services without complex time mocking.
	now := time.Now().UTC()
	if now.Sub(parsedTime) > 5*time.Second || parsedTime.Sub(now) > 5*time.Second {
		t.Errorf("Timestamp is not recent. Expected ~%s, got %s", now.Format(time.RFC3339Nano), parsedTime.Format(time.RFC3339Nano))
	}
}

// TestStreamHandler verifies the /stream WebSocket endpoint.
func TestStreamHandler(t *testing.T) {
	// # Mock rationale: httptest.NewServer is used to create a test HTTP server.
	// # For WebSockets, we use websocket.Handler to wrap our streamHandler,
	// # and then connect to this test server's URL using websocket.Dial.
	// # This allows testing WebSocket communication locally without a real network setup.
	mux := http.NewServeMux()
	mux.Handle("/stream", websocket.Handler(streamHandler))
	ts := httptest.NewServer(mux)
	defer ts.Close()

	wsURL := "ws" + strings.TrimPrefix(ts.URL, "http") + "/stream"
	
	// Use a context with timeout for the WebSocket connection and message reception
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	conn, err := websocket.Dial(wsURL, "", "http://localhost") // Origin doesn't matter for local test
	if err != nil {
		t.Fatalf("Failed to dial WebSocket: %v", err)
	}
	defer conn.Close()

	var msg string
	var receivedTimes []time.Time

	// Receive a few messages to ensure continuous streaming
	for i := 0; i < 3; i++ {
		select {
		case <-ctx.Done():
			t.Fatalf("Test timed out waiting for WebSocket messages: %v", ctx.Err())
		default:
			if err := websocket.Message.Receive(conn, &msg); err != nil {
				t.Fatalf("Failed to receive WebSocket message: %v", err)
			}
			parsedTime, err := time.Parse(time.RFC3339Nano, msg)
			if err != nil {
				t.Fatalf("Failed to parse timestamp from WebSocket message '%s': %v", msg, err)
			}
			receivedTimes = append(receivedTimes, parsedTime)
		}
	}

	if len(receivedTimes) < 3 {
		t.Fatalf("Expected to receive at least 3 messages, got %d", len(receivedTimes))
	}

	// Verify timestamps are increasing and roughly at the expected interval
	for i := 1; i < len(receivedTimes); i++ {
		if receivedTimes[i].Before(receivedTimes[i-1]) {
			t.Errorf("Received timestamp %s is not after previous timestamp %s", receivedTimes[i], receivedTimes[i-1])
		}
		// Check interval, allowing for some jitter
		diff := receivedTimes[i].Sub(receivedTimes[i-1])
		if diff < pulseInterval/2 || diff > pulseInterval*2 { // Allow +/- 50% for network/scheduling jitter
			t.Errorf("Unexpected time difference between pulses: %s (expected ~%s)", diff, pulseInterval)
		}
	}

	// Check if the last timestamp is recent
	now := time.Now().UTC()
	lastParsedTime := receivedTimes[len(receivedTimes)-1]
	if now.Sub(lastParsedTime) > 5*time.Second || lastParsedTime.Sub(now) > 5*time.Second {
		t.Errorf("Last received timestamp is not recent. Expected ~%s, got %s", now.Format(time.RFC3339Nano), lastParsedTime.Format(time.RFC3339Nano))
	}
}

// TestStartServer function to ensure the server can be started and stopped gracefully.
func TestStartServer(t *testing.T) {
	// # Mock rationale: We start a real server on a random available port (by passing "0")
	// # and then immediately shut it down. This tests the server's lifecycle
	// # without needing to interact with it over the network for a long duration.
	// # It verifies that the server can bind and unbind from a port.
	server := startServer("0") // Use port 0 to let the OS choose a free port
	if server == nil {
		t.Fatal("startServer returned nil")
	}

	// Give the server a moment to start up
	time.Sleep(100 * time.Millisecond)

	// Attempt to gracefully shut down the server
	ctx, cancel := context.WithTimeout(context.Background(), shutdownTimeout)
	defer cancel()

	err := server.Shutdown(ctx)
	if err != nil && err != http.ErrServerClosed {
		t.Fatalf("Server shutdown failed: %v", err)
	}
}
