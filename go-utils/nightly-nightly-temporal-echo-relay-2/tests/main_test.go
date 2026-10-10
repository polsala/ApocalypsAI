package main

import (
	"bytes"
	"encoding/json"
	"math/rand"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

// mockSleeper implements the sleeper interface for testing
type mockSleeper struct {
	sleptFor time.Duration
}

func (ms *mockSleeper) Sleep(d time.Duration) {
	// # Mock rationale: Prevents actual time.Sleep calls during tests, making them fast and deterministic.
	ms.sleptFor = d
}

// TestCorruptMessage_NoCorruption tests with corruption level 0
func TestCorruptMessage_NoCorruption(t *testing.T) {
	msg := "Hello World"
	r := rand.New(rand.NewSource(0)) // # Mock rationale: Deterministic random source for repeatable tests.
	corrupted := corruptMessage(msg, 0.0, r)
	if corrupted != msg {
		t.Errorf("Expected no corruption for level 0.0, got %s", corrupted)
	}
}

// TestCorruptMessage_FullCorruption_Deterministic tests with corruption level 1 and a fixed seed
func TestCorruptMessage_FullCorruption_Deterministic(t *testing.T) {
	msg := "abcde"
	// With seed 0, level 1.0, and the current corruption logic:
	// i=0, 'a': r.Intn(3) -> 1 (swap). runes becomes ['b', 'a', 'c', 'd', 'e']. i becomes 1.
	// i=1, 'a': r.Intn(3) -> 0 (case change). runes[1] becomes 'A'. runes becomes ['b', 'A', 'c', 'd', 'e'].
	// i=2, 'c': r.Intn(3) -> 2 (replace). runes[2] becomes '!' (r.Intn(94)+33 for seed 2 is 33+1 = 34, which is '!'). runes becomes ['b', 'A', '!', 'd', 'e'].
	// i=3, 'd': r.Intn(3) -> 1 (swap). runes becomes ['b', 'A', '!', 'e', 'd']. i becomes 4.
	// i=4, 'd': r.Intn(3) -> 0 (case change). runes[4] becomes 'D'. runes becomes ['b', 'A', '!', 'e', 'D'].
	// Expected output: "bA!eD"
	
	r := rand.New(rand.NewSource(0)) // # Mock rationale: Deterministic random source for repeatable tests.
	corrupted := corruptMessage(msg, 1.0, r)

	if corrupted != "bA!eD" {
		t.Errorf("Expected specific corruption for '%s' with seed 0, got '%s'", msg, corrupted)
	}

	// Length should remain the same
	if len(corrupted) != len(msg) {
		t.Errorf("Expected corrupted message length to be %d, got %d", len(msg), len(corrupted))
	}
}

// TestEchoHandler_Success tests a successful echo request
func TestEchoHandler_Success(t *testing.T) {
	mockS := &mockSleeper{} // # Mock rationale: Prevents actual time.Sleep calls during tests, making them fast and deterministic.
	// Use a specific seed for rand to make corruption deterministic for this test.
	r := rand.New(rand.NewSource(100)) // # Mock rationale: Deterministic random source for repeatable tests.

	payload := RequestPayload{
		Message:        "Test Message for Echo",
		DelayMs:        50,
		CorruptionLevel: 0.5,
	}
	body, _ := json.Marshal(payload)
	req := httptest.NewRequest(http.MethodPost, "/echo", bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")

	rr := httptest.NewRecorder()
	handler := echoHandler(mockS, r)
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	var response ResponsePayload
	err := json.NewDecoder(rr.Body).Decode(&response)
	if err != nil {
		t.Fatalf("Could not decode response: %v", err)
	}

	if response.OriginalMessage != payload.Message {
		t.Errorf("handler returned wrong original message: got %v want %v",
			response.OriginalMessage, payload.Message)
	}

	if response.DelayAppliedMs != payload.DelayMs {
		t.Errorf("handler returned wrong delay applied: got %v want %v",
			response.DelayAppliedMs, payload.DelayMs)
	}

	// To test the corrupted message deterministically, we call corruptMessage with the same parameters.
	// This ensures the test is robust against changes in the corruption logic as long as the seed is consistent.
	expectedCorrupted := corruptMessage(payload.Message, payload.CorruptionLevel, rand.New(rand.NewSource(100)))
	if response.CorruptedMessage != expectedCorrupted {
		t.Errorf("handler returned wrong corrupted message: got '%v' want '%v'",
			response.CorruptedMessage, expectedCorrupted)
	}

	if mockS.sleptFor != time.Duration(payload.DelayMs)*time.Millisecond {
		t.Errorf("mockSleeper did not sleep for expected duration: got %v want %v",
			mockS.sleptFor, time.Duration(payload.DelayMs)*time.Millisecond)
	}
}

// TestEchoHandler_InvalidMethod tests non-POST requests
func TestEchoHandler_InvalidMethod(t *testing.T) {
	mockS := &mockSleeper{} // # Mock rationale: Prevents actual time.Sleep calls during tests.
	r := rand.New(rand.NewSource(0)) // # Mock rationale: Deterministic random source for repeatable tests.

	req := httptest.NewRequest(http.MethodGet, "/echo", nil)
	rr := httptest.NewRecorder()
	handler := echoHandler(mockS, r)
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusMethodNotAllowed {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusMethodNotAllowed)
	}
	if !strings.Contains(rr.Body.String(), "Only POST requests are accepted") {
		t.Errorf("handler returned unexpected body: %v", rr.Body.String())
	}
}

// TestEchoHandler_InvalidPayload tests malformed JSON
func TestEchoHandler_InvalidPayload(t *testing.T) {
	mockS := &mockSleeper{} // # Mock rationale: Prevents actual time.Sleep calls during tests.
	r := rand.New(rand.NewSource(0)) // # Mock rationale: Deterministic random source for repeatable tests.

	req := httptest.NewRequest(http.MethodPost, "/echo", bytes.NewBufferString("{invalid json}"))
	req.Header.Set("Content-Type", "application/json")
	rr := httptest.NewRecorder()
	handler := echoHandler(mockS, r)
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusBadRequest)
	}
	if !strings.Contains(rr.Body.String(), "Invalid request payload") {
		t.Errorf("handler returned unexpected body: %v", rr.Body.String())
	}
}
