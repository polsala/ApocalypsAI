package main

import (
	"bytes"
	"context"
	"encoding/json"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"
	"time"
)

// MockHTTPClient is a mock implementation of http.Client for testing network calls.
type MockHTTPClient struct {
	DoFunc func(req *http.Request) (*http.Response, error)
}

func (m *MockHTTPClient) Do(req *http.Request) (*http.Response, error) {
	return m.DoFunc(req)
}

// TestNewGossipGoblin ensures the constructor initializes correctly.
func TestNewGossipGoblin(t *testing.T) {
	addr := ":8080"
	peers := []string{"http://localhost:8081", "http://localhost:8082"}

	goblin := NewGossipGoblin(addr, peers)

	if goblin.Addr != addr {
		t.Errorf("Expected address %s, got %s", addr, goblin.Addr)
	}
	if len(goblin.Peers) != 2 {
		t.Errorf("Expected 2 peers, got %d", len(goblin.Peers))
	}
	if len(goblin.MessageLog) != 0 {
		t.Errorf("Expected empty message log, got %d messages", len(goblin.MessageLog))
	}
	if goblin.httpClient == nil {
		t.Errorf("Expected http client to be initialized")
	}
}

// TestHandleGossipReceive tests if the goblin can receive and log a message.
func TestHandleGossipReceive(t *testing.T) {
	goblin := NewGossipGoblin(":8080", []string{}) // No peers for this test

	// Create a test HTTP server that uses our goblin's handler
	ts := httptest.NewServer(http.HandlerFunc(goblin.handleGossip))
	defer ts.Close()

	// Send a mock message to the test server
	msg := GossipMessage{
		Sender:    "test-sender",
		Content:   "Hello, goblin!",
		Timestamp: time.Now(),
	}
	jsonMsg, _ := json.Marshal(msg)

	res, err := http.Post(ts.URL+"/gossip", "application/json", bytes.NewBuffer(jsonMsg))
	if err != nil {
		t.Fatalf("Failed to send POST request: %v", err)
	}
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		t.Errorf("Expected status OK, got %d", res.StatusCode)
	}

	// Wait briefly for the async logMessage to complete
	time.Sleep(10 * time.Millisecond)

	goblin.logMutex.Lock()
	defer goblin.logMutex.Unlock()

	if len(goblin.MessageLog) != 1 {
		t.Fatalf("Expected 1 message in log, got %d", len(goblin.MessageLog))
	}

	receivedMsg := goblin.MessageLog[0]
	if receivedMsg.Content != msg.Content {
		t.Errorf("Expected message content '%s', got '%s'", msg.Content, receivedMsg.Content)
	}
	if receivedMsg.Sender != msg.Sender {
		t.Errorf("Expected message sender '%s', got '%s'", msg.Sender, receivedMsg.Sender)
	}
}

// TestPropagateGossip tests if the goblin attempts to send messages to its peers.
func TestPropagateGossip(t *testing.T) {
	peer1URL := "http://localhost:8081"
	peer2URL := "http://localhost:8082"
	goblin := NewGossipGoblin(":8080", []string{peer1URL, peer2URL})

	var mu sync.Mutex
	calledURLs := make(map[string]int)

	// Mock rationale: We mock the http.Client to prevent actual network calls
	// and instead capture which URLs the goblin attempts to gossip to.
	goblin.httpClient = &MockHTTPClient{
		DoFunc: func(req *http.Request) (*http.Response, error) {
			mu.Lock()
			defer mu.Unlock()
			calledURLs[req.URL.String()]++
			return &http.Response{StatusCode: http.StatusOK, Body: ioutil.NopCloser(bytes.NewBufferString("OK"))}, nil
		},
	}

	msg := GossipMessage{
		Sender:    "original-sender",
		Content:   "Secret whisper!",
		Timestamp: time.Now(),
	}

	goblin.propagateGossip(msg)

	// Give goroutines a moment to execute
	time.Sleep(50 * time.Millisecond)

	mu.Lock()
	defer mu.Unlock()

	if calledURLs[peer1URL+"/gossip"] != 1 {
		t.Errorf("Expected gossip to peer1 once, got %d", calledURLs[peer1URL+"/gossip"])
	}
	if calledURLs[peer2URL+"/gossip"] != 1 {
		t.Errorf("Expected gossip to peer2 once, got %d", calledURLs[peer2URL+"/gossip"])
	}

	// Ensure the sender in the propagated message is the current goblin's address
	// This is implicitly tested by the mock, as the request body would contain it.
	// A more explicit test would involve decoding the request body in the mock.
}

// TestPropagateGossipSelfExclusion ensures a goblin doesn't gossip to itself.
func TestPropagateGossipSelfExclusion(t *testing.T) {
	addr := "http://localhost:8080"
	goblin := NewGossipGoblin(addr, []string{addr, "http://localhost:8081"})

	var mu sync.Mutex
	calledURLs := make(map[string]int)

	// Mock rationale: Similar to TestPropagateGossip, we mock the HTTP client
	// to verify that the self-address is excluded from propagation targets.
	goblin.httpClient = &MockHTTPClient{
		DoFunc: func(req *http.Request) (*http.Response, error) {
			mu.Lock()
			defer mu.Unlock()
			calledURLs[req.URL.String()]++
			return &http.Response{StatusCode: http.StatusOK, Body: ioutil.NopCloser(bytes.NewBufferString("OK"))}, nil
		},
	}

	msg := GossipMessage{
		Sender:    "original-sender",
		Content:   "Self-exclusion test",
		Timestamp: time.Now(),
	}

	goblin.propagateGossip(msg)

	time.Sleep(50 * time.Millisecond)

	mu.Lock()
	defer mu.Unlock()

	if calledURLs[addr+"/gossip"] != 0 {
		t.Errorf("Expected no gossip to self, but found %d calls", calledURLs[addr+"/gossip"])
	}
	if calledURLs["http://localhost:8081"+"/gossip"] != 1 {
		t.Errorf("Expected gossip to other peer once, got %d", calledURLs["http://localhost:8081"+"/gossip"])
	}
}

// TestSendMessageClient tests the client-side message sending function.
func TestSendMessageClient(t *testing.T) {
	var receivedMsg GossipMessage
	var mu sync.Mutex

	// Mock rationale: We create a test HTTP server to act as the target goblin.
	// This allows us to verify that sendMessage correctly formats and sends the message
	// without needing a real running goblin server.
	targetServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		mu.Lock()
		defer mu.Unlock()
		if r.Method != http.MethodPost {
			t.Errorf("Expected POST, got %s", r.Method)
			http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
			return
		}
		if !strings.Contains(r.URL.Path, "/gossip") {
			t.Errorf("Expected /gossip endpoint, got %s", r.URL.Path)
			http.Error(w, "Not Found", http.StatusNotFound)
			return
		}
		err := json.NewDecoder(r.Body).Decode(&receivedMsg)
		if err != nil {
			t.Errorf("Failed to decode received message: %v", err)
			http.Error(w, "Bad Request", http.StatusBadRequest)
			return		}
		w.WriteHeader(http.StatusOK)
	}))
	defer targetServer.Close()

	content := "Client test message"
	err := sendMessage(targetServer.URL, content)
	if err != nil {
		t.Fatalf("sendMessage failed: %v", err)
	}

	mu.Lock()
	defer mu.Unlock()

	if receivedMsg.Content != content {
		t.Errorf("Expected received message content '%s', got '%s'", content, receivedMsg.Content)
	}
	if receivedMsg.Sender != "client" {
		t.Errorf("Expected sender 'client', got '%s'", receivedMsg.Sender)
	}
	if receivedMsg.Timestamp.IsZero() {
		t.Errorf("Expected timestamp to be set, but it's zero")
	}
}
