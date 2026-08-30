package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
	"sync"
	"testing"
	"time"
)

// MockHTTPClient implements HTTPClient for testing purposes.
type MockHTTPClient struct {
	MockResponses    map[string]*http.Response // Map URL to a mock response
	MockErrors       map[string]error          // Map URL to a mock error
	ReceivedRequests []struct {                // To inspect what was sent
		URL  string
		Body string
	}
	Mutex sync.Mutex // Protects ReceivedRequests
}

// NewMockHTTPClient creates a new mock client with default success responses.
func NewMockHTTPClient() *MockHTTPClient {
	return &MockHTTPClient{
		MockResponses: make(map[string]*http.Response),
		MockErrors:    make(map[string]error),
	}
}

// Post simulates an HTTP POST request.
func (m *MockHTTPClient) Post(url, contentType string, body *bytes.Buffer) (*http.Response, error) {
	m.Mutex.Lock()
	defer m.Mutex.Unlock()

	// # Mock rationale: Simulate network latency for deterministic tests.
	// This ensures that even with mocked network calls, the concurrency
	// and waiting logic (WaitGroup) is tested under conditions that
	// resemble real-world asynchronous behavior.
	time.Sleep(10 * time.Millisecond)

	m.ReceivedRequests = append(m.ReceivedRequests, struct {
		URL  string
		Body string
	}{URL: url, Body: body.String()})

	if err, ok := m.MockErrors[url]; ok {
		return nil, err
	}
	if resp, ok := m.MockResponses[url]; ok {
		return resp, nil
	}

	// Default successful response
	return &http.Response{
		StatusCode: http.StatusOK,
		Body:       ioutil.NopCloser(strings.NewReader(`{"status":"received"}`)),
		Header:     make(http.Header),
	}, nil
}

func TestObfuscateMessage(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"Hello World", "Uryyb Jbeyq [echoed]"},
		{"ApocalypsAI", "NcbcnycfnN [echoed]"},
		{"123 ABC", "123 NOP [echoed]"},
		{"", " [echoed]"},
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			actual := obfuscateMessage(tt.input)
			if actual != tt.expected {
				t.Errorf("obfuscateMessage(%q) = %q; want %q", tt.input, actual, tt.expected)
			}
		})
	}
}

func TestBroadcastWhisper(t *testing.T) {
	mockClient := NewMockHTTPClient()

	// # Mock rationale: Define specific mock responses for deterministic testing of broadcast logic.
	// This allows us to control success/failure scenarios without actual network calls.
	mockClient.MockResponses["http://mock-post-1/receive"] = &http.Response{
		StatusCode: http.StatusOK,
		Body:       ioutil.NopCloser(strings.NewReader(`{"status":"received"}`)),
	}
	mockClient.MockResponses["http://mock-post-2/receive"] = &http.Response{
		StatusCode: http.StatusInternalServerError,
		Body:       ioutil.NopCloser(strings.NewReader(`{"error":"server error"}`)),
	}
	mockClient.MockErrors["http://mock-post-3/receive"] = fmt.Errorf("network timeout")

	posts := []ListeningPost{
		{Name: "Mock Post 1", URL: "http://mock-post-1/receive"},
		{Name: "Mock Post 2", URL: "http://mock-post-2/receive"},
		{Name: "Mock Post 3", URL: "http://mock-post-3/receive"},
		{Name: "Mock Post 4", URL: "http://mock-post-4/receive"}, // Will use default success
	}

	message := "Test Whisper"
	results := broadcastWhisper(message, posts, mockClient)

	if len(results) != len(posts) {
		t.Errorf("Expected %d results, got %d", len(posts), len(results))
	}

	// Check if expected outcomes are present
	expectedSuccess := 0
	expectedFailure := 0
	for _, res := range results {
		if strings.Contains(res, "Successfully echoed to Mock Post 1") {
			expectedSuccess++
		} else if strings.Contains(res, "Failed to send to Mock Post 2") {
			expectedFailure++
		} else if strings.Contains(res, "Error sending to Mock Post 3") {
			expectedFailure++
		} else if strings.Contains(res, "Successfully echoed to Mock Post 4") {
			expectedSuccess++
		} else {
			t.Errorf("Unexpected result: %s", res)
		}
	}

	if expectedSuccess != 2 {
		t.Errorf("Expected 2 successful broadcasts, got %d", expectedSuccess)
	}
	if expectedFailure != 2 {
		t.Errorf("Expected 2 failed broadcasts, got %d", expectedFailure)
	}

	// Verify the content sent to mock posts
	obfuscatedMsg := obfuscateMessage(message)
	mockClient.Mutex.Lock()
	defer mockClient.Mutex.Unlock()
	if len(mockClient.ReceivedRequests) != len(posts) {
		t.Errorf("Expected %d requests to be received by mock client, got %d", len(posts), len(mockClient.ReceivedRequests))
	}

	for _, req := range mockClient.ReceivedRequests {
		var payload MessagePayload
		err := json.Unmarshal([]byte(req.Body), &payload)
		if err != nil {
			t.Fatalf("Failed to unmarshal received request body: %v", err)
		}
		if payload.Message != obfuscatedMsg {
			t.Errorf("Message sent to %s was %q, expected %q", req.URL, payload.Message, obfuscatedMsg)
		}
		if _, err := time.Parse(time.RFC3339, payload.Timestamp); err != nil {
			t.Errorf("Timestamp format invalid for %s: %v", req.URL, err)
		}
	}
}

func TestSendWhisperToPost(t *testing.T) {
	mockClient := NewMockHTTPClient()
	post := ListeningPost{Name: "Single Post", URL: "http://single-mock/receive"}
	obfuscatedMsg := "Test Message [echoed]"

	var wg sync.WaitGroup
	results := make(chan string, 1)

	wg.Add(1)
	go sendWhisperToPost(mockClient, post, obfuscatedMsg, &wg, results)
	wg.Wait()
	close(results)

	result := <-results
	if !strings.Contains(result, "Successfully echoed to Single Post") {
		t.Errorf("Expected success message, got: %s", result)
	}

	// Test error case
	mockClient = NewMockHTTPClient()
	mockClient.MockErrors["http://error-mock/receive"] = fmt.Errorf("forced error")
	errorPost := ListeningPost{Name: "Error Post", URL: "http://error-mock/receive"}

	wg = sync.WaitGroup{}
	results = make(chan string, 1)

	wg.Add(1)
	go sendWhisperToPost(mockClient, errorPost, obfuscatedMsg, &wg, results)
	wg.Wait()
	close(results)

	result = <-results
	if !strings.Contains(result, "Error sending to Error Post") {
		t.Errorf("Expected error message, got: %s", result)
	}
}
