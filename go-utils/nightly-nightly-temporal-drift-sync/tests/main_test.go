package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

// TestDriftManager_AddDriftAndGetConsensus tests adding drifts and getting consensus.
func TestDriftManager_AddDriftAndGetConsensus(t *testing.T) {
	dm := NewDriftManager()

	// Test with no drifts
	if dm.GetConsensusDrift() != 0.0 {
		t.Errorf("Expected 0.0 consensus drift for empty manager, got %f", dm.GetConsensusDrift())
	}

	// Add first drift
	dm.AddDrift("node-1", 0.1)
	if dm.GetConsensusDrift() != 0.1 {
		t.Errorf("Expected 0.1 consensus drift, got %f", dm.GetConsensusDrift())
	}

	// Add second drift
	dm.AddDrift("node-2", 0.2)
	// Expected average: (0.1 + 0.2) / 2 = 0.15
	if dm.GetConsensusDrift() != 0.15 {
		t.Errorf("Expected 0.15 consensus drift, got %f", dm.GetConsensusDrift())
	}

	// Update existing drift
	dm.AddDrift("node-1", 0.3)
	// Expected average: (0.3 + 0.2) / 2 = 0.25
	if dm.GetConsensusDrift() != 0.25 {
		t.Errorf("Expected 0.25 consensus drift after update, got %f", dm.GetConsensusDrift())
	}

	// Add a negative drift
	dm.AddDrift("node-3", -0.1)
	// Expected average: (0.3 + 0.2 - 0.1) / 3 = 0.4 / 3 = 0.1333...
	expected := 0.4 / 3.0
	if dm.GetConsensusDrift() != expected {
		t.Errorf("Expected %f consensus drift, got %f", expected, dm.GetConsensusDrift())
	}
}

// TestHandleReportDrift tests the HTTP handler for reporting drift.
func TestHandleReportDrift(t *testing.T) {
	dm := NewDriftManager() // # Mock rationale: Using an in-memory DriftManager for isolated testing.

	// Test valid report
	report := DriftReport{NodeID: "test-node-1", DriftValue: 0.5}
	body, _ := json.Marshal(report)
	req := httptest.NewRequest(http.MethodPost, "/report-drift", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	rr := httptest.NewRecorder()

	handleReportDrift(dm, rr, req)

	if status := rr.Code; status != http.StatusAccepted {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusAccepted)
	}
	if dm.GetConsensusDrift() != 0.5 {
		t.Errorf("Expected drift 0.5, got %f", dm.GetConsensusDrift())
	}

	// Test invalid method
	req = httptest.NewRequest(http.MethodGet, "/report-drift", nil)
	rr = httptest.NewRecorder()
	handleReportDrift(dm, rr, req)
	if status := rr.Code; status != http.StatusMethodNotAllowed {
		t.Errorf("handler returned wrong status code for GET: got %v want %v", status, http.StatusMethodNotAllowed)
	}

	// Test invalid JSON payload
	req = httptest.NewRequest(http.MethodPost, "/report-drift", bytes.NewBufferString("{invalid json"))
	req.Header.Set("Content-Type", "application/json")
	rr = httptest.NewRecorder()
	handleReportDrift(dm, rr, req)
	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code for invalid JSON: got %v want %v", status, http.StatusBadRequest)
	}

	// Test empty NodeID
	report = DriftReport{NodeID: "", DriftValue: 0.1}
	body, _ = json.Marshal(report)
	req = httptest.NewRequest(http.MethodPost, "/report-drift", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	rr = httptest.NewRecorder()
	handleReportDrift(dm, rr, req)
	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code for empty NodeID: got %v want %v", status, http.StatusBadRequest)
	}
}

// TestHandleGetConsensus tests the HTTP handler for getting consensus drift.
func TestHandleGetConsensus(t *testing.T) {
	dm := NewDriftManager(); // # Mock rationale: Using an in-memory DriftManager for isolated testing.
	dm.AddDrift("node-a", 0.1)
	dm.AddDrift("node-b", 0.2)

	// Test valid GET request
	req := httptest.NewRequest(http.MethodGet, "/consensus-drift", nil)
	rr := httptest.NewRecorder()

	handleGetConsensus(dm, rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	var response ConsensusResponse
	if err := json.NewDecoder(rr.Body).Decode(&response); err != nil {
		t.Fatalf("Could not decode response: %v", err)
	}

	expectedConsensus := (0.1 + 0.2) / 2.0
	if response.ConsensusDrift != expectedConsensus {
		t.Errorf("Expected consensus drift %f, got %f", expectedConsensus, response.ConsensusDrift)
	}

	// Test invalid method
	req = httptest.NewRequest(http.MethodPost, "/consensus-drift", nil)
	rr = httptest.NewRecorder()
	handleGetConsensus(dm, rr, req)
	if status := rr.Code; status != http.StatusMethodNotAllowed {
		t.Errorf("handler returned wrong status code for POST: got %v want %v", status, http.StatusMethodNotAllowed)
	}
}

// TestHandleGetConsensus_EmptyDrifts tests getting consensus when no drifts are reported.
func TestHandleGetConsensus_EmptyDrifts(t *testing.T) {
	dm := NewDriftManager(); // # Mock rationale: Using an in-memory DriftManager for isolated testing.

	req := httptest.NewRequest(http.MethodGet, "/consensus-drift", nil)
	rr := httptest.NewRecorder()

	handleGetConsensus(dm, rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	var response ConsensusResponse
	if err := json.NewDecoder(rr.Body).Decode(&response); err != nil {
		t.Fatalf("Could not decode response: %v", err)
	}

	if response.ConsensusDrift != 0.0 {
		t.Errorf("Expected consensus drift 0.0 for empty manager, got %f", response.ConsensusDrift)
	}
}
