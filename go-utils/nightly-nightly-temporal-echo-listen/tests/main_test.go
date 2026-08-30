package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"
	"time"
)

// Mock rationale: We use httptest.NewServer to create a mock HTTP server
// that allows us to test the handlers without binding to a real port,
// ensuring deterministic and offline tests. The EchoStore itself is
// an in-memory structure, so no external dependencies need mocking.

func TestEchoHandler(t *testing.T) {
	store := &EchoStore{echoes: make([]Echo, 0)}
	handler := echoHandler(store)

	// Test POST request
	echoPayload := Echo{Source: "Past-Node-X", Message: "Hello from the past!"}
	body, _ := json.Marshal(echoPayload)
	req := httptest.NewRequest(http.MethodPost, "/echo", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	rr := httptest.NewRecorder()

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusAccepted {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusAccepted)
	}

	if len(store.GetEchoes()) != 1 {
		t.Errorf("expected 1 echo, got %d", len(store.GetEchoes()))
	}

	// Test non-POST request
	req = httptest.NewRequest(http.MethodGet, "/echo", nil)
	rr = httptest.NewRecorder()
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusMethodNotAllowed {
		t.Errorf("handler returned wrong status code for GET: got %v want %v",
			status, http.StatusMethodNotAllowed)
	}
}

func TestSummaryHandler(t *testing.T) {
	store := &EchoStore{echoes: make([]Echo, 0)}
	handler := summaryHandler(store)

	// Add some test echoes
	store.AddEcho(Echo{Source: "Future-Node-Y", Message: "The future is bright!", Timestamp: time.Now().Add(-1 * time.Hour)})
	store.AddEcho(Echo{Source: "Present-Observer", Message: "All clear.", Timestamp: time.Now()})

	req := httptest.NewRequest(http.MethodGet, "/summary", nil)
	rr := httptest.NewRecorder()

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	var echoes []Echo
	err := json.NewDecoder(rr.Body).Decode(&echoes)
	if err != nil {
		t.Fatalf("could not decode response: %v", err)
	}

	if len(echoes) != 2 {
		t.Errorf("expected 2 echoes in summary, got %d", len(echoes))
	}

	if echoes[0].Source != "Future-Node-Y" {
		t.Errorf("expected first echo source 'Future-Node-Y', got '%s'", echoes[0].Source)
	}

	// Test non-GET request
	req = httptest.NewRequest(http.MethodPost, "/summary", nil)
	rr = httptest.NewRecorder()
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusMethodNotAllowed {
		t.Errorf("handler returned wrong status code for POST: got %v want %v",
			status, http.StatusMethodNotAllowed)
	}
}

func TestConcurrency(t *testing.T) {
	store := &EchoStore{echoes: make([]Echo, 0)}
	echoHandlerFunc := echoHandler(store)
	summaryHandlerFunc := summaryHandler(store)

	numEchoes := 100
	var wg sync.WaitGroup
	wg.Add(numEchoes)

	for i := 0; i < numEchoes; i++ {
		go func(i int) {
			defer wg.Done()
			echoPayload := Echo{Source: fmt.Sprintf("Temporal-Drifter-%d", i), Message: fmt.Sprintf("Echo %d", i)}
			body, _ := json.Marshal(echoPayload)
			req := httptest.NewRequest(http.MethodPost, "/echo", bytes.NewReader(body))
			req.Header.Set("Content-Type", "application/json")
			rr := httptest.NewRecorder()
			echoHandlerFunc.ServeHTTP(rr, req)
			if rr.Code != http.StatusAccepted {
				t.Errorf("concurrent echo %d failed with status %v", i, rr.Code)
			}
		}(i)
	}
	wg.Wait()

	// Check if all echoes were added
	req := httptest.NewRequest(http.MethodGet, "/summary", nil)
	rr := httptest.NewRecorder()
	summaryHandlerFunc.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Fatalf("summary handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	var echoes []Echo
	err := json.NewDecoder(rr.Body).Decode(&echoes)
	if err != nil {
		t.Fatalf("could not decode summary response: %v", err)
	}

	if len(echoes) != numEchoes {
		t.Errorf("expected %d echoes after concurrent adds, got %d", numEchoes, len(echoes))
	}
}
