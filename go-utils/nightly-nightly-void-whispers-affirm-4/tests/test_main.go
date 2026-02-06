package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

// Mock rationale: Simulates HTTP requests without needing a live server.
func TestAffirmationHandler(t *testing.T) {
	req, err := http.NewRequest("GET", "/affirmation", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(affirmationHandler)
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	var response AffirmationResponse
	if err := json.NewDecoder(rr.Body).Decode(&response); err != nil {
		t.Errorf("could not decode response: %v", err)
	}

	if response.Affirmation == "" {
		t.Errorf("expected affirmation, got empty string")
	}
}
