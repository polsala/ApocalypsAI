package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"reflect"
	"testing"
	"time"
)

// Mock rationale: We need to test the HTTP handler and the consensus logic
// without making actual network calls to NTP servers, which would be slow,
// non-deterministic, and require external network access. By replacing the
// `ntpQueryFunc` with a mock, we can control the exact responses from
// "NTP servers" for various test scenarios, ensuring deterministic and fast tests.

func TestSyncHandler_Success(t *testing.T) {
	// Save the original function and defer its restoration
	originalNTPQueryFunc := ntpQueryFunc
	defer func() { ntpQueryFunc = originalNTPQueryFunc }()

	// Mock ntpQueryFunc to return predefined times
	mockTimes := map[string]time.Time{
		"ntp1.example.com": time.Date(2023, time.October, 27, 10, 0, 0, 100000000, time.UTC),
		"ntp2.example.com": time.Date(2023, time.October, 27, 10, 0, 0, 300000000, time.UTC),
		"ntp3.example.com": time.Date(2023, time.October, 27, 10, 0, 0, 200000000, time.UTC),
	}
	ntpQueryFunc = func(serverAddr string) (time.Time, error) {
		if tm, ok := mockTimes[serverAddr]; ok {
			return tm, nil
		}
		return time.Time{}, fmt.Errorf("unknown mock server: %s", serverAddr)
	}

	// Set mock NTP servers for the test environment
	os.Setenv("CHRONOSYNC_NTP_SERVERS", "ntp1.example.com,ntp2.example.com,ntp3.example.com")
	defer os.Unsetenv("CHRONOSYNC_NTP_SERVERS")

	req, err := http.NewRequest("GET", "/sync", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(syncHandler)

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	var response SyncResponse
	err = json.Unmarshal(rr.Body.Bytes(), &response)
	if err != nil {
		t.Fatalf("could not unmarshal response: %v", err)
	}

	// Expected median time (200ms) from the sorted list [100ms, 200ms, 300ms]
	expectedConsensus := time.Date(2023, time.October, 27, 10, 0, 0, 200000000, time.UTC)
	if !response.ConsensusTime.Equal(expectedConsensus) {
		t.Errorf("consensus time mismatch: got %v want %v", response.ConsensusTime, expectedConsensus)
	}

	// Check source times
	if len(response.SourceTimes) != 3 {
		t.Errorf("expected 3 source times, got %d", len(response.SourceTimes))
	}

	expectedSourceTimes := []NTPResponse{
		{Server: "ntp1.example.com", Time: mockTimes["ntp1.example.com"], Error: ""},
		{Server: "ntp2.example.com", Time: mockTimes["ntp2.example.com"], Error: ""},
		{Server: "ntp3.example.com", Time: mockTimes["ntp3.example.com"], Error: ""},
	}

	// Sort both slices for comparison as order of goroutine completion is not guaranteed
	sort.Slice(response.SourceTimes, func(i, j int) bool {
		return response.SourceTimes[i].Server < response.SourceTimes[j].Server
	})
	sort.Slice(expectedSourceTimes, func(i, j int) bool {
		return expectedSourceTimes[i].Server < expectedSourceTimes[j].Server
	})

	if !reflect.DeepEqual(response.SourceTimes, expectedSourceTimes) {
		t.Errorf("source times mismatch: got %v want %v", response.SourceTimes, expectedSourceTimes)
	}
}

func TestSyncHandler_PartialFailure(t *testing.T) {
	originalNTPQueryFunc := ntpQueryFunc
	defer func() { ntpQueryFunc = originalNTPQueryFunc }()

	mockTimes := map[string]time.Time{
		"ntp1.example.com": time.Date(2023, time.October, 27, 10, 0, 0, 100000000, time.UTC),
		"ntp3.example.com": time.Date(2023, time.October, 27, 10, 0, 0, 300000000, time.UTC),
	}
	ntpQueryFunc = func(serverAddr string) (time.Time, error) {
		if tm, ok := mockTimes[serverAddr]; ok {
			return tm, nil
		}
		// Mock rationale: Simulate a network error for ntp2.example.com
		if serverAddr == "ntp2.example.com" {
			return time.Time{}, fmt.Errorf("connection refused")
		}
		return time.Time{}, fmt.Errorf("unknown mock server: %s", serverAddr)
	}

	os.Setenv("CHRONOSYNC_NTP_SERVERS", "ntp1.example.com,ntp2.example.com,ntp3.example.com")
	defer os.Unsetenv("CHRONOSYNC_NTP_SERVERS")

	req, err := http.NewRequest("GET", "/sync", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(syncHandler)

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	var response SyncResponse
	err = json.Unmarshal(rr.Body.Bytes(), &response)
	if err != nil {
		t.Fatalf("could not unmarshal response: %v", err)
	}

	// Expected median time (200ms) from valid times [100ms, 300ms] -> median is 100ms (first element if even count)
	// Go's median for even count takes the lower of the two middle elements.
	expectedConsensus := time.Date(2023, time.October, 27, 10, 0, 0, 100000000, time.UTC)
	if !response.ConsensusTime.Equal(expectedConsensus) {
		t.Errorf("consensus time mismatch: got %v want %v", response.ConsensusTime, expectedConsensus)
	}

	if len(response.SourceTimes) != 3 {
		t.Errorf("expected 3 source times, got %d", len(response.SourceTimes))
	}

	expectedSourceTimes := []NTPResponse{
		{Server: "ntp1.example.com", Time: mockTimes["ntp1.example.com"], Error: ""},
		{Server: "ntp2.example.com", Time: time.Time{}, Error: "connection refused"},
		{Server: "ntp3.example.com", Time: mockTimes["ntp3.example.com"], Error: ""},
	}

	sort.Slice(response.SourceTimes, func(i, j int) bool {
		return response.SourceTimes[i].Server < response.SourceTimes[j].Server
	})
	sort.Slice(expectedSourceTimes, func(i, j int) bool {
		return expectedSourceTimes[i].Server < expectedSourceTimes[j].Server
	})

	if !reflect.DeepEqual(response.SourceTimes, expectedSourceTimes) {
		t.Errorf("source times mismatch: got %v want %v", response.SourceTimes, expectedSourceTimes)
	}
}

func TestSyncHandler_AllFailure(t *testing.T) {
	originalNTPQueryFunc := ntpQueryFunc
	defer func() { ntpQueryFunc = originalNTPQueryFunc }()

	ntpQueryFunc = func(serverAddr string) (time.Time, error) {
		// Mock rationale: Simulate all NTP servers failing to respond.
		return time.Time{}, fmt.Errorf("timeout")
	}

	os.Setenv("CHRONOSYNC_NTP_SERVERS", "ntp1.example.com,ntp2.example.com")
	defer os.Unsetenv("CHRONOSYNC_NTP_SERVERS")

	req, err := http.NewRequest("GET", "/sync", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(syncHandler)

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	var response SyncResponse
	err = json.Unmarshal(rr.Body.Bytes(), &response)
	if err != nil {
		t.Fatalf("could not unmarshal response: %v", err)
	}

	// Expect zero time for consensus if all failed
	if !response.ConsensusTime.IsZero() {
		t.Errorf("expected zero consensus time, got %v", response.ConsensusTime)
	}

	if len(response.SourceTimes) != 2 {
		t.Errorf("expected 2 source times, got %d", len(response.SourceTimes))
	}

	for _, st := range response.SourceTimes {
		if st.Error == "" || !st.Time.IsZero() {
			t.Errorf("expected error and zero time for all sources, got %v", st)
		}
	}
}

func TestSyncHandler_NoServersConfigured(t *testing.T) {
	originalNTPQueryFunc := ntpQueryFunc
	defer func() { ntpQueryFunc = originalNTPQueryFunc }()

	// Mock rationale: Ensure no actual NTP queries are attempted if no servers are configured.
	ntpQueryFunc = func(serverAddr string) (time.Time, error) {
		t.Errorf("ntpQueryFunc should not be called if no servers are configured")
		return time.Time{}, nil
	}

	os.Setenv("CHRONOSYNC_NTP_SERVERS", "") // Explicitly set to empty
	defer os.Unsetenv("CHRONOSYNC_NTP_SERVERS")

	req, err := http.NewRequest("GET", "/sync", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(syncHandler)

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusInternalServerError {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusInternalServerError)
	}

	if !strings.Contains(rr.Body.String(), "No NTP servers configured") {
		t.Errorf("expected error message 'No NTP servers configured', got %s", rr.Body.String())
	}
}

func TestGetEnvOrDefault(t *testing.T) {
	// Test with environment variable set
	os.Setenv("TEST_VAR", "custom_value")
	val := getEnvOrDefault("TEST_VAR", "default_value")
	if val != "custom_value" {
		t.Errorf("Expected 'custom_value', got '%s'", val)
	}
	os.Unsetenv("TEST_VAR")

	// Test with environment variable not set
	val = getEnvOrDefault("NON_EXISTENT_VAR", "default_value")
	if val != "default_value" {
		t.Errorf("Expected 'default_value', got '%s'", val)
	}

	// Test with environment variable set to empty string
	os.Setenv("EMPTY_VAR", "")
	val = getEnvOrDefault("EMPTY_VAR", "default_value")
	if val != "default_value" {
		t.Errorf("Expected 'default_value' when env var is empty, got '%s'", val)
	}
	os.Unsetenv("EMPTY_VAR")
}
