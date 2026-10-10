package main

import (
	"io"
	"os"
	"strings"
	"testing"
)

// TestScavenge_Found tests finding a resource that exists.
func TestScavenge_Found(t *testing.T) {
	// # Mock rationale: Using the predefined `ZoneContents` map ensures deterministic
	// # outcomes for the `Scavenge` function without external dependencies.
	// # The random delay within `Scavenge` is ignored for result verification.

	target := "scrap metal"
	zone := "Old Factory"
	result := Scavenge(zone, target)

	if !result.Found {
		t.Errorf("Expected to find '%s' in '%s', but it was not found. Message: %s", target, zone, result.Message)
	}
	// The message includes the original target string, so we check for its presence.
	if !strings.Contains(result.Message, "Found 'scrap metal' in Old Factory!") {
		t.Errorf("Expected message to indicate success and contain target, got '%s'", result.Message)
	}
}

// TestScavenge_NotFound tests searching for a resource that does not exist.
func TestScavenge_NotFound(t *testing.T) {
	target := "rare artifact"
	zone := "Abandoned Mall"
	result := Scavenge(zone, target)

	if result.Found {
		t.Errorf("Expected not to find '%s' in '%s', but it was found. Message: %s", target, zone, result.Message)
	}
	// The message includes the original target string, so we check for its presence.
	if !strings.Contains(result.Message, "'rare artifact' not found in Abandoned Mall.") {
		t.Errorf("Expected message to indicate failure and contain target, got '%s'", result.Message)
	}
}

// TestScavenge_ZoneNotFound tests searching in a non-existent zone.
func TestScavenge_ZoneNotFound(t *testing.T) {
	target := "water"
	zone := "Non-Existent Zone"
	result := Scavenge(zone, target)

	if result.Found {
		t.Errorf("Expected not to find '%s' in '%s', but it was found. Message: %s", target, zone, result.Message)
	}
	expectedMessage := "Zone not recognized or empty."
	if result.Message != expectedMessage {
		t.Errorf("Expected message '%s', got '%s'", expectedMessage, result.Message)
	}
}

// TestScavenge_CaseInsensitive tests if the search is case-insensitive.
func TestScavenge_CaseInsensitive(t *testing.T) {
	target := "ScRaP MeTaL" // Mixed case
	zone := "Old Factory"
	result := Scavenge(zone, target)

	if !result.Found {
		t.Errorf("Expected to find '%s' (case-insensitive) in '%s', but it was not found. Message: %s", target, zone, result.Message)
	}
	// Message uses original target, but indicates success.
	if !strings.Contains(result.Message, "Found 'ScRaP MeTaL' in Old Factory!") {
		t.Errorf("Expected message to indicate success and contain target, got '%s'", result.Message)
	}
}

// TestMainFunction_Integration tests the main function's output for a simple scenario.
// This test captures stdout to verify the overall program flow and output.
func TestMainFunction_Integration(t *testing.T) {
	// # Mock rationale: By temporarily redirecting os.Stdout and providing specific
	// # arguments, we can deterministically test the main function's output
	// # without actual console interaction. The `ZoneContents` global mock ensures
	// # the `Scavenge` function's behavior is predictable. The random seed for `rand.Intn`
	// # is initialized in `main`, but for this test, we only care about the presence
	// # of specific output lines, not their exact order due to variable delays.

	// Save original os.Stdout and redirect to a pipe
	oldStdout := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	// Set up mock command-line arguments
	os.Args = []string{"cmd", "water filter", "Abandoned Mall", "Overgrown Park"}

	// Run main in a goroutine to allow capturing output
	done := make(chan struct{})
	go func() {
		main()
		w.Close()
		done <- struct{}{}
	}()

	// Read output from the pipe
	<-done
	os.Stdout = oldStdout // Restore original Stdout
	out, _ := io.ReadAll(r)
	output := string(out)

	// Assertions: Check for key phrases in the captured output
	if !strings.Contains(output, "Dispatching scavenger swarm to find 'water filter' across 2 zones...") {
		t.Errorf("Output missing initial dispatch message: %s", output)
	}
	if !strings.Contains(output, "[SUCCESS] Found 'water filter' in Abandoned Mall!") {
		t.Errorf("Output missing success message for 'water filter': %s", output)
	}
	if !strings.Contains(output, "[FAILURE] 'water filter' not found in Overgrown Park.") {
		t.Errorf("Output missing failure message for 'water filter': %s", output)
	}
	if !strings.Contains(output, "Successfully located 'water filter' in 1 out of 2 zones.") {
		t.Errorf("Output missing summary message: %s", output)
	}

	// Test case for no resources found
	// Reset stdout for next capture
	r, w, _ = os.Pipe()
	os.Stdout = w

	os.Args = []string{"cmd", "nonexistent resource", "Old Factory", "Abandoned Mall"}
	done = make(chan struct{})
	go func() {
		main()
		w.Close()
		done <- struct{}{}
	}()
	<-done
	os.Stdout = oldStdout
	out, _ = io.ReadAll(r)
	output = string(out)

	if !strings.Contains(output, "'nonexistent resource' was not found in any of the 2 zones.") {
		t.Errorf("Output missing 'not found in any zones' summary: %s", output)
	}
}
