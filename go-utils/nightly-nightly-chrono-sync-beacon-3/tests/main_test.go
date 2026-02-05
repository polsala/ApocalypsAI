package main

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"testing"
	"time"
)

// MockRoundTripper is a mock implementation of http.RoundTripper.
// # Mock rationale: This mock allows us to simulate HTTP responses with controlled delays and errors,
// # without making actual network calls, ensuring deterministic and fast tests.
type MockRoundTripper struct {
	Response *http.Response
	Error    error
	Delay    time.Duration
}

// RoundTrip implements the http.RoundTripper interface.
func (m *MockRoundTripper) RoundTrip(req *http.Request) (*http.Response, error) {
	if m.Delay > 0 {
		time.Sleep(m.Delay)
	}
	if m.Error != nil {
		return nil, m.Error
	}
	return m.Response, nil
}

// newMockClient creates an http.Client with a custom MockRoundTripper.
// # Mock rationale: Provides a controlled HTTP client for testing network interactions.
func newMockClient(statusCode int, body string, delay time.Duration, err error) *http.Client {
	resp := &http.Response{
		StatusCode: statusCode,
		Body:       io.NopCloser(bytes.NewBufferString(body)),
		Header:     make(http.Header),
	}
	return &http.Client{
		Transport: &MockRoundTripper{
			Response: resp,
			Error:    err,
			Delay:    delay,
		},
		Timeout: 10 * time.Second, // Set a reasonable timeout for the mock client
	}
}

func TestCheckTarget_TemporalHarmony(t *testing.T) {
	target := Target{URL: "http://example.com/fast", ExpectedMaxDurationMs: 100}
	client := newMockClient(200, "OK", 50*time.Millisecond, nil)

	result := checkTarget(client, target)

	if result.Status != "Temporal Harmony" {
		t.Errorf("Expected status 'Temporal Harmony', got '%s'", result.Status)
	}
	if result.Error != nil {
		t.Errorf("Expected no error, got '%v'", result.Error)
	}
	if result.Duration > 100*time.Millisecond {
		t.Errorf("Expected duration <= 100ms, got %v", result.Duration)
	}
}

func TestCheckTarget_SlightChronalAnomaly(t *testing.T) {
	target := Target{URL: "http://example.com/slow", ExpectedMaxDurationMs: 100}
	// Delay is 1.2x expected, which should be a slight anomaly (between 1x and 1.5x)
	client := newMockClient(200, "OK", 120*time.Millisecond, nil)

	result := checkTarget(client, target)

	if result.Status != "Slight Chronal Anomaly" {
		t.Errorf("Expected status 'Slight Chronal Anomaly', got '%s'", result.Status)
	}
	if result.Error != nil {
		t.Errorf("Expected no error, got '%v'", result.Error)
	}
	if result.Duration <= 100*time.Millisecond || result.Duration > time.Duration(target.ExpectedMaxDurationMs)*time.Millisecond*time.Duration(SevereDilationFactor) {
		t.Errorf("Expected duration between 100ms and %v, got %v", time.Duration(target.ExpectedMaxDurationMs)*time.Millisecond*time.Duration(SevereDilationFactor), result.Duration)
	}
}

func TestCheckTarget_SevereTimeDilation(t *testing.T) {
	target := Target{URL: "http://example.com/very-slow", ExpectedMaxDurationMs: 100}
	// Delay is 3.5x expected, which should be severe dilation (over 3x)
	client := newMockClient(200, "OK", 350*time.Millisecond, nil)

	result := checkTarget(client, target)

	if result.Status != "Severe Time Dilation" {
		t.Errorf("Expected status 'Severe Time Dilation', got '%s'", result.Status)
	}
	if result.Error != nil {
		t.Errorf("Expected no error, got '%v'", result.Error)
	}
	if result.Duration <= time.Duration(target.ExpectedMaxDurationMs)*time.Millisecond*time.Duration(SevereDilationFactor) {
		t.Errorf("Expected duration > %v, got %v", time.Duration(target.ExpectedMaxDurationMs)*time.Millisecond*time.Duration(SevereDilationFactor), result.Duration)
	}
}

func TestCheckTarget_LostInTheVoid_ConnectionError(t *testing.T) {
	target := Target{URL: "http://nonexistent.local", ExpectedMaxDurationMs: 50}
	client := newMockClient(0, "", 0, fmt.Errorf("dial tcp: lookup nonexistent.local: no such host"))

	result := checkTarget(client, target)

	if result.Status != "Lost in the Void" {
		t.Errorf("Expected status 'Lost in the Void', got '%s'", result.Status)
	}
	if result.Error == nil {
		t.Errorf("Expected an error, got nil")
	}
}

func TestCheckTarget_LostInTheVoid_RequestCreationError(t *testing.T) {
	// Invalid URL to trigger request creation error
	target := Target{URL: "://invalid-url", ExpectedMaxDurationMs: 50}
	client := newMockClient(0, "", 0, nil)

	result := checkTarget(client, target)

	if result.Status != "Lost in the Void" {
		t.Errorf("Expected status 'Lost in the Void', got '%s'", result.Status)
	}
	if result.Error == nil {
		t.Errorf("Expected an error, got nil")
	}
	if result.Error.Error() != "failed to create request: parse \"://invalid-url\": missing protocol scheme"
		{
		t.Errorf("Expected specific request creation error, got '%v'", result.Error)
	}
}

func TestCheckTarget_SlightChronalAnomaly_EdgeCase(t *testing.T) {
	target := Target{URL: "http://example.com/edge", ExpectedMaxDurationMs: 100}
	// Exactly 1.5x expected, should be Slight Chronal Anomaly
	client := newMockClient(200, "OK", 150*time.Millisecond, nil)

	result := checkTarget(client, target)

	if result.Status != "Slight Chronal Anomaly" {
		t.Errorf("Expected status 'Slight Chronal Anomaly', got '%s'", result.Status)
	}
}

func TestCheckTarget_SevereTimeDilation_EdgeCase(t *testing.T) {
	target := Target{URL: "http://example.com/edge-severe", ExpectedMaxDurationMs: 100}
	// Exactly 3.0x expected, should be Severe Time Dilation
	client := newMockClient(200, "OK", 300*time.Millisecond, nil)

	result := checkTarget(client, target)

	if result.Status != "Severe Time Dilation" {
		t.Errorf("Expected status 'Severe Time Dilation', got '%s'", result.Status)
	}
}
