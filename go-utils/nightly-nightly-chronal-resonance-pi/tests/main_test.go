package main

import (
	"bytes"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
	"time"
)

// Mock rationale: We use httptest.NewServer to create a local, in-memory HTTP server
// that can simulate various network conditions (fast response, slow response, errors)
// without making actual external network calls. This ensures tests are deterministic
// and run offline.

func TestPingTarget_Success(t *testing.T) {
	// Mock rationale: Simulating a successful, fast HTTP response.
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "OK")
	}))
	defer server.Close()

	client := &http.Client{Timeout: 1 * time.Second}
	result := pingTarget(server.URL, client)

	if result.Error != nil {
		t.Errorf("Expected no error, got %v", result.Error)
	}
	// Duration should be non-zero but small
	if result.Duration == 0 || result.Duration > 100*time.Millisecond {
		t.Errorf("Expected a reasonable non-zero duration, got %v", result.Duration)
	}
	if result.Target != server.URL {
		t.Errorf("Expected target %s, got %s", server.URL, result.Target)
	}
}

func TestPingTarget_Timeout(t *testing.T) {
	// Mock rationale: Simulating a server that takes longer to respond than the client's timeout.
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(200 * time.Millisecond) // Longer than client timeout
		fmt.Fprintln(w, "Too slow!")
	}))
	defer server.Close()

	client := &http.Client{Timeout: 50 * time.Millisecond} // Short timeout
	result := pingTarget(server.URL, client)

	if result.Error == nil {
		t.Errorf("Expected a timeout error, got nil")
	}
	// Check for common timeout error messages
	if !strings.Contains(result.Error.Error(), "timeout") && !strings.Contains(result.Error.Error(), "context deadline exceeded") {
		t.Errorf("Expected timeout error, got: %v", result.Error)
	}
	// Duration should be close to the timeout value
	if result.Duration < 40*time.Millisecond || result.Duration > 100*time.Millisecond {
		t.Errorf("Expected duration around timeout (%v), got %v", client.Timeout, result.Duration)
	}
	if result.Target != server.URL {
		t.Errorf("Expected target %s, got %s", server.URL, result.Target)
	}
}

func TestPingTarget_HTTPError(t *testing.T) {
	// Mock rationale: Simulating a server that returns an HTTP error (e.g., 500 Internal Server Error).
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
	}))
	defer server.Close()

	client := &http.Client{Timeout: 1 * time.Second}
	result := pingTarget(server.URL, client)

	if result.Error == nil {
		t.Errorf("Expected an HTTP error, got nil")
	}
	if !strings.Contains(result.Error.Error(), "HTTP status 500") {
		t.Errorf("Expected HTTP status 500 error, got: %v", result.Error)
	}
	if result.Target != server.URL {
		t.Errorf("Expected target %s, got %s", server.URL, result.Target)
	}
}

func TestMainLogic_SuccessAndFailure(t *testing.T) {
	// Mock rationale: Simulating multiple servers with different behaviors to test the main aggregation logic.
	// Server 1: Fast success
	server1 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(10 * time.Millisecond)
		fmt.Fprintln(w, "OK")
	}))
	defer server1.Close()

	// Server 2: Slow success
	server2 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(100 * time.Millisecond)
		fmt.Fprintln(w, "OK")
	}))
	defer server2.Close()

	// Server 3: HTTP 500 error
	server3 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
	}))
	defer server3.Close()

	// Capture stdout
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Temporarily set os.Args for the test
	originalArgs := os.Args
	os.Args = []string{"nightly-chronal-resonance-pinger", server1.URL, server2.URL, server3.URL}

	// Use a defer to restore os.Stdout and os.Args
	defer func() {
		w.Close()
		os.Stdout = oldStdout
		os.Args = originalArgs
	}()

	main()

	out, _ := io.ReadAll(r)
	output := string(out)

	if !strings.Contains(output, "Successful Resonances:") {
		t.Errorf("Output missing 'Successful Resonances:'\n%s", output)
	}
	if !strings.Contains(output, fmt.Sprintf("[OK] %-30s:", server1.URL)) {
		t.Errorf("Output missing successful ping for server1\n%s", output)
	}
	if !strings.Contains(output, fmt.Sprintf("[OK] %-30s:", server2.URL)) {
		t.Errorf("Output missing successful ping for server2\n%s", output)
	}
	if !strings.Contains(output, "Temporal Anomalies (Failed Resonances):") {
		t.Errorf("Output missing 'Temporal Anomalies (Failed Resonances):'\n%s", output)
	}
	if !strings.Contains(output, fmt.Sprintf("[FAIL] %-30s: HTTP status 500", server3.URL)) {
		t.Errorf("Output missing failed ping for server3\n%s", output)
	}
	if !strings.Contains(output, "Average Resonance Time:") {
		t.Errorf("Output missing 'Average Resonance Time:'\n%s", output)
	}
}

func TestMainLogic_NoArgs(t *testing.T) {
	// Mock rationale: Testing the usage message when no arguments are provided.
	oldStdout := os.Stdout
	oldStderr := os.Stderr
	rOut, wOut, _ := os.Pipe()
	rErr, wErr, _ := os.Pipe()
	os.Stdout = wOut
	os.Stderr = wErr

	originalArgs := os.Args
	os.Args = []string{"nightly-chronal-resonance-pinger"}

	// Use a defer to restore os.Stdout/Stderr and os.Args
	defer func() {
		wOut.Close()
		wErr.Close()
		os.Stdout = oldStdout
		os.Stderr = oldStderr
		os.Args = originalArgs
	}()

	// Capture os.Exit calls
	exitCalled := false
	oldOsExit := osExit
	osExit = func(code int) {
		exitCalled = true
		if code != 1 {
			t.Errorf("Expected exit code 1, got %d", code)
		}
		panic("os.Exit was called") // Panic to stop execution, caught by recover
	}
	defer func() { osExit = oldOsExit }() // Restore original osExit

	// Call main in a goroutine and recover from the panic
	func() {
		defer func() {
			if r := recover(); r == nil {
				t.Errorf("Expected main() to panic due to os.Exit, but it did not")
			}
		}()
		main()
	}()

	if !exitCalled {
		t.Errorf("Expected os.Exit(1) to be called, but it wasn't")
	}

	outBytes, _ := io.ReadAll(rOut)
	errBytes, _ := io.ReadAll(rErr)
	output := string(outBytes) + string(errBytes)

	expectedUsage := "Usage: nightly-chronal-resonance-pinger <target_url_1> [target_url_2 ...]"
	if !strings.Contains(output, expectedUsage) {
		t.Errorf("Expected output to contain '%s', got:\n%s", expectedUsage, output)
	}
}

func TestCalculateAverageDuration(t *testing.T) {
	tests := []struct {
		name    string
		results []ResonanceResult
		want    time.Duration
	}{
		{
			name:    "empty slice",
			results: []ResonanceResult{},
			want:    0,
		},
		{
			name: "single result",
			results: []ResonanceResult{
				{Duration: 10 * time.Millisecond},
			},
			want: 10 * time.Millisecond,
		},
		{
			name: "multiple results",
			results: []ResonanceResult{
				{Duration: 10 * time.Millisecond},
				{Duration: 20 * time.Millisecond},
				{Duration: 30 * time.Millisecond},
			},
			want: 20 * time.Millisecond, // (10+20+30)/3 = 20
		},
		{
			name: "results with remainder",
			results: []ResonanceResult{
				{Duration: 10 * time.Millisecond},
				{Duration: 10 * time.Millisecond},
				{Duration: 10 * time.Millisecond},
				{Duration: 10 * time.Millisecond},
				{Duration: 10 * time.Millisecond},
				{Duration: 1 * time.Millisecond}, // 51 / 6 = 8.5, Go truncates
			},
			want: 8 * time.Millisecond,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := calculateAverageDuration(tt.results)
			// For exact comparison, convert to int60 nanoseconds
			if got.Nanoseconds() != tt.want.Nanoseconds() {
				t.Errorf("calculateAverageDuration() got = %v, want %v", got, tt.want)
			}
		})
	}
}
