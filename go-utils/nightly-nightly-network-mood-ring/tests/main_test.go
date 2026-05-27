package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"
	"time"
)

// # Mock rationale:
// The tests use `httptest.NewRecorder` and `http.NewRequest` to simulate HTTP requests and responses
// without actually binding to a network port or making external calls. This ensures tests are
// deterministic, fast, and offline. Time.Now() is used for timestamps, which is acceptable as
// the exact time value isn't asserted, only its presence and update behavior.

func TestReportMoodHandler_Success(t *testing.T) {
	mr := NewMoodRing()

	// Test reporting a new mood
	reportPayload := []byte(`{"source": "test-service-1", "mood": "Optimistic"}`)
	req := httptest.NewRequest(http.MethodPost, "/report", bytes.NewBuffer(reportPayload))
	req.Header.Set("Content-Type", "application/json")
	rr := httptest.NewRecorder()

	mr.reportMoodHandler(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	expected := "Mood for test-service-1 updated to Optimistic\n"
	if rr.Body.String() != expected {
		t.Errorf("handler returned unexpected body: got %v want %v", rr.Body.String(), expected)
	}

	mr.mu.RLock()
	defer mr.mu.RUnlock()
	if len(mr.componentMoods) != 1 {
		t.Fatalf("Expected 1 mood report, got %d", len(mr.componentMoods))
	}
	if mood, ok := mr.componentMoods["test-service-1"]; !ok || mood.Mood != "Optimistic" {
		t.Errorf("Mood not correctly stored: got %+v", mood)
	}

	// Test updating an existing mood
	updatePayload := []byte(`{"source": "test-service-1", "mood": "Anxious"}`)
	req = httptest.NewRequest(http.MethodPost, "/report", bytes.NewBuffer(updatePayload))
	req.Header.Set("Content-Type", "application/json")
	rr = httptest.NewRecorder()

	mr.reportMoodHandler(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code for update: got %v want %v", status, http.StatusOK)
	}

	mr.mu.RLock()
	defer mr.mu.RUnlock()
	if len(mr.componentMoods) != 1 {
		t.Fatalf("Expected 1 mood report after update, got %d", len(mr.componentMoods))
	}
	if mood, ok := mr.componentMoods["test-service-1"]; !ok || mood.Mood != "Anxious" {
		t.Errorf("Mood not correctly updated: got %+v", mood)
	}
}

func TestReportMoodHandler_InvalidMethod(t *testing.T) {
	mr := NewMoodRing()
	req := httptest.NewRequest(http.MethodGet, "/report", nil)
	rr := httptest.NewRecorder()

	mr.reportMoodHandler(rr, req)

	if status := rr.Code; status != http.StatusMethodNotAllowed {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusMethodNotAllowed)
	}
}

func TestReportMoodHandler_InvalidBody(t *testing.T) {
	mr := NewMoodRing()
	req := httptest.NewRequest(http.MethodPost, "/report", bytes.NewBuffer([]byte(`invalid json`)))
	req.Header.Set("Content-Type", "application/json")
	rr := httptest.NewRecorder()

	mr.reportMoodHandler(rr, req)

	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusBadRequest)
	}
}

func TestReportMoodHandler_MissingFields(t *testing.T) {
	mr := NewMoodRing()

	// Missing source
	payload := []byte(`{"mood": "Optimistic"}`)
	req := httptest.NewRequest(http.MethodPost, "/report", bytes.NewBuffer(payload))
	req.Header.Set("Content-Type", "application/json")
	rr := httptest.NewRecorder()
	mr.reportMoodHandler(rr, req)
	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code for missing source: got %v want %v", status, http.StatusBadRequest)
	}

	// Missing mood
	payload = []byte(`{"source": "test-service-2"}`)
	req = httptest.NewRequest(http.MethodPost, "/report", bytes.NewBuffer(payload))
	req.Header.Set("Content-Type", "application/json")
	rr = httptest.NewRecorder()
	mr.reportMoodHandler(rr, req)
	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code for missing mood: got %v want %v", status, http.StatusBadRequest)
	}
}

func TestGetStatusHandler_Success(t *testing.T) {
	mr := NewMoodRing()

	// Report some moods first
	reportPayload1 := []byte(`{"source": "service-A", "mood": "Serene"}`)
	req1 := httptest.NewRequest(http.MethodPost, "/report", bytes.NewBuffer(reportPayload1))
	req1.Header.Set("Content-Type", "application/json")
	rr1 := httptest.NewRecorder()
	mr.reportMoodHandler(rr1, req1)

	reportPayload2 := []byte(`{"source": "service-B", "mood": "Chaotic"}`)
	req2 := httptest.NewRequest(http.MethodPost, "/report", bytes.NewBuffer(reportPayload2))
	req2.Header.Set("Content-Type", "application/json")
	rr2 := httptest.NewRecorder()
	mr.reportMoodHandler(rr2, req2)

	// Now get status
	req := httptest.NewRequest(http.MethodGet, "/status", nil)
	rr := httptest.NewRecorder()

	mr.getStatusHandler(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	var response map[string][]MoodReport
	if err := json.NewDecoder(rr.Body).Decode(&response); err != nil {
		t.Fatalf("Could not decode response: %v", err)
	}

	if len(response["component_moods"]) != 2 {
		t.Fatalf("Expected 2 component moods, got %d", len(response["component_moods"]))
	}

	// Due to sorting in the handler, service-A should be first
	if response["component_moods"][0].Source != "service-A" || response["component_moods"][0].Mood != "Serene" {
		t.Errorf("Expected service-A Serene, got %+v", response["component_moods"][0])
	}
	if response["component_moods"][1].Source != "service-B" || response["component_moods"][1].Mood != "Chaotic" {
		t.Errorf("Expected service-B Chaotic, got %+v", response["component_moods"][1])
	}

	// Test timestamp presence
	if response["component_moods"][0].Timestamp.IsZero() {
		t.Errorf("Timestamp for service-A is zero")
	}
}

func TestGetStatusHandler_NoMoods(t *testing.T) {
	mr := NewMoodRing()
	req := httptest.NewRequest(http.MethodGet, "/status", nil)
	rr := httptest.NewRecorder()

	mr.getStatusHandler(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	var response map[string][]MoodReport
	if err := json.NewDecoder(rr.Body).Decode(&response); err != nil {
		t.Fatalf("Could not decode response: %v", err)
	}

	if len(response["component_moods"]) != 0 {
		t.Errorf("Expected 0 component moods, got %d", len(response["component_moods"]))
	}
}

func TestGetStatusHandler_InvalidMethod(t *testing.T) {
	mr := NewMoodRing()
	req := httptest.NewRequest(http.MethodPost, "/status", nil)
	rr := httptest.NewRecorder()

	mr.getStatusHandler(rr, req)

	if status := rr.Code; status != http.StatusMethodNotAllowed {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusMethodNotAllowed)
	}
}

func TestMain(m *testing.M) {
	// Suppress log output during tests for cleaner test results
	log.SetOutput(bytes.NewBuffer(nil))
	os.Exit(m.Run())
}
