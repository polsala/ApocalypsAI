package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strconv"
	"testing"
	"time"
)

// Mock rationale: We use httptest.NewRecorder and httptest.NewRequest to create
// isolated, in-memory HTTP request/response cycles. This allows us to test the
// handlers' logic and HTTP responses without needing to bind to a real network
// port or make external network calls. The time.Now() calls are part of the
// handler's core logic and are implicitly "mocked" by controlling the test
// execution environment and checking relative time within a small tolerance.

func TestTimeHandlerNoDrift(t *testing.T) {
	req, err := http.NewRequest("GET", "/time", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(timeHandler)

	// Capture time before handler call to compare
	expectedTime := time.Now().UTC()

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	var response TimeResponse
	err = json.Unmarshal(rr.Body.Bytes(), &response)
	if err != nil {
		t.Fatalf("could not unmarshal response: %v", err)
	}

	parsedTime, err := time.Parse(time.RFC3339Nano, response.Timestamp)
	if err != nil {
		t.Fatalf("could not parse timestamp: %v", err)
	}

	// Allow a small margin for execution time difference
	if parsedTime.Before(expectedTime.Add(-10*time.Millisecond)) || parsedTime.After(expectedTime.Add(10*time.Millisecond)) {
		t.Errorf("handler returned unexpected timestamp: got %v, expected around %v",
			parsedTime, expectedTime)
	}
	if response.DriftMs != 0 {
		t.Errorf("handler returned unexpected drift_ms: got %v, want %v",
			response.DriftMs, 0)
	}
	if response.Message == "" {
		t.Errorf("handler returned empty message")
	}
}

func TestTimeHandlerPositiveDrift(t *testing.T) {
	drift := 1000 // 1 second
	req, err := http.NewRequest("GET", "/time?drift_ms="+strconv.Itoa(drift), nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(timeHandler)

	expectedTimeBase := time.Now().UTC()
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	var response TimeResponse
	err = json.Unmarshal(rr.Body.Bytes(), &response)
	if err != nil {
		t.Fatalf("could not unmarshal response: %v", err)
	}

	parsedTime, err := time.Parse(time.RFC3339Nano, response.Timestamp)
	if err != nil {
		t.Fatalf("could not parse timestamp: %v", err)
	}

	expectedDriftedTime := expectedTimeBase.Add(time.Duration(drift) * time.Millisecond)

	if parsedTime.Before(expectedDriftedTime.Add(-10*time.Millisecond)) || parsedTime.After(expectedDriftedTime.Add(10*time.Millisecond)) {
		t.Errorf("handler returned unexpected drifted timestamp: got %v, expected around %v",
			parsedTime, expectedDriftedTime)
	}
	if response.DriftMs != drift {
		t.Errorf("handler returned unexpected drift_ms: got %v, want %v",
			response.DriftMs, drift)
	}
}

func TestTimeHandlerNegativeDrift(t *testing.T) {
	drift := -500 // -0.5 seconds
	req, err := http.NewRequest("GET", "/time?drift_ms="+strconv.Itoa(drift), nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(timeHandler)

	expectedTimeBase := time.Now().UTC()
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	var response TimeResponse
	err = json.Unmarshal(rr.Body.Bytes(), &response)
	if err != nil {
		t.Fatalf("could not unmarshal response: %v", err)
	}

	parsedTime, err := time.Parse(time.RFC3339Nano, response.Timestamp)
	if err != nil {
		t.Fatalf("could not parse timestamp: %v", err)
	}

	expectedDriftedTime := expectedTimeBase.Add(time.Duration(drift) * time.Millisecond)

	if parsedTime.Before(expectedDriftedTime.Add(-10*time.Millisecond)) || parsedTime.After(expectedDriftedTime.Add(10*time.Millisecond)) {
		t.Errorf("handler returned unexpected drifted timestamp: got %v, expected around %v",
			parsedTime, expectedDriftedTime)
	}
	if response.DriftMs != drift {
		t.Errorf("handler returned unexpected drift_ms: got %v, want %v",
			response.DriftMs, drift)
	}
}

func TestTimeHandlerInvalidDrift(t *testing.T) {
	req, err := http.NewRequest("GET", "/time?drift_ms=notanumber", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(timeHandler)

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code for invalid drift: got %v want %v",
			status, http.StatusBadRequest)
	}

	expected := `{"error": "Invalid drift_ms parameter. Must be an integer."}` + "\n" // http.Error adds a newline
	if rr.Body.String() != expected {
		t.Errorf("handler returned unexpected body for invalid drift: got %q want %q",
			rr.Body.String(), expected)
	}
}

func TestStatusHandler(t *testing.T) {
	// Initialize startTime for statusHandler, as it's a global variable set in main
	// For tests, we need to ensure it's set before calling the handler.
	startTime = time.Now()

	req, err := http.NewRequest("GET", "/status", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(statusHandler)

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	var response map[string]string
	err = json.Unmarshal(rr.Body.Bytes(), &response)
	if err != nil {
		t.Fatalf("could not unmarshal response: %v", err)
	}

	if response["status"] != "Operational" {
		t.Errorf("handler returned unexpected status: got %v, want %v",
			response["status"], "Operational")
	}
	if response["message"] == "" {
		t.Errorf("handler returned empty message")
	}
	if _, ok := response["uptime"]; !ok {
		t.Errorf("handler did not return uptime")
	}
}
