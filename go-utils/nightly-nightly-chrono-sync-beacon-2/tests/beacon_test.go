package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

// Mock rationale: httptest.NewRecorder and http.HandlerFunc allow us to test the HTTP handler logic
// directly without starting a full HTTP server or making actual network calls. This ensures
// deterministic and offline execution of tests.
func TestTimeHandler(t *testing.T) {
	req, err := http.NewRequest("GET", "/time", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(timeHandler) // Use the handler directly

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	var response TimeResponse
	err = json.NewDecoder(rr.Body).Decode(&response)
	if err != nil {
		t.Fatalf("could not decode response: %v", err)
	}

	// Check temporal status
	expectedStatus := "Temporal flow is stable. All systems nominal."
	if response.TemporalStatus != expectedStatus {
		t.Errorf("handler returned unexpected temporal status: got %v want %v",
			response.TemporalStatus, expectedStatus)
	}

	// Check UTC time format and if it's a valid time
	parsedTime, err := time.Parse(time.RFC3339Nano, response.UTCTime)
	if err != nil {
		t.Errorf("handler returned invalid UTC time format: %v", err)
	}

	// Ensure the time is recent (within a reasonable margin of test execution)
	// This check is soft to account for minor test execution time variations.
	now := time.Now().UTC()
	// Allow up to 5 seconds difference for test execution overhead
	if parsedTime.After(now.Add(5*time.Second)) || parsedTime.Before(now.Add(-5*time.Second)) {
		t.Errorf("handler returned UTC time too far from current time: got %v, current %v", parsedTime, now)
	}
}
