package main

import (
	"bufio"
	"context"
	"fmt"
	"io"
	"net"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock rationale: For testing the `startServer` and `handleConnection` functions,
// we use actual TCP sockets on dynamically assigned local ports (`127.0.0.1:0`).
// This approach simulates real network interactions without requiring external services
// or complex mocking frameworks, making the tests deterministic and offline.
// The `context.WithCancel` is used to gracefully shut down the server goroutine,
// ensuring tests clean up resources and don't leave lingering processes.

// startTestServer starts the echo server in a goroutine for testing.
// It returns the address the server is listening on and a cleanup function.
func startTestServer(t *testing.T, cfg Config) (string, func()) {
	ctx, cancel := context.WithCancel(context.Background())
	var wg sync.WaitGroup
	wg.Add(1)

	// Find an available port by listening on "127.0.0.1:0" and immediately closing.
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("Failed to find an available port: %v", err)
	}
	addr := listener.Addr().String()
	port := listener.Addr().(*net.TCPAddr).Port
	listener.Close() // Close it immediately, we just needed the port

	cfg.Port = port // Update config with the chosen port

	serverErrChan := make(chan error, 1)
	go startServer(ctx, cfg, &wg, serverErrChan) // Start the actual server function in a goroutine

	// Give the server a moment to start listening, or check for immediate error
	select {
	case err := <-serverErrChan:
		t.Fatalf("Server failed to start: %v", err)
	case <-time.After(10 * time.Millisecond):
		// Server likely started successfully
	}

	return addr, func() {
		cancel()    // Signal the server to shut down
		wg.Wait()   // Wait for the server goroutine to finish
		select {
		case err := <-serverErrChan:
			t.Errorf("Server encountered error during shutdown: %v", err)
		default:
			// No error, or already handled
		}
	}
}

// connectAndSend connects to the server, sends a message, and reads the response.
func connectAndSend(t *testing.T, addr, message string, expectedResponse string, minDelay time.Duration) {
	conn, err := net.Dial("tcp", addr)
	if err != nil {
		t.Fatalf("Failed to connect to server at %s: %v", addr, err)
	}
	defer conn.Close()

	// Set a read deadline to prevent tests from hanging indefinitely
	conn.SetReadDeadline(time.Now().Add(5 * time.Second))

	startTime := time.Now()
	_, err = fmt.Fprintf(conn, "%s\n", message)
	if err != nil {
		t.Fatalf("Failed to send message: %v", err)
	}

	response, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		t.Fatalf("Failed to read response: %v", err)
	}
	endTime := time.Now()

	actualResponse := strings.TrimSpace(response)
	if actualResponse != expectedResponse {
		t.Errorf("Expected '%s', got '%s'", expectedResponse, actualResponse)
	}

	// Check delay if applicable
	if minDelay > 0 {
		duration := endTime.Sub(startTime)
		if duration < minDelay {
			t.Errorf("Expected response after at least %v, got after %v", minDelay, duration)
		}
	}
}

func TestTemporalEchoListener_NoDistortion(t *testing.T) {
	cfg := Config{
		Port:        0, // Will be overridden by startTestServer
		EchoDelay:   0,
		EchoReverse: false,
	}
	addr, cleanup := startTestServer(t, cfg)
	defer cleanup()

	connectAndSend(t, addr, "hello", "hello", 0)
	connectAndSend(t, addr, "world", "world", 0)
}

func TestTemporalEchoListener_WithDelay(t *testing.T) {
	delay := 100 * time.Millisecond
	cfg := Config{
		Port:        0,
		EchoDelay:   delay,
		EchoReverse: false,
	}
	addr, cleanup := startTestServer(t, cfg)
	defer cleanup()

	connectAndSend(t, addr, "delayed message", "delayed message", delay)
}

func TestTemporalEchoListener_WithReversal(t *testing.T) {
	cfg := Config{
		Port:        0,
		EchoDelay:   0,
		EchoReverse: true,
	}
	addr, cleanup := startTestServer(t, cfg)
	defer cleanup()

	connectAndSend(t, addr, "reverse me", "em esrever", 0)
	connectAndSend(t, addr, "GoLang", "gnaLGo", 0)
	connectAndSend(t, addr, "你好世界", "界世好你", 0) // Test with Unicode
}

func TestTemporalEchoListener_WithDelayAndReversal(t *testing.T) {
	delay := 50 * time.Millisecond
	cfg := Config{
		Port:        0,
		EchoDelay:   delay,
		EchoReverse: true,
	}
	addr, cleanup := startTestServer(t, cfg)
	defer cleanup()

	connectAndSend(t, addr, "combo", "obmoc", delay)
}

func TestTemporalEchoListener_MultipleConnections(t *testing.T) {
	cfg := Config{
		Port:        0,
		EchoDelay:   20 * time.Millisecond,
		EchoReverse: false,
	}
	addr, cleanup := startTestServer(t, cfg)
	defer cleanup()

	var wg sync.WaitGroup
	numClients := 5
	for i := 0; i < numClients; i++ {
		wg.Add(1)
		go func(clientID int) {
			defer wg.Done()
			message := fmt.Sprintf("client %d message", clientID)
			connectAndSend(t, addr, message, message, cfg.EchoDelay)
		}(i)
	}
	wg.Wait()
}

func TestTemporalEchoListener_EnvVarConfig(t *testing.T) {
	// Set environment variables for this test
	os.Setenv("PORT", "0") // Dynamic port
	os.Setenv("ECHO_DELAY_MS", "75")
	os.Setenv("ECHO_REVERSE", "true")
	defer func() {
		os.Unsetenv("PORT")
		os.Unsetenv("ECHO_DELAY_MS")
		os.Unsetenv("ECHO_REVERSE")
	}()

	// Load config from env vars
	cfg := loadConfig()
	if cfg.EchoDelay != 75*time.Millisecond {
		t.Errorf("Expected delay 75ms, got %v", cfg.EchoDelay)
	}
	if !cfg.EchoReverse {
		t.Errorf("Expected reverse true, got %t", cfg.EchoReverse)
	}

	addr, cleanup := startTestServer(t, cfg)
	defer cleanup()

	connectAndSend(t, addr, "env test", "tset vne", 75*time.Millisecond)
}

func TestTemporalEchoListener_EmptyMessageHandling(t *testing.T) {
	cfg := Config{
		Port:        0,
		EchoDelay:   0,
		EchoReverse: false,
	}
	addr, cleanup := startTestServer(t, cfg)
	defer cleanup()

	conn, err := net.Dial("tcp", addr)
	if err != nil {
		t.Fatalf("Failed to connect to server at %s: %v", addr, err)
	}
	defer conn.Close()

	// Send an empty line
	_, err = fmt.Fprintf(conn, "\n")
	if err != nil {
		t.Fatalf("Failed to send empty message: %v", err)
	}

	// Try to read a response, expect nothing or timeout
	readChan := make(chan string)
	errorChan := make(chan error)
	go func() {
		conn.SetReadDeadline(time.Now().Add(100 * time.Millisecond)) // Short deadline
		response, err := bufio.NewReader(conn).ReadString('\n')
		if err != nil {
			errorChan <- err
			return
		}
		readChan <- response
	}()

	select {
	case response := <-readChan:
		t.Errorf("Received unexpected response for empty message: '%s'", strings.TrimSpace(response))
	case err := <-errorChan:
		// Expected error could be timeout or EOF if server closes connection (it shouldn't for empty line)
		if !strings.Contains(err.Error(), "i/o timeout") && err != io.EOF {
			t.Errorf("Received unexpected error for empty message: %v", err)
		}
	case <-time.After(200 * time.Millisecond):
		// This is the expected outcome: no response within a reasonable time
		t.Log("Successfully received no response for empty message (timeout).")
	}
}
