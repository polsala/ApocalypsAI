package main

import (
	"bytes"
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

// Mock rationale: We need to control the HTTP client's behavior to prevent actual network calls
// and to verify that the delayed forwarding logic attempts to send the message correctly.
// httptest.NewServer provides a lightweight, in-memory HTTP server for mocking the target URL.
// The mockSleeper prevents actual time.Sleep calls during tests to ensure determinism and speed.

func TestRelayHandler_Success(t *testing.T) {
	// Create a mock HTTP server for the target_url to capture the forwarded message
	targetServerCalled := make(chan bool, 1)
	targetServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			t.Errorf("Expected POST request, got %s", r.Method)
		}
		body, _ := ioutil.ReadAll(r.Body)
		var payload map[string]string
		json.Unmarshal(body, &payload)
		if payload["echo_message"] != "test message" {
			t.Errorf("Expected message 'test message', got '%s'", payload["echo_message"])
		}
		w.WriteHeader(http.StatusOK)
		targetServerCalled <- true
	}))
	defer targetServer.Close()

	// Create a mock sleeper that doesn't actually sleep but signals completion
	sleepDone := make(chan time.Duration, 1)
	mockSleeper := func(d time.Duration) {
		sleepDone <- d
	}

	// Temporarily replace the defaultSleeper with our mock
	originalSleeper := defaultSleeper
	defaultSleeper = mockSleeper
	defer func() { defaultSleeper = originalSleeper }() // Restore after test

	// Create a request to our relay handler
	relayReqBody := RelayRequest{
		Message:   "test message",
		TargetURL: targetServer.URL,
		DelayMs:   50, // 50ms delay
	}
	jsonBody, _ := json.Marshal(relayReqBody)
	req := httptest.NewRequest(http.MethodPost, "/relay", bytes.NewBuffer(jsonBody))
	req.Header.Set("Content-Type", "application/json")

	rr := httptest.NewRecorder()
	relayHandler(rr, req)

	// Check the immediate response from the relay handler
	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}
	expected := "Message scheduled for relay to " + targetServer.URL + " with 50ms delay.\n"
	if rr.Body.String() != expected {
		t.Errorf("handler returned unexpected body: got %v want %v", rr.Body.String(), expected)
	}

	// Verify the mock sleeper was called with the correct delay
	select {
	case d := <-sleepDone:
		if d != 50*time.Millisecond {
			t.Errorf("Expected sleeper to be called with 50ms, got %v", d)
		}
	case <-time.After(1 * time.Second): // Give it a moment, though it should be immediate
		t.Fatal("Mock sleeper was not called")
	}

	// Wait for the delayed forwarding to complete and hit the target server
	select {
	case <-targetServerCalled:
		// Success, target server was hit
	case <-time.After(1 * time.Second): // A reasonable timeout for the goroutine to run
		t.Fatal("Delayed message was not forwarded to target server")
	}
}

func TestRelayHandler_InvalidRequest(t *testing.T) {
	tests := []struct {
		name       string
		method     string
		body       string
		statusCode int
		errorMsg   string
	}{
		{
			name:       "GET method",
			method:     http.MethodGet,
			body:       `{}`, // Body doesn't matter for method check
			statusCode: http.StatusMethodNotAllowed,
			errorMsg:   "Only POST method is supported\n",
		},
		{
			name:       "Invalid JSON",
			method:     http.MethodPost,
			body:       `not json`,
			statusCode: http.StatusBadRequest,
			errorMsg:   "Invalid request body\n",
		},
		{
			name:       "Missing target_url",
			method:     http.MethodPost,
			body:       `{"message": "hello"}`,
			statusCode: http.StatusBadRequest,
			errorMsg:   "target_url is required\n",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req := httptest.NewRequest(tt.method, "/relay", bytes.NewBufferString(tt.body))
			req.Header.Set("Content-Type", "application/json")
			rr := httptest.NewRecorder()
			relayHandler(rr, req)

			if status := rr.Code; status != tt.statusCode {
				t.Errorf("handler returned wrong status code: got %v want %v", status, tt.statusCode)
			}
			if rr.Body.String() != tt.errorMsg {
				t.Errorf("handler returned unexpected body: got %q want %q", rr.Body.String(), tt.errorMsg)
			}
		})
	}
}

func TestDelayedForward_NetworkError(t *testing.T) {
	// Mock the http.Post call to simulate a network error
	// We need to temporarily replace the http.DefaultClient's Transport for this.
	originalTransport := http.DefaultClient.Transport
	defer func() { http.DefaultClient.Transport = originalTransport }()

	http.DefaultClient.Transport = roundTripperFunc(func(req *http.Request) (*http.Response, error) {
		return nil, fmt.Errorf("simulated network error")
	})

	// Use a mock sleeper that just signals completion immediately
	mockSleeper := func(d time.Duration) {
		// No actual sleep
	}

	// Capture logs to verify error message
	var logBuffer bytes.Buffer
	log.SetOutput(&logBuffer)
	defer log.SetOutput(ioutil.Discard) // Reset log output after test

	delayedForward("error message", "http://nonexistent-target.com", 1*time.Millisecond, mockSleeper)

	// Verify that the error was logged
	if !bytes.Contains(logBuffer.Bytes(), []byte("Error forwarding message")) {
		t.Errorf("Expected network error to be logged, but it wasn't. Log: %s", logBuffer.String())
	}
}

// roundTripperFunc is a helper type to allow a function to implement http.RoundTripper.
type roundTripperFunc func(*http.Request) (*http.Response, error)

func (f roundTripperFunc) RoundTrip(req *http.Request) (*http.Response, error) {
	return f(req)
}

func TestDelayedForward_TargetReturnsError(t *testing.T) {
	// Create a mock HTTP server for the target_url that returns an error status
	targetServerCalled := make(chan bool, 1)
	targetServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
		w.Write([]byte("Internal Server Error from Target"))
		targetServerCalled <- true
	}))
	defer targetServer.Close()

	mockSleeper := func(d time.Duration) {} // No actual sleep

	var logBuffer bytes.Buffer
	log.SetOutput(&logBuffer)
	defer log.SetOutput(ioutil.Discard)

	delayedForward("error message", targetServer.URL, 1*time.Millisecond, mockSleeper)

	select {
	case <-targetServerCalled:
		// Target server was hit
	case <-time.After(1 * time.Second):
		t.Fatal("Delayed message was not forwarded to target server")
	}

	// Verify that the failure was logged
	if !bytes.Contains(logBuffer.Bytes(), []byte("Failed to forward message to")) ||
		!bytes.Contains(logBuffer.Bytes(), []byte("Status: 500 Internal Server Error")) ||
		!bytes.Contains(logBuffer.Bytes(), []byte("Body: Internal Server Error from Target")) {
		t.Errorf("Expected target server error to be logged, but it wasn't. Log: %s", logBuffer.String())
	}
}

func TestRelayHandler_DefaultDelay(t *testing.T) {
	targetServerCalled := make(chan bool, 1)
	targetServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		targetServerCalled <- true
	}))
	defer targetServer.Close()

	sleepDone := make(chan time.Duration, 1)
	mockSleeper := func(d time.Duration) {
		sleepDone <- d
	}
	originalSleeper := defaultSleeper
	defaultSleeper = mockSleeper
	defer func() { defaultSleeper = originalSleeper }()

	relayReqBody := RelayRequest{
		Message:   "default delay test",
		TargetURL: targetServer.URL,
		// DelayMs is omitted, should default to 100ms
	}
	jsonBody, _ := json.Marshal(relayReqBody)
	req := httptest.NewRequest(http.MethodPost, "/relay", bytes.NewBuffer(jsonBody))
	req.Header.Set("Content-Type", "application/json")

	rr := httptest.NewRecorder()
	relayHandler(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	// Verify the mock sleeper was called with the default delay
	select {
	case d := <-sleepDone:
		if d != 100*time.Millisecond {
			t.Errorf("Expected sleeper to be called with 100ms default, got %v", d)
		}
	case <-time.After(1 * time.Second):
		t.Fatal("Mock sleeper was not called for default delay test")
	}

	select {
	case <-targetServerCalled:
	case <-time.After(1 * time.Second):
		t.Fatal("Delayed message was not forwarded to target server for default delay test")
	}
}
