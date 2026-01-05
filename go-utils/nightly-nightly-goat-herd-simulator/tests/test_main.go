package main

import (
	"os"
	"strings"
	"testing"
	"time"
)

// TestHerdInitialization ensures a herd is created with correct initial size
func TestHerdInitialization(t *testing.T) {
	herd := NewHerd(5, false)

	if herd.Size != 5 {
		t.Errorf("Expected herd size 5, got %d", herd.Size)
	}

	if herd.Events == nil {
		t.Error("Events channel should be initialized")
	}

	if herd.Done == nil {
		t.Error("Done channel should be initialized")
	}
}

// TestAddInitialGoats verifies initial goat population
func TestAddInitialGoats(t *testing.T) {
	herd := NewHerd(3, false)
	herd.addInitialGoats()

	if len(herd.Goats) != 3 {
		t.Errorf("Expected 3 initial goats, got %d", len(herd.Goats))
	}

	for _, goat := range herd.Goats {
		if goat.Name == "" {
			t.Error("Goat should have a non-empty name")
		}
		if goat.Age < 1 || goat.Age > 5 {
			t.Errorf("Goat age should be between 1-5, got %d", goat.Age)
		}
	}
}

// TestReproductionBehavior mocks reproduction logic to ensure deterministic outcomes
func TestReproductionBehavior(t *testing.T) {
	herd := NewHerd(1, false)
	herd.addInitialGoats()

	// Mock rand.Float64 to always return 0.0 (trigger reproduction)
	originalRand := rand.Float64
	defer func() { rand.Float64 = originalRand }()

	// Override rand.Float64 for deterministic test
	var callCount int
	rand.Float64 = func() float64 {
		callCount++
		return 0.0 // Always trigger reproduction
	}

	// Simulate a single reproduction cycle
	goat := herd.Goats[0]
	herd.simulateReproduction(goat)

	time.Sleep(100 * time.Millisecond) // Give goroutine time to run
	close(herd.Done)

	time.Sleep(10 * time.Millisecond)

	// Verify a new kid was added
	herd.Mutex.RLock()
	finalSize := len(herd.Goats)
	herd.Mutex.RUnlock()

	if finalSize != 2 {
		t.Errorf("Expected herd size 2 after reproduction, got %d", finalSize)
	}
}

// TestFlagParsing validates command line argument parsing
func TestFlagParsing(t *testing.T) {
	// Save original args
	originalArgs := os.Args
	defer func() { os.Args = originalArgs }()

	// Test default values
	os.Args = []string{"goat-herd-simulator"}
	sz, dur, vb := parseFlags()
	if sz != 10 || dur != 15*time.Second || vb != false {
		t.Error("Default values not set correctly")
	}

	// Test custom herd size
	os.Args = []string{"goat-herd-simulator", "--herd-size", "25"}
	sz, dur, vb = parseFlags()
	if sz != 25 {
		t.Errorf("Expected herd size 25, got %d", sz)
	}

	// Test custom duration
	os.Args = []string{"goat-herd-simulator", "--duration", "10s"}
	sz, dur, vb = parseFlags()
	if dur != 10*time.Second {
		t.Errorf("Expected duration 10s, got %v", dur)
	}

	// Test verbose flag
	os.Args = []string{"goat-herd-simulator", "--verbose"}
	sz, dur, vb = parseFlags()
	if !vb {
		t.Error("Verbose flag not parsed correctly")
	}
}

// TestEventChannel ensures events are sent and received correctly
func TestEventChannel(t *testing.T) {
	herd := NewHerd(1, false)
	herd.addInitialGoats()

	// Send a test event
	testEvent := "Test event from test"
	select {
	case herd.Events <- testEvent:
		// Event sent successfully
	default:
		t.Error("Failed to send event to channel")
	}

	// Receive the event
	received := <-herd.Events
	if received != testEvent {
		t.Errorf("Expected event '%s', got '%s'", testEvent, received)
	}
}

// BenchmarkSimulation runs a quick benchmark of the simulation setup
func BenchmarkSimulation(b *testing.B) {
	for i := 0; i < b.N; i++ {
		herd := NewHerd(10, false)
		herd.addInitialGoats()
	}
}\n
