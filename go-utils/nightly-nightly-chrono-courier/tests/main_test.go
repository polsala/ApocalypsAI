package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"os"
	"sync"
	"testing"
	"time"
)

// MockRoundTripper is a mock http.RoundTripper for testing purposes.
// It captures the request and signals when it was "sent".
type MockRoundTripper struct {
	mu       sync.Mutex
	requests []*http.Request
	signal   chan struct{} // Used to signal that a request was "sent"
	response *http.Response
}

func NewMockRoundTripper() *MockRoundTripper {
	return &MockRoundTripper{
		signal:   make(chan struct{}, 1), // Buffered channel to avoid deadlock if signal is sent before receive
		response: &http.Response{StatusCode: http.StatusOK, Body: ioutil.NopCloser(bytes.NewBufferString("OK"))},
	}
}

// RoundTrip implements the http.RoundTripper interface.
func (m *MockRoundTripper) RoundTrip(req *http.Request) (*http.Response, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.requests = append(m.requests, req)
	select {
	case m.signal <- struct{}{}: // Try to send signal, non-blocking
	default:
	}
	return m.response, nil // Always return a successful response for the mock
}

// GetRequests returns the captured requests.
func (m *MockRoundTripper) GetRequests() []*http.Request {
	m.mu.Lock()
	defer m.mu.Unlock()
	return m.requests
}

// WaitForRequest waits for a request to be captured by the mock.
func (m *MockRoundTripper) WaitForRequest(timeout time.Duration) bool {
	select {
	case <-m.signal:
		return true
	case <-time.After(timeout):
		return false
	}
}

// Reset clears captured requests and signals.
func (m *MockRoundTripper) Reset() {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.requests = nil
	// Clear the signal channel
	select {
	case <-m.signal:
	default:
	}
}

func TestHandleRelay(t *testing.T) {
	// Mock rationale: We need to test the `deliverMessage` function's behavior (delay and HTTP call)
	// without actually making external network requests. MockRoundTripper allows us to intercept
	// the HTTP client's `Do` method, capture the outgoing request, and verify it was called
	// after the expected delay.
	mockRT := NewMockRoundTripper()
	mockClient := &http.Client{Transport: mockRT}
	courierService := NewCourierService(mockClient)

	// Create a test server for the courier
	ts := httptest.NewServer(http.HandlerFunc(courierService.handleRelay))
	defer ts.Close()

	tests := []struct {
		name           string
		requestBody    RelayRequest
		expectedStatus int
		expectedDelay  time.Duration
		envDefaultDelay string
		expectRelay    bool
	}{
		{
			name: "Valid request with explicit delay",
			requestBody: RelayRequest{
				DestinationURL: "http://mock-destination.com/receive",
				MessageBody:    json.RawMessage(`{"data": "test message 1"}`),
				DelaySeconds:   1,
			},
			expectedStatus: http.StatusAccepted,
			expectedDelay:  1 * time.Second,
			expectRelay:    true,
		},
		{
			name: "Valid request with default delay from env",
			requestBody: RelayRequest{
				DestinationURL: "http://mock-destination.com/receive",
				MessageBody:    json.RawMessage(`{"data": "test message 2"}`),
				DelaySeconds:   0, // Should use default
			},
			expectedStatus:  http.StatusAccepted,
			expectedDelay:   2 * time.Second, // From env var
			envDefaultDelay: "2",
			expectRelay:     true,
		},
		{
			name: "Valid request with hardcoded default delay",
			requestBody: RelayRequest{
				DestinationURL: "http://mock-destination.com/receive",
				MessageBody:    json.RawMessage(`{"data": "test message 3"}`),
				DelaySeconds:   0, // Should use hardcoded default (5s)
			},
			expectedStatus: http.StatusAccepted,
			expectedDelay:  5 * time.Second, // Hardcoded default
			expectRelay:    true,
		},
		{
			name: "Missing destination_url",
			requestBody: RelayRequest{
				MessageBody:  json.RawMessage(`{"data": "invalid"}`),
				DelaySeconds: 1,
			},
			expectedStatus: http.StatusBadRequest,
			expectRelay:    false,
		},
		{
			name: "Missing message_body",
			requestBody: RelayRequest{
				DestinationURL: "http://mock-destination.com/receive",
				DelaySeconds:   1,
			},
			expectedStatus: http.StatusBadRequest,
			expectRelay:    false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			mockRT.Reset() // Clear previous requests for each test case

			// Set environment variable for default delay if specified
			if tt.envDefaultDelay != "" {
				os.Setenv("DEFAULT_DELAY_SECONDS", tt.envDefaultDelay)
				defer os.Unsetenv("DEFAULT_DELAY_SECONDS")
			} else {
				os.Unsetenv("DEFAULT_DELAY_SECONDS") // Ensure it's not set from previous tests
			}

			reqBodyBytes, _ := json.Marshal(tt.requestBody)
			req, err := http.NewRequest(http.MethodPost, ts.URL+"/relay", bytes.NewBuffer(reqBodyBytes))
			if err != nil {
				t.Fatalf("Failed to create request: %v", err)
			}
			req.Header.Set("Content-Type", "application/json")

			client := &http.Client{}
			resp, err := client.Do(req)
			if err != nil {
				t.Fatalf("Failed to send request to test server: %v", err)
			}
			defer resp.Body.Close()

			if resp.StatusCode != tt.expectedStatus {
				body, _ := ioutil.ReadAll(resp.Body)
				t.Errorf("Expected status %d, got %d. Body: %s", tt.expectedStatus, resp.StatusCode, string(body))
			}

			if tt.expectRelay {
				start := time.Now()
				// Wait for the mock RoundTripper to receive the request, with a small buffer
				if !mockRT.WaitForRequest(tt.expectedDelay + 500*time.Millisecond) {
					t.Errorf("Timed out waiting for message to be relayed after %v", tt.expectedDelay)
				}
				elapsed := time.Since(start)

				// Check if the elapsed time is approximately the expected delay
				// Allow for a small margin of error (e.g., 100ms before and 500ms after)
				if elapsed < tt.expectedDelay-100*time.Millisecond || elapsed > tt.expectedDelay+500*time.Millisecond {
					t.Errorf("Expected relay after ~%v, but it happened after %v", tt.expectedDelay, elapsed)
				}

				// Verify the relayed request details
				relayedRequests := mockRT.GetRequests()
				if len(relayedRequests) != 1 {
					t.Fatalf("Expected 1 relayed request, got %d", len(relayedRequests))
				}

				relayedReq := relayedRequests[0]
				if relayedReq.URL.String() != tt.requestBody.DestinationURL {
					t.Errorf("Relayed request destination URL mismatch. Expected %s, got %s", tt.requestBody.DestinationURL, relayedReq.URL.String())
				}

				relayedBody, _ := ioutil.ReadAll(relayedReq.Body)
				if !bytes.Equal(relayedBody, tt.requestBody.MessageBody) {
					t.Errorf("Relayed message body mismatch. Expected %s, got %s", string(tt.requestBody.MessageBody), string(relayedBody))
				}
			} else {
				// For requests that should not trigger a relay, ensure no requests were captured by the mock
				if mockRT.WaitForRequest(100 * time.Millisecond) { // Give a small grace period
					t.Errorf("Unexpectedly relayed a message for an invalid request.")
				}
				if len(mockRT.GetRequests()) > 0 {
					t.Errorf("Expected no relayed requests, but found %d", len(mockRT.GetRequests()))
				}
			}
		})
	}
}

func TestNewCourierService(t *testing.T) {
	// Test with nil client
	cs := NewCourierService(nil)
	if cs.client == nil {
		t.Error("Expected a default http.Client when nil is provided")
	}
	if cs.client.Timeout != 30*time.Second {
		t.Errorf("Expected default client timeout of 30s, got %v", cs.client.Timeout)
	}

	// Test with custom client
	customClient := &http.Client{Timeout: 10 * time.Second}
	cs = NewCourierService(customClient)
	if cs.client != customClient {
		t.Error("Expected custom http.Client to be used")
	}
}
