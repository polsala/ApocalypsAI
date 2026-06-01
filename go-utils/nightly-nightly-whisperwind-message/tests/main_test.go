package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
	"time"
)

// Mock rationale: We need to test the relay logic without making actual network calls
// to external services. httptest.NewServer allows us to create local, in-memory
// HTTP servers that simulate target endpoints, providing deterministic responses.

func TestRelayHandler_SingleSuccess(t *testing.T) {
	// Mock rationale: Simulate a successful target endpoint.
	mockServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			t.Errorf("Expected POST, got %s", r.Method)
		}
		body, _ := ioutil.ReadAll(r.Body)
		if string(body) != `{"data":"test"}` {
			t.Errorf("Expected body '{\"data\":\"test\"}', got '%s'", string(body))
		}
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, `{"status":"received"}`)
	}))
	defer mockServer.Close()

	os.Setenv("TARGET_URLS", mockServer.URL)
	defer os.Unsetenv("TARGET_URLS")

	// Re-initialize targetURLs after setting env var for test
	loadTargetURLsFromEnv()

	reqBody := `{"message":{"data":"test"}}`
	req := httptest.NewRequest(http.MethodPost, "/relay", bytes.NewBufferString(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rr := httptest.NewRecorder()

	relayHandler(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	var resp RelayResponse
	err := json.NewDecoder(rr.Body).Decode(&resp)
	if err != nil {
		t.Fatalf("Could not decode response: %v", err)
	}

	if len(resp.Results) != 1 {
		t.Fatalf("Expected 1 relay result, got %d", len(resp.Results))
	}

	result := resp.Results[0]
	if result.URL != mockServer.URL {
		t.Errorf("Expected URL %s, got %s", mockServer.URL, result.URL)
	}
	if result.Status != "success" {
		t.Errorf("Expected status 'success', got '%s'", result.Status)
	}
	if result.Error != "" {
		t.Errorf("Expected no error, got '%s'", result.Error)
	}
}

func TestRelayHandler_MultipleTargets(t *testing.T) {
	// Mock rationale: Simulate multiple target endpoints, some succeeding, some failing.
	mockServer1 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, `{"status":"received1"}`)
	}))
	defer mockServer1.Close()

	mockServer2 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprint(w, `{"error":"internal error"}`)
	}))
	defer mockServer2.Close()

	mockServer3 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusAccepted)
		fmt.Fprint(w, `{"status":"received3"}`)
	}))
	defer mockServer3.Close()

	os.Setenv("TARGET_URLS", fmt.Sprintf("%s,%s,%s", mockServer1.URL, mockServer2.URL, mockServer3.URL))
	defer os.Unsetenv("TARGET_URLS")

	// Re-initialize targetURLs after setting env var for test
	loadTargetURLsFromEnv()

	reqBody := `{"message":{"event":"test_multi"}}`
	req := httptest.NewRequest(http.MethodPost, "/relay", bytes.NewBufferString(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rr := httptest.NewRecorder()

	relayHandler(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	var resp RelayResponse
	err := json.NewDecoder(rr.Body).Decode(&resp)
	if err != nil {
		t.Fatalf("Could not decode response: %v", err)
	}

	if len(resp.Results) != 3 {
		t.Fatalf("Expected 3 relay results, got %d", len(resp.Results))
	}

	// Check results, order might vary due to concurrency
	resultsMap := make(map[string]RelayResult)
	for _, r := range resp.Results {
		resultsMap[r.URL] = r
	}

	// Check mockServer1 (success)
	res1, ok := resultsMap[mockServer1.URL]
	if !ok || res1.Status != "success" || res1.Error != "" {
		t.Errorf("Expected %s to be success, got %+v", mockServer1.URL, res1)
	}

	// Check mockServer2 (failure)
	res2, ok := resultsMap[mockServer2.URL]
	if !ok || res2.Status != "failed" || !strings.Contains(res2.Error, "Target responded with status 500") {
		t.Errorf("Expected %s to be failed with 500 error, got %+v", mockServer2.URL, res2)
	}

	// Check mockServer3 (success)
	res3, ok := resultsMap[mockServer3.URL]
	if !ok || res3.Status != "success" || res3.Error != "" {
		t.Errorf("Expected %s to be success, got %+v", mockServer3.URL, res3)
	}
}

func TestRelayHandler_NoTargetsConfigured(t *testing.T) {
	os.Setenv("TARGET_URLS", "") // Ensure no targets are configured
	defer os.Unsetenv("TARGET_URLS")

	// Re-initialize targetURLs after setting env var for test
	loadTargetURLsFromEnv()

	reqBody := `{"message":{"data":"no_targets"}}`
	req := httptest.NewRequest(http.MethodPost, "/relay", bytes.NewBufferString(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rr := httptest.NewRecorder()

	relayHandler(rr, req)

	if status := rr.Code; status != http.StatusOK { // Still 200 OK, but with a skipped message
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	var resp RelayResponse
	err := json.NewDecoder(rr.Body).Decode(&resp)
	if err != nil {
		t.Fatalf("Could not decode response: %v", err)
	}

	if len(resp.Results) != 1 {
		t.Fatalf("Expected 1 relay result (skipped), got %d", len(resp.Results))
	}

	result := resp.Results[0]
	if result.Status != "skipped" {
		t.Errorf("Expected status 'skipped', got '%s'", result.Status)
	}
	if !strings.Contains(result.Error, "No target URLs configured") {
		t.Errorf("Expected error about no targets, got '%s'", result.Error)
	}
}

func TestRelayHandler_InvalidJson(t *testing.T) {
	os.Setenv("TARGET_URLS", "http://localhost:9999") // Dummy target, won't be hit
	defer os.Unsetenv("TARGET_URLS")
	loadTargetURLsFromEnv()

	reqBody := `{"message": "invalid json` // Malformed JSON
	req := httptest.NewRequest(http.MethodPost, "/relay", bytes.NewBufferString(reqBody))
	req.Header.Set("Content-Type", "application/json")
	rr := httptest.NewRecorder()

	relayHandler(rr, req)

	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusBadRequest)
	}
	if !strings.Contains(rr.Body.String(), "Invalid JSON request body") {
		t.Errorf("Expected error message about invalid JSON, got '%s'", rr.Body.String())
	}
}

func TestRelayHandler_MethodNotAllowed(t *testing.T) {
	os.Setenv("TARGET_URLS", "http://localhost:9999") // Dummy target
	defer os.Unsetenv("TARGET_URLS")
	loadTargetURLsFromEnv()

	req := httptest.NewRequest(http.MethodGet, "/relay", nil) // GET request
	rr := httptest.NewRecorder()

	relayHandler(rr, req)

	if status := rr.Code; status != http.StatusMethodNotAllowed {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusMethodNotAllowed)
	}
	if !strings.Contains(rr.Body.String(), "Only POST requests are accepted") {
		t.Errorf("Expected error message about method not allowed, got '%s'", rr.Body.String())
	}
}

func TestRelayMessage_NetworkError(t *testing.T) {
	// Mock rationale: Simulate a target that is unreachable or causes a network error.
	// We can achieve this by using a non-existent URL or closing the server immediately.
	// For simplicity, we'll use a URL that won't resolve or connect.
	unreachableURL := "http://localhost:12345" // Assuming nothing is listening here

	message := []byte(`{"data":"network_test"}`)
	result := relayMessage(unreachableURL, message)

	if result.URL != unreachableURL {
		t.Errorf("Expected URL %s, got %s", unreachableURL, result.URL)
	}
	if result.Status != "failed" {
		t.Errorf("Expected status 'failed', got '%s'", result.Status)
	}
	if !strings.Contains(result.Error, "Network error") {
		t.Errorf("Expected network error, got '%s'", result.Error)
	}
}

func TestRelayMessage_Timeout(t *testing.T) {
	// Mock rationale: Simulate a target that takes too long to respond, triggering a timeout.
	mockServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(6 * time.Second) // Longer than the 5-second client timeout
		w.WriteHeader(http.StatusOK)
	}))
	defer mockServer.Close()

	message := []byte(`{"data":"timeout_test"}`)
	result := relayMessage(mockServer.URL, message)

	if result.URL != mockServer.URL {
		t.Errorf("Expected URL %s, got %s", mockServer.URL, result.URL)
	}
	if result.Status != "failed" {
		t.Errorf("Expected status 'failed', got '%s'", result.Status)
	}
	if !strings.Contains(result.Error, "Client.Timeout exceeded") && !strings.Contains(result.Error, "context deadline exceeded") {
		t.Errorf("Expected timeout error, got '%s'", result.Error)
	}
}
