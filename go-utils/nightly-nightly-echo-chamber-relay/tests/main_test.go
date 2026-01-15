package main

import (
	"fmt"
	"os"
	"strings"
	"testing"
	"time"
)

// Mock rationale: We need to control the outcome of network interactions (latency, success/failure)
// to ensure deterministic and offline tests. By replacing the global sendWhisperFunc,
// we can inject predefined behaviors without actual network calls or random delays.

// TestSendWhisperSuccess tests a successful whisper relay.
func TestSendWhisperSuccess(t *testing.T) {
	// Temporarily override the global sendWhisperFunc for this test
	originalSendWhisperFunc := sendWhisperFunc
	defer func() { sendWhisperFunc = originalSendWhisperFunc }() // Restore after test

	sendWhisperFunc = func(post ListeningPost, message string) RelayResult {
		return RelayResult{
			PostURL: post.URL,
			Status:  "Success",
			Latency: 100 * time.Millisecond,
			Error:   "",
		}
	}

	post := ListeningPost{URL: "test-chamber.void", MinLatencyMs: 1, MaxLatencyMs: 1, FailureRate: 0.0}
	result := sendWhisperFunc(post, "hello")

	if result.Status != "Success" {
		t.Errorf("Expected status 'Success', got '%s'", result.Status)
	}
	if result.Latency != 100*time.Millisecond {
		t.Errorf("Expected latency 100ms, got %s", result.Latency)
	}
	if result.Error != "" {
		t.Errorf("Expected no error, got '%s'", result.Error)
	}
}

// TestSendWhisperFailure tests a failed whisper relay.
func TestSendWhisperFailure(t *testing.T) {
	originalSendWhisperFunc := sendWhisperFunc
	defer func() { sendWhisperFunc = originalSendWhisperFunc }()

	sendWhisperFunc = func(post ListeningPost, message string) RelayResult {
		return RelayResult{
			PostURL: post.URL,
			Status:  "Failure",
			Latency: 200 * time.Millisecond,
			Error:   "Mocked connection refused",
		}
	}

	post := ListeningPost{URL: "failing-chamber.void", MinLatencyMs: 1, MaxLatencyMs: 1, FailureRate: 1.0}
	result := sendWhisperFunc(post, "ping")

	if result.Status != "Failure" {
		t.Errorf("Expected status 'Failure', got '%s'", result.Status)
	}
	if result.Latency != 200*time.Millisecond {
		t.Errorf("Expected latency 200ms, got %s", result.Latency)
	}
	if result.Error != "Mocked connection refused" {
		t.Errorf("Expected error 'Mocked connection refused', got '%s'", result.Error)
	}
}

// TestMainFunctionWithAllSuccess mocks the main execution path with all successful relays.
func TestMainFunctionWithAllSuccess(t *testing.T) {
	originalSendWhisperFunc := sendWhisperFunc
	defer func() { sendWhisperFunc = originalSendWhisperFunc }()

	// Mock rationale: sendWhisperFunc is replaced to ensure all simulated network calls succeed
	// with a predictable latency, making the test deterministic.
	sendWhisperFunc = func(post ListeningPost, message string) RelayResult {
		return RelayResult{
			PostURL: post.URL,
			Status:  "Success",
			Latency: 50 * time.Millisecond,
			Error:   "",
		}
	}

	// Capture stdout
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Set command-line arguments
	os.Args = []string{"nightly-echo-chamber-relay", "test-message"}

	main() // Run the main function

	w.Close()
	os.Stdout = oldStdout // Restore stdout
	out, _ := os.ReadFile(r.Name())
	output := string(out)

	if !strings.Contains(output, "Relaying whisper \"test-message\" to 4 echo chambers...") {
		t.Errorf("Output missing initial message: %s", output)
	}
	if !strings.Contains(output, "✅ echo-chamber-alpha.void") {
		t.Errorf("Output missing alpha success: %s", output)
	}
	if !strings.Contains(output, "✅ echo-chamber-beta.void") {
		t.Errorf("Output missing beta success: %s", output)
	}
	if !strings.Contains(output, "✅ echo-chamber-gamma.void") {
		t.Errorf("Output missing gamma success: %s", output)
	}
	if !strings.Contains(output, "✅ echo-chamber-delta.void") {
		t.Errorf("Output missing delta success: %s", output)
	}
	if !strings.Contains(output, "Summary: 4 successful echoes, 0 failed echoes.") {
		t.Errorf("Output missing correct summary: %s", output)
	}
}

// TestMainFunctionWithMixedResults mocks the main execution path with mixed success/failure.
func TestMainFunctionWithMixedResults(t *testing.T) {
	originalSendWhisperFunc := sendWhisperFunc
	defer func() { sendWhisperFunc = originalSendWhisperFunc }()

	// Mock rationale: sendWhisperFunc is replaced to provide a predefined mix of successful
	// and failed outcomes for specific URLs, ensuring the test covers different result scenarios.
	mockResults := map[string]RelayResult{
		"echo-chamber-alpha.void": {PostURL: "echo-chamber-alpha.void", Status: "Success", Latency: 60 * time.Millisecond, Error: ""},
		"echo-chamber-beta.void":  {PostURL: "echo-chamber-beta.void", Status: "Failure", Latency: 120 * time.Millisecond, Error: "Connection timed out"},
		"echo-chamber-gamma.void": {PostURL: "echo-chamber-gamma.void", Status: "Success", Latency: 30 * time.Millisecond, Error: ""},
		"echo-chamber-delta.void": {PostURL: "echo-chamber-delta.void", Status: "Failure", Latency: 250 * time.Millisecond, Error: "Access denied"},
	}
	sendWhisperFunc = func(post ListeningPost, message string) RelayResult {
		if res, ok := mockResults[post.URL]; ok {
			return res
		}
		return RelayResult{PostURL: post.URL, Status: "Failure", Latency: 1 * time.Millisecond, Error: "Unexpected post"}
	}

	// Capture stdout
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Set command-line arguments
	os.Args = []string{"nightly-echo-chamber-relay", "urgent-broadcast"}

	main() // Run the main function

	w.Close()
	os.Stdout = oldStdout // Restore stdout
	out, _ := os.ReadFile(r.Name())
	output := string(out)

	if !strings.Contains(output, "Relaying whisper \"urgent-broadcast\" to 4 echo chambers...") {
		t.Errorf("Output missing initial message: %s", output)
	}
	if !strings.Contains(output, "✅ echo-chamber-alpha.void") {
		t.Errorf("Output missing alpha success: %s", output)
	}
	if !strings.Contains(output, "❌ echo-chamber-beta.void | Status: Failure | Latency: 120ms     | Error: Connection timed out") {
		t.Errorf("Output missing beta failure: %s", output)
	}
	if !strings.Contains(output, "✅ echo-chamber-gamma.void") {
		t.Errorf("Output missing gamma success: %s", output)
	}
	if !strings.Contains(output, "❌ echo-chamber-delta.void | Status: Failure | Latency: 250ms     | Error: Access denied") {
		t.Errorf("Output missing delta failure: %s", output)
	}
	if !strings.Contains(output, "Summary: 2 successful echoes, 2 failed echoes.") {
		t.Errorf("Output missing correct summary: %s", output)
	}
}

// TestMainFunctionNoArgs tests the case where no arguments are provided.
func TestMainFunctionNoArgs(t *testing.T) {
	// Capture stdout
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Mock rationale: osExit is replaced to prevent the test from terminating the program
	// prematurely. Instead, it records the exit code and panics, allowing the test to recover
	// and assert the expected exit behavior.
	var exitCode int
	originalOsExit := osExit
	osExit = func(code int) {
		exitCode = code
		panic("os.Exit called") // Panic to stop execution, caught by recover
	}
	defer func() {
		os.Stdout = oldStdout // Restore stdout
		osExit = originalOsExit // Restore os.Exit
		if r := recover(); r == nil {
			t.Errorf("Expected panic due to os.Exit, but no panic occurred")
		}
	}()

	os.Args = []string{"nightly-echo-chamber-relay"} // No arguments

	main() // This should call os.Exit(1) and panic

	w.Close()

	out, _ := os.ReadFile(r.Name())
	output := string(out)

	if !strings.Contains(output, "Usage: nightly-echo-chamber-relay <whisper_message>") {
		t.Errorf("Expected usage message, got: %s", output)
	}
	if exitCode != 1 {
		t.Errorf("Expected exit code 1, got %d", exitCode)
	}
}
