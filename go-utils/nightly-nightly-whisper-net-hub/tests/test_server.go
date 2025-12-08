package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"
	"time" // Mock rationale: time.Now() is used in the handler, but for testing aggregation, its exact value isn't critical. The test focuses on message content and origin.
)

func TestWhisperHub_HandleWhisper(t *testing.T) {
	hub := NewWhisperHub()
	ts := httptest.NewServer(http.HandlerFunc(hub.HandleWhisper)) // Mock rationale: httptest.NewServer provides a mock HTTP server for isolated testing of handlers.
	defer ts.Close()

	testCases := []struct {
		name       string
		origin     string
		message    string
		statusCode int
		expectedBody string
	}{
		{"ValidWhisper", "node-alpha", "The winds whisper of change...", http.StatusAccepted, "Whisper received from node-alpha\n"},
		{"AnotherValidWhisper", "node-beta", "Found a shiny bottlecap!", http.StatusAccepted, "Whisper received from node-beta\n"},
		{"EmptyOrigin", "", "A silent message.", http.StatusBadRequest, "Origin and Message cannot be empty\n"},
		{"EmptyMessage", "node-gamma", "", http.StatusBadRequest, "Origin and Message cannot be empty\n"},
		{"EmptyBoth", "", "", http.StatusBadRequest, "Origin and Message cannot be empty\n"},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			whisperPayload := Whisper{Origin: tc.origin, Message: tc.message}
			jsonPayload, _ := json.Marshal(whisperPayload)
			req, err := http.NewRequest(http.MethodPost, ts.URL+"/whisper", bytes.NewBuffer(jsonPayload))
			if err != nil {
				t.Fatalf("Failed to create request: %v", err)
			}
			req.Header.Set("Content-Type", "application/json")

			resp, err := http.DefaultClient.Do(req) // Mock rationale: http.DefaultClient is used to make requests to the httptest.NewServer, which is a controlled, local environment.
			if err != nil {
				t.Fatalf("Failed to send request: %v", err)
			}
			defer resp.Body.Close()

			if resp.StatusCode != tc.statusCode {
				bodyBytes, _ := ioutil.ReadAll(resp.Body)
				t.Errorf("Expected status %d, got %d. Body: %s", tc.statusCode, resp.StatusCode, string(bodyBytes))
			}

			if tc.statusCode == http.StatusAccepted {
				// Verify the whisper was stored
				hub.mu.Lock()
				storedWhispers := hub.whispers[tc.origin]
				hub.mu.Unlock()

				if len(storedWhispers) == 0 {
					t.Errorf("Expected whisper from %s to be stored, but none found.", tc.origin)
				} else {
					found := false
					for _, w := range storedWhispers {
						if w.Message == tc.message {
							found = true
							break
						}
					}
					if !found {
						t.Errorf("Whisper \"%s\" from %s not found in stored whispers.", tc.message, tc.origin)
					}
				}
			}
		})
	}
}

func TestWhisperHub_HandleStatus(t *testing.T) {
	hub := NewWhisperHub()
	ts := httptest.NewServer(http.HandlerFunc(hub.HandleStatus)) // Mock rationale: httptest.NewServer provides a mock HTTP server for isolated testing of handlers.
	defer ts.Close()

	// Add some test whispers directly to the hub
	hub.mu.Lock()
	hub.whispers["node-alpha"] = []Whisper{
		{Origin: "node-alpha", Message: "First whisper", Timestamp: time.Now().Add(-5 * time.Minute)},
		{Origin: "node-alpha", Message: "Second whisper", Timestamp: time.Now().Add(-2 * time.Minute)},
	}
	hub.whispers["node-beta"] = []Whisper{
		{Origin: "node-beta", Message: "Beta's message", Timestamp: time.Now().Add(-1 * time.Minute)},
	}
	hub.mu.Unlock()

	req, err := http.NewRequest(http.MethodGet, ts.URL+"/status", nil)
	if err != nil {
		t.Fatalf("Failed to create request: %v", err)
	}

	resp, err := http.DefaultClient.Do(req) // Mock rationale: http.DefaultClient is used to make requests to the httptest.NewServer, which is a controlled, local environment.
	if err != nil {
		t.Fatalf("Failed to send request: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status %d, got %d", http.StatusOK, resp.StatusCode)
	}

	var receivedStatus map[string][]Whisper
	err = json.NewDecoder(resp.Body).Decode(&receivedStatus)
	if err != nil {
		t.Fatalf("Failed to decode response body: %v", err)
	}

	if len(receivedStatus) != 2 {
		t.Errorf("Expected 2 origins in status, got %d", len(receivedStatus))
	}
	if len(receivedStatus["node-alpha"]) != 2 {
		t.Errorf("Expected 2 whispers from node-alpha, got %d", len(receivedStatus["node-alpha"]))
	}
	if len(receivedStatus["node-beta"]) != 1 {
		t.Errorf("Expected 1 whisper from node-beta, got %d", len(receivedStatus["node-beta"]))
	}

	// Check content of a specific whisper (ignoring timestamp for simplicity in comparison)
	foundAlphaWhisper := false
	for _, w := range receivedStatus["node-alpha"] {
		if w.Message == "First whisper" && w.Origin == "node-alpha" {
			foundAlphaWhisper = true
			break
		}
	}
	if !foundAlphaWhisper {
		t.Errorf("Expected 'First whisper' from 'node-alpha' not found in status.")
	}
}

func TestWhisperHub_ConcurrentWhispers(t *testing.T) {
	hub := NewWhisperHub()
	ts := httptest.NewServer(http.HandlerFunc(hub.HandleWhisper)) // Mock rationale: httptest.NewServer provides a mock HTTP server for isolated testing of handlers.
	defer ts.Close()

	numSenders := 10
	whispersPerSender := 5
	var wg sync.WaitGroup
	wg.Add(numSenders)

	for i := 0; i < numSenders; i++ {
		go func(senderID int) {
			defer wg.Done()
			origin := fmt.Sprintf("node-%d", senderID)
			for j := 0; j < whispersPerSender; j++ {
				message := fmt.Sprintf("Whisper %d from %s", j, origin)
				whisperPayload := Whisper{Origin: origin, Message: message}
				jsonPayload, _ := json.Marshal(whisperPayload)

				req, err := http.NewRequest(http.MethodPost, ts.URL+"/whisper", bytes.NewBuffer(jsonPayload))
				if err != nil {
					t.Errorf("Sender %d: Failed to create request: %v", senderID, err)
					continue
				}
				req.Header.Set("Content-Type", "application/json")

				resp, err := http.DefaultClient.Do(req) // Mock rationale: http.DefaultClient is used to make requests to the httptest.NewServer, which is a controlled, local environment.
				if err != nil {
					t.Errorf("Sender %d: Failed to send request: %v", senderID, err)
					continue
				}
				resp.Body.Close()
				if resp.StatusCode != http.StatusAccepted {
					t.Errorf("Sender %d: Expected status %d, got %d", senderID, http.StatusAccepted, resp.StatusCode)
				}
			}
		}(i)
	}

	wg.Wait()

	// Verify all whispers were collected
	hub.mu.Lock()
	defer hub.mu.Unlock()

	totalWhispers := 0
	for origin, whispers := range hub.whispers {
		if len(whispers) != whispersPerSender {
			t.Errorf("Origin %s: Expected %d whispers, got %d", origin, whispersPerSender, len(whispers))
		}
		totalWhispers += len(whispers)
	}

	expectedTotal := numSenders * whispersPerSender
	if totalWhispers != expectedTotal {
		t.Errorf("Expected total %d whispers, got %d", expectedTotal, totalWhispers)
	}
}
