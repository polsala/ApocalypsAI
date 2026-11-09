package main

import (
	"bytes"
	"fmt"
	"log"
	"net"
	"os"
	"strings"
	"sync"
	"testing"
	"time"
)

// Mock rationale: We need to test the aggregation logic and graceful shutdown without
// relying on actual network I/O, which can be flaky and non-deterministic.
// Instead of mocking `net.UDPConn` directly (which is complex due to its methods),
// we test the `aggregateWhispers` and `processCollectiveThought` functions by
// feeding them data via channels and capturing log output.
// For the `listenUDP` function, we'll use a real UDP connection in a controlled
// test environment to ensure it correctly receives and forwards messages,
// but ensure it's shut down gracefully.

// TestNewWhisperNetAggregator ensures the constructor works
func TestNewWhisperNetAggregator(t *testing.T) {
	cfg := Config{Port: 9000, Interval: 5 * time.Second}
	agg := NewWhisperNetAggregator(cfg)

	if agg == nil {
		t.Fatal("NewWhisperNetAggregator returned nil")
	}
	if agg.config.Port != 9000 {
		t.Errorf("Expected port 9000, got %d", agg.config.Port)
	}
	if agg.config.Interval != 5*time.Second {
		t.Errorf("Expected interval 5s, got %s", agg.config.Interval)
	}
	if agg.whisperCh == nil {
		t.Error("whisperCh is nil")
	}
	if agg.stopCh == nil {
		t.Error("stopCh is nil")
	}
}

// TestAggregateWhispersLogic tests the core aggregation and processing logic
func TestAggregateWhispersLogic(t *testing.T) {
	cfg := Config{Port: 0, Interval: 100 * time.Millisecond} // Short interval for testing
	agg := NewWhisperNetAggregator(cfg)

	var logBuffer bytes.Buffer
	log.SetOutput(&logBuffer)
	defer log.SetOutput(os.Stderr) // Restore default stderr after test

	// Start the aggregator goroutine
	agg.wg.Add(1)
	go agg.aggregateWhispers()

	// Send some whispers
	agg.whisperCh <- "whisper 1"
	agg.whisperCh <- "whisper 2"
	agg.whisperCh <- "whisper 3"

	// Wait for the first aggregation interval to pass
	time.Sleep(150 * time.Millisecond) // Slightly longer than interval

	// Check log output for collective thought
	output := logBuffer.String()
	if !strings.Contains(output, "The collective consciousness stirred with 3 whispers: \"whisper 1\", \"whisper 2\", \"whisper 3\"") {
		t.Errorf("Expected collective thought for 3 whispers, got:\n%s", output)
	}
	logBuffer.Reset() // Clear buffer for next check

	// Send more whispers for a second interval
	agg.whisperCh <- "whisper 4"
	time.Sleep(150 * time.Millisecond)

	output = logBuffer.String()
	if !strings.Contains(output, "A lone whisper echoed: \"whisper 4\"") {
		t.Errorf("Expected collective thought for 1 whisper, got:\n%s", output)
	}
	logBuffer.Reset()

	// Test no whispers
	time.Sleep(150 * time.Millisecond)
	output = logBuffer.String()
	if strings.Contains(output, "[COLLECTIVE THOUGHT]") {
		t.Errorf("Expected no collective thought when no whispers, got:\n%s", output)
	}
	logBuffer.Reset()

	// Stop the aggregator
	close(agg.stopCh)
	agg.wg.Wait() // Wait for aggregateWhispers to finish
}

// TestAggregateWhispersShutdown tests that remaining whispers are processed on shutdown
func TestAggregateWhispersShutdown(t *testing.T) {
	cfg := Config{Port: 0, Interval: 1 * time.Hour} // Long interval, so it won't tick
	agg := NewWhisperNetAggregator(cfg)

	var logBuffer bytes.Buffer
	log.SetOutput(&logBuffer)
	defer log.SetOutput(os.Stderr)

	agg.wg.Add(1)
	go agg.aggregateWhispers()

	agg.whisperCh <- "shutdown whisper 1"
	agg.whisperCh <- "shutdown whisper 2"

	// Give goroutine a moment to read from channel
	time.Sleep(50 * time.Millisecond)

	// Stop the aggregator
	close(agg.stopCh)
	agg.wg.Wait() // Wait for aggregateWhispers to finish

	output := logBuffer.String()
	if !strings.Contains(output, "The collective consciousness stirred with 2 whispers: \"shutdown whisper 1\", \"shutdown whisper 2\"") {
		t.Errorf("Expected remaining whispers to be processed on shutdown, got:\n%s", output)
	}
}

// TestListenUDPAndStop tests the UDP listener's ability to receive and shut down
func TestListenUDPAndStop(t *testing.T) {
	// Use a random available port for testing
	addr, err := net.ResolveUDPAddr("udp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("Failed to resolve UDP address: %v", err)
	}
	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		t.Fatalf("Failed to listen on UDP: %v", err)
	}
	port := conn.LocalAddr().(*net.UDPAddr).Port
	conn.Close() // Close it, aggregator will open it

	cfg := Config{Port: port, Interval: 1 * time.Hour} // Long interval, focus on listener
	agg := NewWhisperNetAggregator(cfg)

	// Start the aggregator (which includes listenUDP)
	err = agg.Start()
	if err != nil {
		t.Fatalf("Failed to start aggregator: %v", err)
	}

	// Send a whisper
	clientConn, err := net.DialUDP("udp", nil, &net.UDPAddr{IP: net.ParseIP("127.0.0.1"), Port: port})
	if err != nil {
		t.Fatalf("Failed to dial UDP: %v", err)
	}
	defer clientConn.Close()

	message := "test whisper"
	_, err = clientConn.Write([]byte(message))
	if err != nil {
		t.Fatalf("Failed to send message: %v", err)
	}

	// Give time for the message to be processed by listenUDP and sent to whisperCh
	time.Sleep(50 * time.Millisecond)

	// Check if the whisper was received by the channel
	select {
	case receivedWhisper := <-agg.whisperCh:
		if receivedWhisper != message {
			t.Errorf("Expected '%s', got '%s'", message, receivedWhisper)
		}
	case <-time.After(1 * time.Second):
		t.Fatal("Timed out waiting for whisper to appear in channel")
	}

	// Stop the aggregator and ensure graceful shutdown
	agg.Stop()

	// Try sending another message, it should fail or be ignored
	_, err = clientConn.Write([]byte("after shutdown"))
	if err != nil {
		// This is expected if the server closed the port quickly
		// t.Logf("Expected error sending after shutdown: %v", err)
	}

	// Ensure all goroutines have finished
	done := make(chan struct{})
	go func() {
		agg.wg.Wait()
		close(done)
	}()

	select {
	case <-done:
		// Success, goroutines finished
	case <-time.After(1 * time.Second):
		t.Fatal("Timed out waiting for goroutines to finish after stop")
	}
}

// TestMainFunctionConceptual is a conceptual test for main,
// but actual signal handling is hard to test programmatically in Go's `testing` framework.
// Mock rationale: Testing `main` with actual OS signals (`syscall.SIGINT`, `syscall.SIGTERM`)
// is outside the scope of deterministic, offline unit testing. It typically requires
// running the binary as a separate process and sending signals, which is integration testing.
// We assume `os/signal` and `syscall` work as expected and focus on the `WhisperNetAggregator`'s
// `Start` and `Stop` methods, which `main` orchestrates.
func TestMainFunctionConceptual(t *testing.T) {
	// This test is purely conceptual and does not execute the main function directly.
	// It serves as a placeholder to acknowledge the difficulty of testing `main` with signals
	// in a unit test context.
	t.Log("Conceptual test for main function's signal handling. Actual testing requires integration tests.")
	// To properly test main, one would typically:
	// 1. Compile the main package into an executable.
	// 2. Run the executable in a separate process.
	// 3. Send OS signals (e.g., SIGINT) to that process.
	// 4. Verify the process exits gracefully.
	// This is beyond the scope of a self-contained, offline unit test.
}
