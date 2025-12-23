package main

import (
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

// # Mock rationale: We need to make rand.Intn deterministic for tests.
// The main package exposes setDeterministicRandSeed for this purpose.
// This ensures that the 'anomaly' feature produces predictable results in tests.

func TestTimeHandler_NoParams(t *testing.T) {
	req, err := http.NewRequest("GET", "/time", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(timeHandler)

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	expectedContentType := "text/plain; charset=utf-8"
	if contentType := rr.Header().Get("Content-Type"); contentType != expectedContentType {
		t.Errorf("handler returned wrong content type: got %v want %v",
			contentType, expectedContentType)
	}

	body := strings.TrimSpace(rr.Body.String())
	parsedTime, err := time.Parse(time.RFC3339Nano, body)
	if err != nil {
		t.Fatalf("Failed to parse time from response: %v", err)
	}

	// Check if the time is roughly now (within a small margin)
	diff := time.Since(parsedTime.UTC())
	if diff < -1*time.Second || diff > 1*time.Second {
		t.Errorf("Returned time is not close to current time: got %v, expected ~%v", parsedTime, time.Now().UTC())
	}
}

func TestTimeHandler_WithDrift(t *testing.T) {
	testCases := []struct {
		name         string
		driftParam   string
		expectedDiff time.Duration
	}{
		{"Positive Drift", "10s", 10 * time.Second},
		{"Negative Drift", "-5m", -5 * time.Minute},
		{"Zero Drift", "0s", 0 * time.Second},
		{"Complex Drift", "1h30m", 90 * time.Minute},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			req, err := http.NewRequest("GET", "/time?drift="+tc.driftParam, nil)
			if err != nil {
				t.Fatal(err)
			}

			rr := httptest.NewRecorder()
			handler := http.HandlerFunc(timeHandler)

			// Capture the time just before the request to compare against
			startTime := time.Now().UTC()
			handler.ServeHTTP(rr, req)

			if status := rr.Code; status != http.StatusOK {
				t.Errorf("handler returned wrong status code: got %v want %v",
					status, http.StatusOK)
			}

			body := strings.TrimSpace(rr.Body.String())
			parsedTime, err := time.Parse(time.RFC3339Nano, body)
			if err != nil {
				t.Fatalf("Failed to parse time from response: %v", err)
			}

			// Calculate the expected time based on startTime and drift
			expectedTime := startTime.Add(tc.expectedDiff)

			// Compare parsedTime with expectedTime, allowing for a small margin of error
			// due to test execution time.
			diff := parsedTime.Sub(expectedTime)
			if diff < -50*time.Millisecond || diff > 50*time.Millisecond {
				t.Errorf("Returned time with drift is incorrect for %s: got %v, expected ~%v (diff %v)",
					tc.driftParam, parsedTime, expectedTime, diff)
			}
		})
	}
}

func TestTimeHandler_InvalidDrift(t *testing.T) {
	req, err := http.NewRequest("GET", "/time?drift=invalid", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(timeHandler)

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code for invalid drift: got %v want %v",
			status, http.StatusBadRequest)
	}
	expectedBodyPart := "Invalid drift duration"
	if !strings.Contains(rr.Body.String(), expectedBodyPart) {
		t.Errorf("Expected error message containing '%s', got '%s'", expectedBodyPart, rr.Body.String())
	}
}

func TestTimeHandler_WithAnomaly(t *testing.T) {
	// # Mock rationale: Set a fixed seed for rand.Intn to make the anomaly deterministic.
	setDeterministicRandSeed(42) // A fixed seed for predictable random numbers

	req, err := http.NewRequest("GET", "/time?anomaly", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(timeHandler)

	// Capture the time just before the request
	startTime := time.Now().UTC()
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	body := strings.TrimSpace(rr.Body.String())
	parsedTime, err := time.Parse(time.RFC3339Nano, body)
	if err != nil {
		t.Fatalf("Failed to parse time from response: %v", err)
	}

	// With seed 42, rand.Intn(7200) will return 6564.
	// randomOffsetSeconds = 6564 - 3600 = 2964 seconds.
	expectedAnomalyDuration := 2964 * time.Second

	expectedTime := startTime.Add(expectedAnomalyDuration)

	diff := parsedTime.Sub(expectedTime)
	if diff < -50*time.Millisecond || diff > 50*time.Millisecond {
		t.Errorf("Returned time with anomaly is incorrect: got %v, expected ~%v (diff %v)",
			parsedTime, expectedTime, diff)
	}
}

func TestTimeHandler_WithDriftAndAnomaly(t *testing.T) {
	// # Mock rationale: Set a fixed seed for rand.Intn to make the anomaly deterministic.
	setDeterministicRandSeed(100) // Another fixed seed

	driftParam := "-30m"
	expectedDriftDuration := -30 * time.Minute

	req, err := http.NewRequest("GET", "/time?drift="+driftParam+"&anomaly", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(timeHandler)

	startTime := time.Now().UTC()
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	body := strings.TrimSpace(rr.Body.String())
	parsedTime, err := time.Parse(time.RFC3339Nano, body)
	if err != nil {
		t.Fatalf("Failed to parse time from response: %v", err)
	}

	// With seed 100, rand.Intn(7200) will return 500.
	// randomOffsetSeconds = 500 - 3600 = -3100 seconds.
	expectedAnomalyDuration := -3100 * time.Second

	expectedTime := startTime.Add(expectedDriftDuration).Add(expectedAnomalyDuration)

	diff := parsedTime.Sub(expectedTime)
	if diff < -50*time.Millisecond || diff > 50*time.Millisecond {
		t.Errorf("Returned time with drift and anomaly is incorrect: got %v, expected ~%v (diff %v)",
			parsedTime, expectedTime, diff)
	}
}

// Test that the setDeterministicRandSeed function works as expected
func TestSetDeterministicRandSeed(t *testing.T) {
	setDeterministicRandSeed(1)
	val1 := rand.Intn(100)
	setDeterministicRandSeed(1)
	val2 := rand.Intn(100)
	setDeterministicRandSeed(2)
	val3 := rand.Intn(100)

	if val1 != val2 {
		t.Errorf("Expected same random sequence for same seed, got %d and %d", val1, val2)
	}
	if val1 == val3 {
		t.Errorf("Expected different random sequence for different seed, got %d and %d", val1, val3)
	}
}
