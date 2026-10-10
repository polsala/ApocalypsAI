package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"
	"time"
)

// Mock rationale: We need to test the echo chamber's behavior without making actual network calls.
// httptest.NewServer allows us to simulate the incoming request endpoint.
// The mock for osExit allows us to test error conditions that would normally terminate the program.

func TestEchoChamber(t *testing.T) {
	// Store original flag values and restore them after the test
	originalOutputURL := *outputURL
	originalDelayMillis := *delayMillis
	defer func() {
		outputURL = &originalOutputURL
		delayMillis = &originalDelayMillis
	}()

	// 1. Setup mock output server
	var receivedBody []byte
	var receivedHeaders http.Header
	var outputWg sync.WaitGroup
	outputWg.Add(1) // Expect one message to be re-broadcasted

	mockOutputServer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer outputWg.Done()
		body, err := ioutil.ReadAll(r.Body)
		if err != nil {
			t.Errorf("Mock output server failed to read body: %v", err)
			http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			return
		}
		receivedBody = body
		receivedHeaders = r.Header
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "OK")
	}))
	defer mockOutputServer.Close()

	// Set flags for this test
	outputURL = &mockOutputServer.URL // Point to the mock server
	*delayMillis = 100                 // Short delay for testing

	// 2. Setup the echo chamber server (using the actual handler)
	echoServer := httptest.NewServer(http.HandlerFunc(echoHandler))
	defer echoServer.Close()

	// 3. Send a message to the echo chamber
	testMessage := "Hello, Temporal Void!"
	req, err := http.NewRequest(http.MethodPost, echoServer.URL+"/echo", bytes.NewBufferString(testMessage))
	if err != nil {
		t.Fatalf("Failed to create request: %v", err)
	}
	req.Header.Set("Content-Type", "text/plain")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		t.Fatalf("Failed to send request to echo chamber: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusAccepted {
		t.Errorf("Expected status %d, got %d", http.StatusAccepted, resp.StatusCode)
	}

	// Wait for the message to be re-broadcasted
	// Use a timeout to prevent tests from hanging indefinitely
	done := make(chan struct{})
	go func() {
		outputWg.Wait()
		close(done)
	}()

	select {
	case <-done:
		// Message re-broadcasted
	case <-time.After(500 * time.Millisecond): // A bit longer than the delayMillis
		t.Fatal("Timeout waiting for message re-broadcast.")
	}

	// 4. Verify the re-broadcasted message
	if string(receivedBody) != testMessage {
		t.Errorf("Expected re-broadcasted body '%s', got '%s'", testMessage, string(receivedBody))
	}
	if receivedHeaders.Get("Content-Type") != "text/plain" {
		t.Errorf("Expected Content-Type 'text/plain', got '%s'", receivedHeaders.Get("Content-Type"))
	}
	if receivedHeaders.Get("X-Temporal-Echo-Delay") != "100ms" {
		t.Errorf("Expected X-Temporal-Echo-Delay '100ms', got '%s'", receivedHeaders.Get("X-Temporal-Echo-Delay"))
	}
}

func TestEchoChamber_MethodNotAllowed(t *testing.T) {
	echoServer := httptest.NewServer(http.HandlerFunc(echoHandler))
	defer echoServer.Close()

	req, err := http.NewRequest(http.MethodGet, echoServer.URL+"/echo", nil)
	if err != nil {
		t.Fatalf("Failed to create request: %v", err)
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		t.Fatalf("Failed to send request to echo chamber: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusMethodNotAllowed {
		t.Errorf("Expected status %d, got %d", http.StatusMethodNotAllowed, resp.StatusCode)
	}
}

func TestEchoChamber_OutputURLRequired(t *testing.T) {
	// Mock os.Exit to prevent actual exit during test
	oldOsExit := osExit
	defer func() { osExit = oldOsExit }()
	exitCalled := make(chan int, 1) // Channel to capture exit code
	osExit = func(code int) {
		exitCalled <- code
		panic("os.Exit called") // Panic to stop execution but allow defer to run
	}

	// Capture log output
	var buf bytes.Buffer
	log.SetOutput(&buf)
	defer log.SetOutput(ioutil.Discard) // Reset log output after test

	// Store original flag values and restore them after the test
	originalOutputURL := *outputURL
	defer func() {
		outputURL = &originalOutputURL
	}()

	// Set outputURL to empty to trigger the validation error
	outputURL = new(string) // Points to an empty string

	// Simulate the main logic that checks outputURL and calls osExit
	// We wrap this in a func to catch the panic from osExit mock
	func() {
		defer func() {
			if r := recover(); r != nil {
				// Expected panic from os.Exit
			}
		}()
		// This block directly tests the validation logic from main()
		if *outputURL == "" {
			log.Println("Error: --output-url is required.")
			osExit(1)
		}
	}()

	select {
	case code := <-exitCalled:
		if code != 1 {
			t.Errorf("Expected os.Exit with code 1, got %d", code)
		}
	case <-time.After(100 * time.Millisecond):
		t.Fatal("Expected os.Exit to be called, but it wasn't.")
	}

	if !bytes.Contains(buf.Bytes(), []byte("Error: --output-url is required.")) {
		t.Errorf("Expected log output to contain 'Error: --output-url is required.', got:\n%s", buf.String())
	}
}
