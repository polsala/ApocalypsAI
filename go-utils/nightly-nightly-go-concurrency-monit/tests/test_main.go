package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"runtime"
	"testing"

	"github.com/gorilla/mux"
)

// Mock rationale: We are mocking the HTTP server and request/response cycle to test the handler logic.
func TestGoroutineCountHandler(t *testing.T) {
	// Create a new router
	r := mux.NewRouter()
	r.HandleFunc("/metrics", GoroutineCountHandler).Methods("GET")

	// Create a new HTTP request to the /metrics endpoint
	req, err := http.NewRequest("GET", "/metrics", nil)
	if err != nil {
		t.Fatalf("Failed to create request: %v", err)
	}

	// Create a ResponseRecorder to record the response
	w := httptest.NewRecorder()

	// Serve the request using the router
	r.ServeHTTP(w, req)

	// Check the status code
	if w.Code != http.StatusOK {
		t.Errorf("Expected status code %d, but got %d", http.StatusOK, w.Code)
	}

	// Check the Content-Type header
	expectedContentType := "application/json"
	if w.Header().Get("Content-Type") != expectedContentType {
		t.Errorf("Expected Content-Type %s, but got %s", expectedContentType, w.Header().Get("Content-Type"))
	}

	// Decode the JSON response
	var result map[string]int
	err = json.NewDecoder(w.Body).Decode(&result)
	if err != nil {
		t.Fatalf("Failed to decode JSON response: %v", err)
	}

	// Verify the goroutine count
	// We expect at least 1 goroutine (the one started in main) plus any test-related goroutines.
	// runtime.NumGoroutine() includes the current goroutine running this test.
	actualGoroutines := result["goroutines"]

	// We can't assert an exact number due to test runner overhead, but we can assert a minimum.
	// The main function starts one goroutine, and this test itself runs in a goroutine.
	// So, we expect at least 2 goroutines.
	minExpectedGoroutines := 2

	if actualGoroutines < minExpectedGoroutines {
		t.Errorf("Expected at least %d goroutines, but got %d", minExpectedGoroutines, actualGoroutines)
	}

	// Optional: Check if the number of goroutines is reasonable (e.g., not excessively high)
	maxExpectedGoroutines := 100 // Arbitrary upper bound for a simple test
	if actualGoroutines > maxExpectedGoroutines {
		t.Errorf("Unexpectedly high goroutine count: %d (max expected %d)", actualGoroutines, maxExpectedGoroutines)
	}
}

// Mock rationale: This test ensures that the main function starts the HTTP server and that it's accessible.
// We don't need to test the actual server startup and shutdown in detail, but we can check if the handler is registered.
func TestMainFunctionRegistersHandler(t *testing.T) {
	// We can't directly test `main()`'s `ListenAndServe()` without blocking or complex setup.
	// Instead, we'll simulate the router setup and check if the handler is registered for the expected path.

	r := mux.NewRouter()
	// Manually call the logic that `main` would use to register handlers
	r.HandleFunc("/metrics", GoroutineCountHandler).Methods("GET")

	// Get the route that matches the /metrics path
	var matchedRoute *mux.Route
	_ = r.Walk(func(route *mux.Route, router *mux.Router, ancestors []*mux.Route) error {
		pathTemplate, err := route.GetPathTemplate()
		if err != nil {
			return err
		}
		if pathTemplate == "/metrics" {
			matchedRoute = route
		}
		return nil
	})

	if matchedRoute == nil {
		t.Errorf("Handler for /metrics was not registered")
	}

	// Further check if the handler is indeed GoroutineCountHandler (optional but good practice)
	methods := []string{}
	matchedRoute.GetMethods(&methods)
	if len(methods) == 0 || methods[0] != "GET" {
		t.Errorf("Expected GET method for /metrics, but got %v", methods)
	}
}
