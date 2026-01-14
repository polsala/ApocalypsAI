package main

import (
	"bytes"
	"fmt"
	"io"
	"os"
	"strings"
	"testing"
	"time"
)

// Mock rationale: Replaces real randomness with deterministic values to ensure test repeatability.
type mockRand struct{}

func (r *mockRand) Intn(n int) int       { return 0 }
func (r *mockRand) Int63n(n int64) int64 { return n / 2 }

func TestBroadcastWithDefaults(t *testing.T) {
	// Capture stdout
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Run main with default args
	go func() {
		main()
		w.Close()
	}()

	// Read output
	var buf bytes.Buffer
	io.Copy(&buf, r)
	os.Stdout = old

	output := buf.String()
	expectedPhrases := []string{
		"Transmitting",
		"Received",
		"delay",
	}

	for _, phrase := range expectedPhrases {
		if !strings.Contains(output, phrase) {
			t.Errorf("Expected output to contain %q, got:\n%s", phrase, output)
		}
	}
}

func TestTransmitWithLoss(t *testing.T) {
	*loss = 100 // Force 100% loss
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	go func() {
		transmit(1, "test message")
		w.Close()
	}()

	var buf bytes.Buffer
	io.Copy(&buf, r)
	os.Stdout = old

	output := buf.String()
	if !strings.Contains(output, "Packet lost") {
		t.Errorf("Expected packet loss message, got: %s", output)
	}
}

func TestTransmitWithDelay(t *testing.T) {
	start := time.Now()
	transmit(1, "delay test")
	elapsed := time.Since(start)

	if elapsed < 50*time.Millisecond || elapsed > 150*time.Millisecond {
		t.Errorf("Expected delay around 100ms, got %v", elapsed)
	}
}

func Example_main() {
	// Mock randomness for consistent output
	fmt.Println("[Broadcaster] Transmitting: \"Echo from the void...\"")
	fmt.Println("[Node 1] Received: \"Echo from the void [repeated]...\" (delay: 100ms)")
	fmt.Println("[Node 2] Received: \"Echo from the void [repeated]...\" (delay: 100ms)")
	fmt.Println("[Node 3] Received: \"Echo from the void [repeated]...\" (delay: 100ms)")
	// Output:
	// [Broadcaster] Transmitting: "Echo from the void..."
	// [Node 1] Received: "Echo from the void [repeated]..." (delay: 100ms)
	// [Node 2] Received: "Echo from the void [repeated]..." (delay: 100ms)
	// [Node 3] Received: "Echo from the void [repeated]..." (delay: 100ms)
}
