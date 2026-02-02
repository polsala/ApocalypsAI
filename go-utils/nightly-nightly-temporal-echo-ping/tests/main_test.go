package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock rationale: We need to simulate network responses and latencies without actual network calls
// to ensure deterministic and fast test execution. httptest.Server allows us to control the server's
// behavior and response times.

func TestPingTarget_Success(t *testing.T) {
	// Mock rationale: Create a local HTTP server to simulate a successful endpoint.
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(50 * time.Millisecond) // Simulate some latency
		fmt.Fprintln(w, "Temporal anomaly detected!")
	}))
	defer ts.Close()

	target := Target{Name: "Test Anchor", URL: ts.URL}
	timeout := 1 * time.Second
	result := pingTarget(target, timeout)

	if result.Error != nil {
		t.Errorf("Expected no error, got %v", result.Error)
	}
	if result.TargetName != "Test Anchor" {
		t.Errorf("Expected target name 'Test Anchor', got '%s'", result.TargetName)
	}
	if result.Latency < 50*time.Millisecond {
		t.Errorf("Expected latency around 50ms, got %s", result.Latency)
	}
	if result.IsEcho {
		t.Errorf("Expected IsEcho to be false for normal latency")
	}
}

func TestPingTarget_Timeout(t *testing.T) {
	// Mock rationale: Create a local HTTP server that delays longer than the client's timeout.
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(200 * time.Millisecond) // Longer than client timeout
		fmt.Fprintln(w, "Too slow!")
	}))
	defer ts.Close()

	target := Target{Name: "Slow Anchor", URL: ts.URL}
	timeout := 50 * time.Millisecond // Short timeout
	result := pingTarget(target, timeout)

	if result.Error == nil {
		t.Errorf("Expected a timeout error, got nil")
	}
	if !strings.Contains(result.Error.Error(), "context deadline exceeded") && !strings.Contains(result.Error.Error(), "Client.Timeout exceeded") {
		t.Errorf("Expected timeout error, got: %v", result.Error)
	}
}

func TestPingTarget_Non2xxStatus(t *testing.T) {
	// Mock rationale: Simulate a server returning an error status code.
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		fmt.Fprintln(w, "Temporal anchor not found!")
	}))
	defer ts.Close()

	target := Target{Name: "Missing Anchor", URL: ts.URL}
	timeout := 1 * time.Second
	result := pingTarget(target, timeout)

	if result.Error == nil {
		t.Errorf("Expected an error for non-2xx status, got nil")
	}
	if !strings.Contains(result.Error.Error(), "non-2xx status code: 404") {
		t.Errorf("Expected 404 status error, got: %v", result.Error)
	}
}

func TestMonitorTargets_Concurrent(t *testing.T) {
	var mu sync.Mutex
	hitCounts := make(map[string]int)

	// Mock rationale: Create multiple test servers to simulate different endpoints
	// and verify concurrent access.
	ts1 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		mu.Lock()
		hitCounts["ts1"]++
		mu.Unlock()
		time.Sleep(10 * time.Millisecond)
		fmt.Fprintln(w, "OK1")
	}))
	defer ts1.Close()

	ts2 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		mu.Lock()
		hitCounts["ts2"]++
		mu.Unlock()
		time.Sleep(50 * time.Millisecond) // Simulate higher latency
		fmt.Fprintln(w, "OK2")
	}))
	defer ts2.Close()

	ts3 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		mu.Lock()
		hitCounts["ts3"]++
		mu.Unlock()
		time.Sleep(150 * time.Millisecond) // Simulate echo latency
		fmt.Fprintln(w, "OK3")
	}))
	defer ts3.Close()

	targets := []Target{
		{Name: "Anchor A", URL: ts1.URL},
		{Name: "Anchor B", URL: ts2.URL},
		{Name: "Anchor C", URL: ts3.URL},
	}
	timeout := 1 * time.Second
	echoThresholdMs := 100 // Anchor C should trigger an echo

	results := monitorTargets(targets, timeout, echoThresholdMs)

	if len(results) != 3 {
		t.Fatalf("Expected 3 results, got %d", len(results))
	}

	// Verify all targets were hit
	mu.Lock()
	if hitCounts["ts1"] != 1 || hitCounts["ts2"] != 1 || hitCounts["ts3"] != 1 {
		t.Errorf("Expected all servers to be hit once, got: %v", hitCounts)
	}
	mu.Unlock()

	// Verify results
	foundA, foundB, foundC := false, false, false
	for _, res := range results {
		switch res.TargetName {
		case "Anchor A":
			foundA = true
			if res.Error != nil {
				t.Errorf("Anchor A: Expected no error, got %v", res.Error)
			}
			if res.IsEcho {
				t.Errorf("Anchor A: Expected no echo")
			}
		case "Anchor B":
			foundB = true
			if res.Error != nil {
				t.Errorf("Anchor B: Expected no error, got %v", res.Error)
			}
			if res.IsEcho {
				t.Errorf("Anchor B: Expected no echo")
			}
		case "Anchor C":
			foundC = true
			if res.Error != nil {
				t.Errorf("Anchor C: Expected no error, got %v", res.Error)
			}
			if !res.IsEcho {
				t.Errorf("Anchor C: Expected an echo due to high latency")
			}
		}
	}
	if !foundA || !foundB || !foundC {
		t.Errorf("Not all anchors were found in results: A=%t, B=%t, C=%t", foundA, foundB, foundC)
	}
}

func TestMainFunction_NoTargets(t *testing.T) {
	// Mock rationale: Temporarily redirect os.Stderr to capture output and
	// simulate no targets being configured.
	oldStderr := os.Stderr
	r, w, _ := os.Pipe()
	os.Stderr = w

	// Clear environment variables that might set targets
	os.Unsetenv("TEMPORAL_ANCHORS")

	// Use a goroutine to run main and capture its exit code
	exitCode := 0
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		defer func() {
			if r := recover(); r != nil {
				// main calls os.Exit, which causes a panic in tests.
				// We capture the exit code here.
				if e, ok := r.(int); ok {
					exitCode = e
				} else {
					panic(r) // Re-panic if it's not an int exit code
				}
			}
		}()
		main()
	}()

	wg.Wait() // Wait for main to finish (and potentially panic/exit)

	w.Close()
	os.Stderr = oldStderr // Restore stderr

	var buf strings.Builder
	_, _ = fmt.Fprintln(&buf, r) // Read from the pipe (this is not ideal, better to read all)
	// For simplicity, just check the exit code. A real test would read the full output.

	if exitCode != 1 {
		t.Errorf("Expected main to exit with code 1 (no targets), got %d", exitCode)
	}
}

func TestMainFunction_WithTargetsAndEcho(t *testing.T) {
	// Mock rationale: Create a test server that will cause an "echo" (high latency)
	// and another that is stable.
	tsEcho := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(300 * time.Millisecond) // High latency
		fmt.Fprintln(w, "Echoing!")
	}))
	defer tsEcho.Close()

	tsStable := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(50 * time.Millisecond) // Low latency
		fmt.Fprintln(w, "Stable!")
	}))
	defer tsStable.Close()

	// Mock rationale: Set environment variables to configure the main function.
	os.Setenv("TEMPORAL_ANCHORS", fmt.Sprintf("EchoAnchor=%s,StableAnchor=%s", tsEcho.URL, tsStable.URL))
	os.Setenv("PING_TIMEOUT_MS", "1000")
	os.Setenv("ECHO_THRESHOLD_MS", "150") // EchoAnchor should exceed this

	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	exitCode := 0
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		defer func() {
			if r := recover(); r != nil {
				if e, ok := r.(int); ok {
					exitCode = e
				} else {
					panic(r)
				}
			}
		}()
		main()
	}()
	wg.Wait()

	w.Close()
	os.Stdout = oldStdout

	outputBytes, _ := os.ReadFile(r.Name()) // Read from the pipe file
	output := string(outputBytes)

	if exitCode != 1 {
		t.Errorf("Expected main to exit with code 1 (echoes detected), got %d", exitCode)
	}
	if !strings.Contains(output, "EchoAnchor: Experiencing temporal flux!") {
		t.Errorf("Expected output to contain echo warning for EchoAnchor, got:\n%s", output)
	}
	if !strings.Contains(output, "StableAnchor: Temporal stability maintained.") {
		t.Errorf("Expected output to contain stable message for StableAnchor, got:\n%s", output)
	}
	if !strings.Contains(output, "Warning: Some temporal anchors are experiencing echoes.") {
		t.Errorf("Expected final warning about echoes, got:\n%s", output)
	}

	// Clean up env vars
	os.Unsetenv("TEMPORAL_ANCHORS")
	os.Unsetenv("PING_TIMEOUT_MS")
	os.Unsetenv("ECHO_THRESHOLD_MS")
}

func TestMainFunction_AllStable(t *testing.T) {
	// Mock rationale: Create test servers that are all stable (low latency).
	tsStable1 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(20 * time.Millisecond)
		fmt.Fprintln(w, "Stable 1!")
	}))
	defer tsStable1.Close()

	tsStable2 := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(30 * time.Millisecond)
		fmt.Fprintln(w, "Stable 2!")
	}))
	defer tsStable2.Close()

	// Mock rationale: Set environment variables to configure the main function.
	os.Setenv("TEMPORAL_ANCHORS", fmt.Sprintf("StableAnchor1=%s,StableAnchor2=%s", tsStable1.URL, tsStable2.URL))
	os.Setenv("PING_TIMEOUT_MS", "1000")
	os.Setenv("ECHO_THRESHOLD_MS", "150") // Both should be below this

	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	exitCode := 0
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer wg.Done()
		defer func() {
			if r := recover(); r != nil {
				if e, ok := r.(int); ok {
					exitCode = e
				} else {
					panic(r)
				}
			}
		}()
		main()
	}()
	wg.Wait()

	w.Close()
	os.Stdout = oldStdout

	outputBytes, _ := os.ReadFile(r.Name())
	output := string(outputBytes)

	if exitCode != 0 {
		t.Errorf("Expected main to exit with code 0 (all stable), got %d", exitCode)
	}
	if !strings.Contains(output, "StableAnchor1: Temporal stability maintained.") {
		t.Errorf("Expected output to contain stable message for StableAnchor1, got:\n%s", output)
	}
	if !strings.Contains(output, "StableAnchor2: Temporal stability maintained.") {
		t.Errorf("Expected output to contain stable message for StableAnchor2, got:\n%s", output)
	}
	if !strings.Contains(output, "All temporal anchors are stable. The timeline holds... for now.") {
		t.Errorf("Expected final stable message, got:\n%s", output)
	}

	// Clean up env vars
	os.Unsetenv("TEMPORAL_ANCHORS")
	os.Unsetenv("PING_TIMEOUT_MS")
	os.Unsetenv("ECHO_THRESHOLD_MS")
}
