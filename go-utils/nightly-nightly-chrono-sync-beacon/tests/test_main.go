package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
	"flag" // Import flag to set test flags
)

// Mock rationale: httptest.NewRecorder and httptest.NewRequest allow us to simulate
// HTTP requests and responses without starting a real network server. This makes
// tests deterministic, fast, and independent of network conditions or available ports.

func TestTimeHandler(t *testing.T) {
	// Set up mock flag values for testing
	// # Mock rationale: Directly setting flag variables for testing purposes.
	// This allows tests to control the configuration of the handler without
	// relying on actual command-line arguments or global state that might
	// interfere with other tests.
	originalPort := *port
	originalOffsetSeconds := *offsetSeconds
	originalBeaconID := *beaconID
	defer func() { // Restore original flag values after test
		*port = originalPort
		*offsetSeconds = originalOffsetSeconds
		*beaconID = originalBeaconID
	}()

	tests := []struct {
		name          string
		method        string
		expectedStatus int
		expectedOffset int
		expectedID     string
		expectError    bool
	}{
		{
			name:          "GET request with default offset",
			method:        http.MethodGet,
			expectedStatus: http.StatusOK,
			expectedOffset: 0,
			expectedID:     "TEST-BEACON-001",
			expectError:    false,
		},
		{
			name:          "GET request with positive offset",
			method:        http.MethodGet,
			expectedStatus: http.StatusOK,
			expectedOffset: 3600, // +1 hour
			expectedID:     "TEST-BEACON-002",
			expectError:    false,
		},
		{
			name:          "GET request with negative offset",
			method:        http.MethodGet,
			expectedStatus: http.StatusOK,
			expectedOffset: -1800, // -30 minutes
			expectedID:     "TEST-BEACON-003",
			expectError:    false,
		},
		{
			name:          "POST request (method not allowed)",
			method:        http.MethodPost,
			expectedStatus: http.StatusMethodNotAllowed,
			expectedOffset: 0, // Not relevant for this test
			expectedID:     "TEST-BEACON-004",
			expectError:    true, // Expect an error response, not a valid time
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Set test-specific flag values
			*offsetSeconds = tt.expectedOffset
			*beaconID = tt.expectedID

			req, err := http.NewRequest(tt.method, "/time", nil)
			if err != nil {
				t.Fatalf("Could not create request: %v", err)
			}

			rr := httptest.NewRecorder()
			handler := http.HandlerFunc(timeHandler)
			handler.ServeHTTP(rr, req)

			if status := rr.Code; status != tt.expectedStatus {
				t.Errorf("handler returned wrong status code: got %v want %v",
					status, tt.expectedStatus)
			}

			if tt.expectError {
				// For error cases, we don't expect a JSON body, just check status.
				return
			}

			var response BeaconResponse
			err = json.Unmarshal(rr.Body.Bytes(), &response)
			if err != nil {
				t.Fatalf("Could not unmarshal response: %v", err)
			}

			if response.BeaconID != tt.expectedID {
				t.Errorf("handler returned wrong BeaconID: got %v want %v",
					response.BeaconID, tt.expectedID)
			}

			if response.TemporalOffsetSeconds != tt.expectedOffset {
				t.Errorf("handler returned wrong TemporalOffsetSeconds: got %v want %v",
					response.TemporalOffsetSeconds, tt.expectedOffset)
			}

			// Verify the adjusted time is approximately correct.
			// We can't check for exact time.Now() due to test execution time,
			// so we check if it's within a small window around the expected time.
			expectedAdjustedTime := time.Now().UTC().Add(time.Duration(tt.expectedOffset) * time.Second)
			// Allow a small delta for test execution time
			if response.CurrentTimeUTC.Before(expectedAdjustedTime.Add(-5*time.Second)) ||
				response.CurrentTimeUTC.After(expectedAdjustedTime.Add(5*time.Second)) {
				t.Errorf("handler returned time %v which is not close to expected adjusted time %v (offset %d)",
					response.CurrentTimeUTC, expectedAdjustedTime, tt.expectedOffset)
			}
		})
	}
}
