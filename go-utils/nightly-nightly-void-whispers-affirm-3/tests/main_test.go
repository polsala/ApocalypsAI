package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

// Mock rationale: Simulates HTTP request to affirmation endpoint without external dependencies.
func TestAffirmationHandler(t *testing.T) {
	req := httptest.NewRequest("GET", "/affirmation", nil)
	w := httptest.NewRecorder()

	affirmationHandler(w, req)

	resp := w.Result()
	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}

	var body AffirmationResponse
	if err := json.NewDecoder(resp.Body).Decode(&body); err != nil {
		t.Fatalf("Failed to decode response: %v", err)
	}

	if body.Message == "" {
		t.Error("Expected non-empty message")
	}
}
