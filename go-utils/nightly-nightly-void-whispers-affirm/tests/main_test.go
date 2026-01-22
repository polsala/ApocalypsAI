package tests

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"../src"
)

// Mock rationale: Simulate HTTP requests to test handler logic without starting a real server.
func TestAffirmationHandler(t *testing.T) {
	req := httptest.NewRequest("GET", "/affirmation", nil)
	w := httptest.NewRecorder()

	src.Handler(w, req)

	resp := w.Result()
	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}
}

func TestAffirmationWithVoidStyle(t *testing.T) {
	req := httptest.NewRequest("GET", "/affirmation?void=true", nil)
	w := httptest.NewRecorder()

	src.Handler(w, req)

	resp := w.Result()
	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}
}
