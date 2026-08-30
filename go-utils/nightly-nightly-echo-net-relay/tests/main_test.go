package main

import (
	"bytes"
	"flag"
	"io"
	"os"
	"strings"
	"testing"
)

// TestApplyEcho tests the applyEcho function with various inputs.
func TestApplyEcho(t *testing.T) {
	tests := []struct {
		name      string
		message   string
		echoLevel int
		expected  string
	}{
		{
			name:      "No Echo, No Distortion (single word)",
			message:   "Hello",
			echoLevel: 0,
			expected:  "Hello",
		},
		{
			name:      "No Echo, Distortion (two words)",
			message:   "Hello World",
			echoLevel: 0,
			expected:  "World Hello", // First two words reversed
		},
		{
			name:      "Basic Echo, No Distortion (single word)",
			message:   "Status",
			echoLevel: 1,
			expected:  "Status (echo)",
		},
		{
			name:      "Basic Echo, Distortion (two words)",
			message:   "Urgent Alert",
			echoLevel: 1,
			expected:  "Alert Urgent (echo)",
		},
		{
			name:      "Multiple Echoes, Distortion (multi-word)",
			message:   "Resource Request Alpha",
			echoLevel: 3,
			expected:  "Request Resource Alpha (echo) (echo) (echo)",
		},
		{
			name:      "Empty Message",
			message:   "",
			echoLevel: 1,
			expected:  " (echo)", // Empty string becomes " (echo)"
		},
		{
			name:      "Message with leading/trailing spaces",
			message:   "  Trim Me  ",
			echoLevel: 1,
			expected:  "Me Trim (echo)", // Fields handles spaces, then reversed
		},
		{
			name:      "Message with more than two words, distortion applies to first two",
			message:   "One Two Three",
			echoLevel: 0,
			expected:  "Two One Three",
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			actual := applyEcho(tt.message, tt.echoLevel)
			if actual != tt.expected {
				t.Errorf("applyEcho(%q, %d) = %q; want %q", tt.message, tt.echoLevel, actual, tt.expected)
			}
		})
	}
}

// TestSimulateForward tests the simulateForward function by capturing stdout.
func TestSimulateForward(t *testing.T) {
	// Mock rationale: Capture stdout to verify the output of simulateForward
	// without actually writing to the console during tests.
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	echoedMessage := "Test Message (echo)"
	nextHop := "Relay Node Gamma"

	simulateForward(echoedMessage, nextHop)

	w.Close()
	out, _ := io.ReadAll(r)
	os.Stdout = oldStdout // Restore stdout

	expectedOutput := fmt.Sprintf("Relaying message: \"%s\"\nNext hop: %s\n", echoedMessage, nextHop)
	if string(out) != expectedOutput {
		t.Errorf("simulateForward output mismatch.\nGot:\n%q\nWant:\n%q", string(out), expectedOutput)
	}
}

// TestRunFunction tests the run function's error handling and successful execution.
func TestRunFunction(t *testing.T) {
	// Mock rationale: Capture stdout/stderr to verify output and error messages.
	// Also, mock os.Exit to prevent the test runner from exiting.
	oldStdout := os.Stdout
	oldStderr := os.Stderr
	oldArgs := os.Args
	oldExit := exitFunc // Store original exitFunc

	// Override os.Exit for testing
	var exitCalledWith int
	exitFunc = func(code int) {
		exitCalledWith = code
		// Do not panic here, just record the code.
		// The `run` function itself returns the code, so we can test that directly.
		// This mock is primarily for the `main` function, but `run` is what we're testing here.
		// For `run`, we just check its return value.
	}

	defer func() {
		os.Stdout = oldStdout
		os.Stderr = oldStderr
		os.Args = oldArgs
		exitFunc = oldExit // Restore original exitFunc
	}()

	// Test case 1: No message provided (should return 1)
	t.Run("NoMessageProvided", func(t *testing.T) {
		var buf bytes.Buffer
		os.Stdout = &buf
		os.Stderr = &buf // Capture stderr too for usage message

		os.Args = []string{"nightly-echo-net-relay"} // No flags
		exitCalledWith = 0 // Reset exit code

		// Reset flags for each test run, as flag.Parse() is global
		flag.CommandLine = flag.NewFlagSet(os.Args[0], flag.ExitOnError)
		code := run()

		if code != 1 {
			t.Errorf("Expected run() to return 1 for no message, got %d", code)
		}
		output := buf.String()
		if !strings.Contains(output, "Error: A message is required.") {
			t.Errorf("Expected error message not found in output: %q", output)
		}
		if !strings.Contains(output, "Usage of nightly-echo-net-relay:") {
			t.Errorf("Expected usage message not found in output: %q", output)
		}
	})

	// Test case 2: Valid message provided (should return 0)
	t.Run("ValidMessage", func(t *testing.T) {
		var buf bytes.Buffer
		os.Stdout = &buf
		os.Stderr = &buf // Capture stderr too

		os.Args = []string{"nightly-echo-net-relay", "-message", "Hello World", "-level", "2", "-next-hop", "Alpha Base"}
		exitCalledWith = 0 // Reset exit code

		// Reset flags for each test run
		flag.CommandLine = flag.NewFlagSet(os.Args[0], flag.ExitOnError)
		code := run()

		if code != 0 {
			t.Errorf("Expected run() to return 0 for valid message, got %d", code)
		}
		output := buf.String()
		expectedOutput := "Relaying message: \"World Hello (echo) (echo)\"\nNext hop: Alpha Base\n"
		if output != expectedOutput {
			t.Errorf("Run function output mismatch.\nGot:\n%q\nWant:\n%q", output, expectedOutput)
		}
	})

	// Test case 3: Valid message with default level and next-hop (should return 0)
	t.Run("ValidMessageWithDefaults", func(t *testing.T) {
		var buf bytes.Buffer
		os.Stdout = &buf
		os.Stderr = &buf // Capture stderr too

		os.Args = []string{"nightly-echo-net-relay", "-message", "Ping"}
		exitCalledWith = 0 // Reset exit code

		// Reset flags for each test run
		flag.CommandLine = flag.NewFlagSet(os.Args[0], flag.ExitOnError)
		code := run()

		if code != 0 {
			t.Errorf("Expected run() to return 0 for valid message, got %d", code)
		}
		output := buf.String()
		expectedOutput := "Relaying message: \"Ping (echo)\"\nNext hop: Unknown Relay\n" // "Ping" is a single word, no distortion
		if output != expectedOutput {
			t.Errorf("Run function output mismatch.\nGot:\n%q\nWant:\n%q", output, expectedOutput)
		}
	})
}

// TestMainExitCode ensures the main function calls exitFunc with the correct code.
func TestMainExitCode(t *testing.T) {
	oldExit := exitFunc
	defer func() { exitFunc = oldExit }()

	var capturedExitCode int
	exitFunc = func(code int) {
		capturedExitCode = code
	}

	// Mock rationale: Temporarily redirect os.Stdout and os.Stderr to prevent
	// actual output during the test, as `main` might print usage or errors.
	oldStdout := os.Stdout
	oldStderr := os.Stderr
	rOut, wOut, _ := os.Pipe()
	rErr, wErr, _ := os.Pipe()
	os.Stdout = wOut
	os.Stderr = wErr
	defer func() {
		wOut.Close()
		wErr.Close()
		io.ReadAll(rOut) // Drain pipes
		io.ReadAll(rErr)
		os.Stdout = oldStdout
		os.Stderr = oldStderr
	}()

	// Test successful exit
	os.Args = []string{"nightly-echo-net-relay", "-message", "Test"}
	flag.CommandLine = flag.NewFlagSet(os.Args[0], flag.ExitOnError) // Reset flags
	main()
	if capturedExitCode != 0 {
		t.Errorf("main() with valid args: Expected exit code 0, got %d", capturedExitCode)
	}

	// Test error exit
	os.Args = []string{"nightly-echo-net-relay"} // Missing message
	flag.CommandLine = flag.NewFlagSet(os.Args[0], flag.ExitOnError) // Reset flags
	main()
	if capturedExitCode != 1 {
		t.Errorf("main() with missing message: Expected exit code 1, got %d", capturedExitCode)
	}
}
