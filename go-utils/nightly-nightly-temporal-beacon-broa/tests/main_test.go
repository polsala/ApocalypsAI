package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
	"testing"
)

// MockRoundTripper is a mock implementation of http.RoundTripper.
type MockRoundTripper struct {
	Response *http.Response
	Err      error
}

// RoundTrip implements the http.RoundTripper interface.
func (m *MockRoundTripper) RoundTrip(req *http.Request) (*http.Response, error) {
	// Mock rationale: This allows us to simulate HTTP responses without making actual network calls.
	// It makes tests deterministic and offline by returning predefined responses or errors.
	return m.Response, m.Err
}

// NewMockClient creates an http.Client with a mock RoundTripper.
func NewMockClient(resp *http.Response, err error) HTTPClient {
	return &http.Client{
		Transport: &MockRoundTripper{Response: resp, Err: err},
	}
}

func TestBroadcast_Success(t *testing.T) {
	// Mock rationale: Simulate a successful HTTP response from a temporal relay.
	// This ensures the utility correctly processes successful network interactions and parses the expected JSON response.
	mockResponseJSON := `{
		"status": "received",
		"temporal_distortion": 0.5,
		"relay_message": "Echo from the past!"
	}`
	mockResp := &http.Response{
		StatusCode: http.StatusOK,
		Body:       ioutil.NopCloser(bytes.NewBufferString(mockResponseJSON)),
		Header:     make(http.Header),
	}
	mockClient := NewMockClient(mockResp, nil)

	message := "Hello Temporal Void!"
	relayURLs := []string{"http://temporal-relay-alpha.com/broadcast", "http://temporal-relay-beta.com/broadcast"}

	results := Broadcast(message, relayURLs, mockClient)

	if len(results) != 2 {
		t.Fatalf("Expected 2 results, got %d", len(results))
	}

	for _, res := range results {
		if !res.Success {
			t.Errorf("Expected success for %s, got failure: %s", res.RelayURL, res.Error)
		}
		if res.TemporalDistortion != 0.5 {
			t.Errorf("Expected distortion 0.5, got %.2f for %s", res.TemporalDistortion, res.RelayURL)
		}
		if res.RelayMessage != "Echo from the past!" {
			t.Errorf("Expected relay message 'Echo from the past!', got '%s' for %s", res.RelayMessage, res.RelayURL)
		}
	}
}

func TestBroadcast_PartialFailure(t *testing.T) {
	// Mock rationale: Simulate one successful and one failed HTTP response based on the URL.
	// This verifies the utility handles mixed outcomes correctly, reporting success for some relays and specific errors for others.

	// Success mock
	successResponseJSON := `{
		"status": "received",
		"temporal_distortion": 1.2,
		"relay_message": "Future echoes!"
	}`
	successResp := &http.Response{
		StatusCode: http.StatusOK,
		Body:       ioutil.NopCloser(bytes.NewBufferString(successResponseJSON)),
		Header:     make(http.Header),
	}

	// Failure mock (simulating a 500 Internal Server Error)
	failureResponseJSON := `{"error": "Temporal anomaly detected"}`
	failureResp := &http.Response{
		StatusCode: http.StatusInternalServerError,
		Body:       ioutil.NopCloser(bytes.NewBufferString(failureResponseJSON)),
		Header:     make(http.Header),
	}

	// Custom mock client that returns different responses based on URL
	mockClient := &mockHTTPClientFunc(func(req *http.Request) (*http.Response, error) {
		if strings.Contains(req.URL.Host, "success") {
			return successResp, nil
		}
		if strings.Contains(req.URL.Host, "failure") {
			return failureResp, nil
		}
		return nil, fmt.Errorf("unexpected URL: %s", req.URL.String())
	})

	message := "Urgent transmission!"
	relayURLs := []string{"http://success-relay.com/broadcast", "http://failure-relay.com/broadcast"}

	results := Broadcast(message, relayURLs, mockClient)

	if len(results) != 2 {
		t.Fatalf("Expected 2 results, got %d", len(results))
	}

	// Check success result
	successResult := results[0]
	if !strings.Contains(successResult.RelayURL, "success") { // Ensure order is not assumed due to goroutines
		successResult = results[1]
	}
	if !successResult.Success {
		t.Errorf("Expected success for success-relay, got failure: %s", successResult.Error)
	}
	if successResult.TemporalDistortion != 1.2 {
		t.Errorf("Expected distortion 1.2, got %.2f for success-relay", successResult.TemporalDistortion)
	}
	if successResult.RelayMessage != "Future echoes!" {
		t.Errorf("Expected relay message 'Future echoes!', got '%s' for success-relay", successResult.RelayMessage)
	}

	// Check failure result
	failureResult := results[0]
	if !strings.Contains(failureResult.RelayURL, "failure") { // Ensure order is not assumed due to goroutines
		failureResult = results[1]
	}
	if failureResult.Success {
		t.Errorf("Expected failure for failure-relay, got success")
	}
	if !strings.Contains(failureResult.Error, "Relay responded with status 500") {
		t.Errorf("Expected 500 error for failure-relay, got: %s", failureResult.Error)
	}
}

func TestBroadcast_NetworkError(t *testing.T) {
	// Mock rationale: Simulate a network error (e.g., connection refused, DNS lookup failure).
	// This tests the utility's robustness against underlying network issues, ensuring it reports connection problems correctly.
	mockClient := NewMockClient(nil, fmt.Errorf("connection refused"))

	message := "Emergency signal!"
	relayURLs := []string{"http://unreachable-relay.com/broadcast"}

	results := Broadcast(message, relayURLs, mockClient)

	if len(results) != 1 {
		t.Fatalf("Expected 1 result, got %d", len(results))
	}

	res := results[0]
	if res.Success {
		t.Errorf("Expected failure for network error, got success")
	}
	if !strings.Contains(res.Error, "Failed to send request: connection refused") {
		t.Errorf("Expected 'connection refused' error, got: %s", res.Error)
	}
}

// Helper for the custom mock client function type.
type mockHTTPClientFunc func(req *http.Request) (*http.Response, error)

func (f mockHTTPClientFunc) Do(req *http.Request) (*http.Response, error) {
	return f(req)
}
