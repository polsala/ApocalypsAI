package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock rationale: httptest.NewServer creates a local HTTP server that can be controlled
// to return specific status codes, delays, or errors. This allows simulating network conditions
// (success, failure, timeout) deterministically and without actual external network calls.

func TestCheckBeacon_Success(t *testing.T) {
	// Mock a successful HTTP server
	successServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "OK")
	}))
	defer successServer.Close()

	results := make(chan BeaconResult, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	go checkBeacon(successServer.URL, 1*time.Second, results, &wg)

	wg.Wait()
	close(results)

	res := <-results

	if res.URL != successServer.URL {
		t.Errorf("Expected URL %s, got %s", successServer.URL, res.URL)
	}
	if res.Status != "pulsing strongly" {
		t.Errorf("Expected status 'pulsing strongly', got '%s'", res.Status)
	}
	if res.StatusCode != http.StatusOK {
		t.Errorf("Expected status code %d, got %d", http.StatusOK, res.StatusCode)
	}
	if res.Error != nil {
		t.Errorf("Expected no error, got %v", res.Error)
	}
	if res.Latency == 0 {
		t.Errorf("Expected non-zero latency")
	}
}

func TestCheckBeacon_ClientError(t *testing.T) {
	// Mock a server returning a 404 Not Found
	clientErrorServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
		fmt.Fprint(w, "Not Found")
	}))
	defer clientErrorServer.Close()

	results := make(chan BeaconResult, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	go checkBeacon(clientErrorServer.URL, 1*time.Second, results, &wg)

	wg.Wait()
	close(results)

	res := <-results

	if res.URL != clientErrorServer.URL {
		t.Errorf("Expected URL %s, got %s", clientErrorServer.URL, res.URL)
	}
	if res.Status != "emitting strange echoes" {
		t.Errorf("Expected status 'emitting strange echoes', got '%s'", res.Status)
	}
	if res.StatusCode != http.StatusNotFound {
		t.Errorf("Expected status code %d, got %d", http.StatusNotFound, res.StatusCode)
	}
	if res.Error != nil {
		t.Errorf("Expected no error, got %v", res.Error)
	}
}

func TestCheckBeacon_ServerError(t *testing.T) {
	// Mock a server returning a 500 Internal Server Error
	serverErrorServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprint(w, "Internal Server Error")
	}))
	defer serverErrorServer.Close()

	results := make(chan BeaconResult, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	go checkBeacon(serverErrorServer.URL, 1*time.Second, results, &wg)

	wg.Wait()
	close(results)

	res := <-results

	if res.URL != serverErrorServer.URL {
		t.Errorf("Expected URL %s, got %s", serverErrorServer.URL, res.URL)
	}
	if res.Status != "experiencing temporal distortions" {
		t.Errorf("Expected status 'experiencing temporal distortions', got '%s'", res.Status)
	}
	if res.StatusCode != http.StatusInternalServerError {
		t.Errorf("Expected status code %d, got %d", http.StatusInternalServerError, res.StatusCode)
	}
	if res.Error != nil {
		t.Errorf("Expected no error, got %v", res.Error)
	}
}

func TestCheckBeacon_Timeout(t *testing.T) {
	// Mock a server that delays its response beyond the timeout
	timeoutServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(200 * time.Millisecond) // Longer than the 100ms timeout below
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "Too Slow")
	}))
	defer timeoutServer.Close()

	results := make(chan BeaconResult, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	go checkBeacon(timeoutServer.URL, 100*time.Millisecond, results, &wg)

	wg.Wait()
	close(results)

	res := <-results

	if res.URL != timeoutServer.URL {
		t.Errorf("Expected URL %s, got %s", timeoutServer.URL, res.URL)
	}
	if res.Status != "lost its signal" {
		t.Errorf("Expected status 'lost its signal', got '%s'", res.Status)
	}
	if res.Error == nil || (!strings.Contains(res.Error.Error(), "timeout") && !strings.Contains(res.Error.Error(), "context deadline exceeded")) {
		t.Errorf("Expected a timeout error, got %v", res.Error)
	}
}

func TestCheckBeacon_ConnectionRefused(t *testing.T) {
	// To simulate connection refused, we use a URL that will definitely not connect.
	// This is tricky with httptest, so we'll use a non-existent local address.
	// Mock rationale: Directly testing a connection refused error requires attempting to connect
	// to a port that is known to be closed or an invalid address. Using a non-routable IP
	// and a high port is a reliable way to simulate this offline.
	badURL := "http://127.0.0.1:65535" // A port that is highly unlikely to be in use

	results := make(chan BeaconResult, 1)
	var wg sync.WaitGroup
	wg.Add(1)

	go checkBeacon(badURL, 100*time.Millisecond, results, &wg)

	wg.Wait()
	close(results)

	res := <-results

	if res.URL != badURL {
		t.Errorf("Expected URL %s, got %s", badURL, res.URL)
	}
	if res.Status != "faint and unreachable" {
		t.Errorf("Expected status 'faint and unreachable', got '%s'", res.Status)
	}
	if res.Error == nil || (!strings.Contains(res.Error.Error(), "connection refused") && !strings.Contains(res.Error.Error(), "no such host") && !strings.Contains(res.Error.Error(), "dial tcp")) {
		t.Errorf("Expected connection refused/no such host error, got %v", res.Error)
	}
}

func TestMainFunction(t *testing.T) {
	// Mock rationale: To test the main function's output, we redirect os.Stdout
	// and provide mock URLs from httptest.NewServer. This allows capturing the console output
	// and verifying it against expected strings, making the test deterministic and offline.

	// Setup mock servers
	successServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "OK")
	}))
	defer successServer.Close()

	timeoutServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		time.Sleep(200 * time.Millisecond)
		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "Too Slow")
	}))
	defer timeoutServer.Close()

	// Simulate connection refused by using a non-existent address
	badURL := "http://127.0.0.1:65534" // Another highly unlikely port

	// Capture stdout
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Set command-line arguments
	oldArgs := os.Args
	os.Args = []string{"main", successServer.URL, timeoutServer.URL, badURL}

	main()

	// Restore stdout and args
	w.Close()
	os.Stdout = oldStdout
	os.Args = oldArgs

	out, _ := ioutil.ReadAll(r)
	output := string(out)

	// Verify output contains expected messages
	if !strings.Contains(output, "Initiating Beacon Pulse Scan...") {
		t.Errorf("Expected 'Initiating Beacon Pulse Scan...' in output, got:\n%s", output)
	}
	if !strings.Contains(output, fmt.Sprintf("Beacon %s pulsing strongly (Status: 200", successServer.URL)) {
		t.Errorf("Expected success message for %s, got:\n%s", successServer.URL, output)
	}
	// The exact error message for timeout can vary slightly by Go version/OS
	if !strings.Contains(output, fmt.Sprintf("Beacon %s lost its signal (Error: ", timeoutServer.URL)) ||
	   (!strings.Contains(output, "timeout") && !strings.Contains(output, "context deadline exceeded")) {
		t.Errorf("Expected timeout message for %s, got:\n%s", timeoutServer.URL, output)
	}
	// The exact error message for connection refused can vary slightly by OS/Go version
	if !strings.Contains(output, fmt.Sprintf("Beacon %s faint and unreachable (Error: ", badURL)) ||
	   (!strings.Contains(output, "connection refused") && !strings.Contains(output, "no such host") && !strings.Contains(output, "dial tcp")) {
		t.Errorf("Expected connection refused/no such host message for %s, got:\n%s", badURL, output)
	}
	if !strings.Contains(output, "Beacon Pulse Scan Complete.") {
		t.Errorf("Expected 'Beacon Pulse Scan Complete.' in output, got:\n%s", output)
	}
}

func TestMainFunction_NoArgs(t *testing.T) {
	// Mock rationale: To test the main function's error handling for no arguments,
	// we redirect os.Stdout and capture the call to os.Exit. This allows verifying
	// the usage message and the program's exit behavior deterministically and offline.

	// Capture stdout
	oldStdout := os.Stdout
	rOut, wOut, _ := os.Pipe()
	os.Stdout = wOut

	// Set command-line arguments to only the program name
	oldArgs := os.Args
	os.Args = []string{"main"}

	// Use a defer to restore os.Exit and capture its call
	exitCalled := false
	oldExit := exit
	exit = func(code int) {
		exitCalled = true
		if code != 1 {
			t.Errorf("Expected exit code 1, got %d", code)
		}
		panic("os.Exit called") // Panic to stop execution without actually exiting the test runner
	}
	defer func() {
		recover() // Recover from the panic
		exit = oldExit // Restore original exit function
	}()

	main()

	// Restore stdout and args
	wOut.Close()
	os.Stdout = oldStdout
	os.Args = oldArgs

	out, _ := ioutil.ReadAll(rOut)
	output := string(out)

	if !strings.Contains(output, "Usage: go run src/main.go <url1> <url2> ...") {
		t.Errorf("Expected usage message in output, got:\n%s", output)
	}
	if !exitCalled {
		t.Errorf("Expected os.Exit(1) to be called, but it wasn't.")
	}
}
